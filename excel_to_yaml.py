import argparse
import sys
from pathlib import Path
from typing import Optional
import pandas as pd
import yaml

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return out

def detect_sections(xlsx_path: Path):
    xl = pd.ExcelFile(xlsx_path, engine="openpyxl")
    cubes_df_list = []
    joins_df_list = []
    dims_df_list = []
    measures_df_list = []
    for sheet in xl.sheet_names:
        df = pd.read_excel(xlsx_path, sheet_name=sheet, engine="openpyxl")
        if df.empty:
            continue
        ndf = normalize_columns(df)
        cols = set(ndf.columns)
        if {"table", "sql_table", "name", "description", "title"}.issubset(cols):
            cubes_df_list.append(ndf)
        if {"primary_table", "secondary_table", "relationship", "primary_table_key_column", "secondary_table_key_column"}.issubset(cols):
            joins_df_list.append(ndf)
        if {"name", "title", "description", "sql", "primarykey", "type"}.issubset(cols):
            dims_df_list.append(ndf)
        elif {"name", "title", "description", "sql", "type"}.issubset(cols):
            measures_df_list.append(ndf)

    cubes_df = pd.concat(cubes_df_list, ignore_index=True) if cubes_df_list else pd.DataFrame()
    joins_df = pd.concat(joins_df_list, ignore_index=True) if joins_df_list else pd.DataFrame()
    dims_df = pd.concat(dims_df_list, ignore_index=True) if dims_df_list else pd.DataFrame()
    measures_df = pd.concat(measures_df_list, ignore_index=True) if measures_df_list else pd.DataFrame()
    return cubes_df, joins_df, dims_df, measures_df

def coerce_bool(v):
    if pd.isna(v):
        return False
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    return s in ("true", "1", "yes", "y")

def clean_str(s):
    if pd.isna(s):
        return None
    return str(s).strip()

def build_yaml_structure(cubes_df, joins_df, dims_df, measures_df, only_cube: Optional[str] = None):
    result = {}

    # Cubes
    cubes = []
    selected_cube_names = set()
    # Keep a lookup of cube name -> table (from cubes sheet)
    name_to_table = {}
    for _, row in cubes_df.iterrows():
        name = clean_str(row.get("name"))
        if only_cube and name != only_cube:
            continue
        table_name = clean_str(row.get("table"))
        name_to_table[name] = table_name
        cube = {
            "description": clean_str(row.get("description")),
            "name": name,
            "sql_table": clean_str(row.get("sql_table")),
            "title": clean_str(row.get("title")),
        }
        cubes.append(cube)
        if name:
            selected_cube_names.add(name)
    result["cubes"] = cubes

    # Joins
    joins = []
    for _, row in joins_df.iterrows():
        primary_table = clean_str(row.get("primary_table"))
        secondary_table = clean_str(row.get("secondary_table"))
        relationship = clean_str(row.get("relationship"))
        pk = clean_str(row.get("primary_table_key_column"))
        sk = clean_str(row.get("secondary_table_key_column"))

        if only_cube:
            # Include only joins where the primary table matches the selected cube's table or name
            allowed_primary_names = {only_cube}
            if only_cube in name_to_table and name_to_table[only_cube]:
                allowed_primary_names.add(name_to_table[only_cube])
            if primary_table not in allowed_primary_names:
                continue

        joins.append({
            "name": secondary_table,
            "relationship": relationship,
            "sql": f"{pk}={sk}",
        })
    result["joins"] = joins

    # Dimensions
    dimensions = []
    for _, row in dims_df.iterrows():
        dimensions.append({
            "name": clean_str(row.get("name")),
            "title": clean_str(row.get("title")),
            "description": clean_str(row.get("description")),
            "sql": clean_str(row.get("sql")),
            "primaryKey": bool(coerce_bool(row.get("primarykey"))),
            "type": clean_str(row.get("type")),
        })
    result["dimensions"] = dimensions

    # Measures
    measures = []
    for _, row in measures_df.iterrows():
        measures.append({
            "name": clean_str(row.get("name")),
            "title": clean_str(row.get("title")),
            "description": clean_str(row.get("description")),
            "sql": clean_str(row.get("sql")),
            "type": clean_str(row.get("type")),
        })
    result["measures"] = measures

    return result

def main():
    parser = argparse.ArgumentParser(description="Convert Excel semantic template to YAML (cubes, joins, dimensions, measures).")
    parser.add_argument("-i", "--input", required=True, help="Path to input Excel file (.xlsx)")
    parser.add_argument("-o", "--output", required=True, help="Path to output YAML file (.yml)")
    parser.add_argument("--only-cube", help="If set, include only this cube by name and filter joins accordingly.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cubes_df, joins_df, dims_df, measures_df = detect_sections(input_path)
    if cubes_df.empty and joins_df.empty and dims_df.empty and measures_df.empty:
        print("Error: No recognizable sections found. Ensure your sheet headers match the expected columns.", file=sys.stderr)
        sys.exit(1)

    data = build_yaml_structure(cubes_df, joins_df, dims_df, measures_df, only_cube=args.only_cube)

    with output_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=4096)

    print(f"Wrote YAML to: {output_path}")

if __name__ == "__main__":
    main()
