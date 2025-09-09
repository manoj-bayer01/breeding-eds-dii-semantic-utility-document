import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import pandas as pd
import yaml

# -----------------------------
# Utilities for cleaning values
# -----------------------------

def clean_str(v):
    """
    Trim strings; return None for NaN/empty. Preserves special characters like {CUBE} and backticks.
    """
    if pd.isna(v):
        return None
    s = str(v).strip()
    return s if s != "" else None

def coerce_bool(v) -> Optional[bool]:
    """
    Convert a variety of truthy/falsy representations to bool.
    Returns None if value is missing/empty.
    """
    if pd.isna(v):
        return None
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s == "":
        return None
    return s in ("true", "1", "yes", "y", "t")

def drop_empty_rows_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows and columns that are entirely empty (NaN or blank strings).
    """
    if df.empty:
        return df
    # Treat blank strings as NaN for emptiness checks
    df2 = df.copy()
    df2 = df2.applymap(lambda x: None if (isinstance(x, str) and x.strip() == "") else x)
    # Drop columns and rows that are entirely empty
    df2 = df2.dropna(axis=1, how="all").dropna(axis=0, how="all")
    return df2

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize header names to snake_case-ish: lowercase, spaces -> underscores, trimmed.
    Also de-duplicates any repeated column names by appending _2, _3, etc.
    """
    out = df.copy()
    raw_cols = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    deduped = []
    seen = {}
    for c in raw_cols:
        if c not in seen:
            seen[c] = 1
            deduped.append(c)
        else:
            seen[c] += 1
            deduped.append(f"{c}_{seen[c]}")
    out.columns = deduped
    return out

# --------------------------------
# Column aliasing and section logic
# --------------------------------

REQUIRED: Dict[str, set] = {
    # Minimal columns to confidently recognize each section
    "cubes": {"table", "sql_table", "name"},
    "joins": {"primary_table", "secondary_table"},
    "dimensions": {"name", "sql", "type"},
    "measures": {"name", "sql", "type"},
}

# Accept common synonyms and variations for headers
ALIASES: Dict[str, Dict[str, str]] = {
    "cubes": {
        "table_name": "table",
        "cube_table": "table",
        "sqltable": "sql_table",
        "sql table": "sql_table",
        "cube_name": "name",
        "cube": "name",
        "desc": "description",
        "data source": "data_source",
        "data_source": "data_source",
    },
    "joins": {
        "primary table": "primary_table",
        "secondary table": "secondary_table",
        "relation": "relationship",
        "relationship_type": "relationship",
        "primary_table_key": "primary_table_key_column",
        "primary key column": "primary_table_key_column",
        "primary_key_column": "primary_table_key_column",
        "secondary_table_key": "secondary_table_key_column",
        "secondary key column": "secondary_table_key_column",
        "secondary_key_column": "secondary_table_key_column",
        "join_sql": "sql",  # if a direct SQL expression is provided
    },
    "dimensions": {
        "primary key": "primarykey",
        "primary_key": "primarykey",
        "is_primary_key": "primarykey",
        "pk": "primarykey",
        "datatype": "type",
        "data_type": "type",
    },
    "measures": {
        "aggregation": "type",
        "aggregate": "type",
        "agg": "type",
    },
}

def remap_known_columns(df: pd.DataFrame, section: str) -> pd.DataFrame:
    """
    Rename recognized alias columns to canonical names for the given section.
    Leaves unknown columns intact (normalized).
    """
    alias_map = ALIASES.get(section, {})
    rename_map = {}
    for c in df.columns:
        key = c.strip().lower()
        # unify spaces and underscores when matching aliases
        key_compact = key.replace(" ", "_")
        if key in alias_map:
            rename_map[c] = alias_map[key]
        elif key_compact in alias_map:
            rename_map[c] = alias_map[key_compact]
    return df.rename(columns=rename_map)

def score_section(df_cols: set, section: str, sheet_name: str) -> int:
    """
    Score likelihood that a sheet is of a given section by:
    - presence of required columns
    - optional bias if sheet name hints the section
    """
    score = len(REQUIRED[section].intersection(df_cols))
    lname = sheet_name.lower()
    if section == "cubes" and "cube" in lname:
        score += 2
    if section == "joins" and ("join" in lname or "relationship" in lname):
        score += 2
    if section == "dimensions" and ("dimension" in lname or "dim" in lname):
        score += 2
    if section == "measures" and ("measure" in lname or "metric" in lname):
        score += 2
    return score

def detect_sections(csv_path: Path, verbose: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Detect sections from a single CSV file.
    Returns four DataFrames (may be empty): cubes_df, joins_df, dims_df, measures_df.
    """
    try:
        raw = pd.read_csv(csv_path, encoding='latin1', on_bad_lines='skip')
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    raw = drop_empty_rows_and_columns(raw)
    if raw.empty:
        print(f"[detect] CSV file is empty: {csv_path}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    ndf = normalize_columns(raw)

    # Assume all columns belong to one of the four sections
    cubes_df = pd.DataFrame()
    joins_df = pd.DataFrame()
    dims_df = pd.DataFrame()
    measures_df = pd.DataFrame()

    # Identify columns for each section based on column names
    for col in ndf.columns:
        col_lower = col.lower()
        if "cube" in col_lower or "table" in col_lower:
            cubes_df[col] = ndf[col]
        elif "join" in col_lower or "relationship" in col_lower:
            joins_df[col] = ndf[col]
        elif "dimension" in col_lower or "dim" in col_lower:
            dims_df[col] = ndf[col]
        elif "measure" in col_lower or "metric" in col_lower:
            measures_df[col] = ndf[col]

    # Remap columns to canonical names
    cubes_df = remap_known_columns(cubes_df, "cubes")
    joins_df = remap_known_columns(joins_df, "joins")
    dims_df = remap_known_columns(dims_df, "dimensions")
    measures_df = remap_known_columns(measures_df, "measures")

    return cubes_df, joins_df, dims_df, measures_df

# --------------------------
# YAML building functionality
# --------------------------

def row_to_dict(row: pd.Series) -> Dict[str, object]:
    """
    Convert a pandas row to a plain dict with:
    - strings trimmed
    - NaN -> None
    """
    out: Dict[str, object] = {}
    for k, v in row.items():
        if isinstance(v, str):
            vv = clean_str(v)
        elif isinstance(v, (int, float)) and pd.isna(v):
            vv = None
        else:
            vv = v if not pd.isna(v) else None
        if vv is not None:
            out[k] = vv
    return out

def build_yaml_structure(
    cubes_df: pd.DataFrame,
    joins_df: pd.DataFrame,
    dims_df: pd.DataFrame,
    measures_df: pd.DataFrame,
    only_cube: Optional[str] = None,
    include_unknown: bool = True
) -> Dict[str, object]:
    """
    Create the final YAML-serializable data structure.
    - Includes unknown columns from each section row if include_unknown=True.
    - Filters to a specific cube by name if only_cube is provided.
    """
    result: Dict[str, object] = {}

    # 1) Cubes
    cubes: List[Dict[str, object]] = []
    name_to_table: Dict[str, str] = {}

    if not cubes_df.empty:
        # Ensure canonical columns exist even if not provided
        for _, row in cubes_df.iterrows():
            r = row_to_dict(row)
            name = clean_str(r.get("name"))
            if only_cube and name != only_cube:
                continue
            # Keep lookup for join filtering
            table_name = clean_str(r.get("table"))
            if name and table_name:
                name_to_table[name] = table_name

            cube_obj: Dict[str, object] = {}
            # Known fields
            for key in ("description", "name", "sql_table", "title"):
                val = r.get(key)
                if val is not None:
                    cube_obj[key] = val
            # Unknown/extra fields
            if include_unknown:
                for k, v in r.items():
                    if k not in cube_obj and k not in ("table",):
                        cube_obj[k] = v
            cubes.append(cube_obj)

    result["cubes"] = cubes

    # 2) Joins
    joins: List[Dict[str, object]] = []
    if not joins_df.empty:
        for _, row in joins_df.iterrows():
            r = row_to_dict(row)
            primary_table = clean_str(r.get("primary_table"))
            secondary_table = clean_str(r.get("secondary_table"))

            if only_cube:
                # Accept joins where primary table equals the cube name or the cube's base table
                allowed = {only_cube}
                if only_cube in name_to_table:
                    allowed.add(name_to_table[only_cube])
                if primary_table not in allowed:
                    continue

            relationship = clean_str(r.get("relationship"))
            pk = clean_str(r.get("primary_table_key_column"))
            sk = clean_str(r.get("secondary_table_key_column"))
            sql_expr = clean_str(r.get("sql"))

            if not sql_expr and pk and sk:
                sql_expr = f"{pk}={sk}"

            join_obj: Dict[str, object] = {}
            # Known fields
            if secondary_table is not None:
                join_obj["name"] = secondary_table
            if relationship is not None:
                join_obj["relationship"] = relationship
            if sql_expr is not None:
                join_obj["sql"] = sql_expr
            # Unknown/extra fields
            if include_unknown:
                for k, v in r.items():
                    if k not in ("primary_table", "secondary_table", "relationship", "primary_table_key_column", "secondary_table_key_column", "sql"):
                        join_obj[k] = v

            joins.append(join_obj)

    result["joins"] = joins

    # 3) Dimensions
    dimensions: List[Dict[str, object]] = []
    if not dims_df.empty:
        for _, row in dims_df.iterrows():
            r = row_to_dict(row)
            dim_obj: Dict[str, object] = {}

            # Known fields
            for key in ("name", "title", "description", "sql", "type"):
                val = r.get(key)
                if val is not None:
                    dim_obj[key] = val

            # primaryKey is optional; include only when provided or truthy
            pk_val = coerce_bool(r.get("primarykey"))
            if pk_val is not None:
                dim_obj["primaryKey"] = bool(pk_val)

            # Unknown/extra fields
            if include_unknown:
                for k, v in r.items():
                    if k not in ("name", "title", "description", "sql", "type", "primarykey"):
                        dim_obj[k] = v

            dimensions.append(dim_obj)

    result["dimensions"] = dimensions

    # 4) Measures
    measures: List[Dict[str, object]] = []
    if not measures_df.empty:
        for _, row in measures_df.iterrows():
            r = row_to_dict(row)
            meas_obj: Dict[str, object] = {}

            # Known fields
            for key in ("name", "title", "description", "sql", "type"):
                val = r.get(key)
                if val is not None:
                    meas_obj[key] = val

            # Unknown/extra fields
            if include_unknown:
                for k, v in r.items():
                    if k not in ("name", "title", "description", "sql", "type"):
                        meas_obj[k] = v

            measures.append(meas_obj)

    result["measures"] = measures

    return result

# ---------------
# Command-line app
# ---------------

def main():
    """
    CLI entry point. Example:
      python excel_to_yaml.py -i ./examples/template.xlsx -o ./output/capacity_request.yml --only-cube capacity_request --verbose
    """
    parser = argparse.ArgumentParser(description="Convert semantic template to YAML (cubes, joins, dimensions, measures).")
    parser.add_argument("--only-cube", help="If set, include only this cube by name and filter joins accordingly.")
    parser.add_argument("--no-include-unknown", action="store_true", help="Do not include unknown/extra columns in the output YAML.")
    parser.add_argument("--verbose", action="store_true", help="Print detection details.")
    args = parser.parse_args()

    input_path = Path("input/11291_v2_semantic_design_template.csv")
    output_path = Path("output/11291_output.yml")

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cubes_df, joins_df, dims_df, measures_df = detect_sections(input_path, verbose=args.verbose)

    data = build_yaml_structure(
        cubes_df,
        joins_df,
        dims_df,
        measures_df,
        only_cube=args.only_cube,
        include_unknown=(not args.no_include_unknown),
    )

    with output_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=4096)

    print(f"Wrote YAML to: {output_path}")

if __name__ == "__main__":
    main()