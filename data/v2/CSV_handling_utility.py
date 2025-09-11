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

def score_section(df_cols: set, section: str, hint_name: str) -> int:
    """
    Score likelihood that a CSV is of a given section by:
    - presence of required columns
    - optional bias if file/folder name hints the section
    """
    score = len(REQUIRED[section].intersection(df_cols))
    lname = hint_name.lower()
    if section == "cubes" and "cube" in lname:
        score += 2
    if section == "joins" and ("join" in lname or "relationship" in lname):
        score += 2
    if section == "dimensions" and ("dimension" in lname or "dim" in lname):
        score += 2
    if section == "measures" and ("measure" in lname or "metric" in lname):
        score += 2
    return score

# --------------------------
# CSV reading and detection
# --------------------------

def read_csv_safely(csv_path: Path) -> pd.DataFrame:
    """
    Read CSV with robust defaults:
    - auto-detect delimiter
    - handle UTF-8 + BOM
    - keep as object to preserve formatting
    """
    df = pd.read_csv(
        csv_path,
        sep=None,           # auto-detect delimiter
        engine="python",    # needed for sep=None
        dtype=object,       # keep everything as object; we'll clean/convert later
        encoding="utf-8-sig",
        keep_default_na=True,
    )
    return df

def detect_csv_sections(input_path: Path, verbose: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Detect and load sections from CSV input.
    - If input is a directory: look for cubes.csv, joins.csv, dimensions.csv, measures.csv.
    - If input is a CSV file: detect which section it represents based on headers and filename hints.
    Returns four DataFrames (may be empty): cubes_df, joins_df, dims_df, measures_df.
    """
    cubes_df_list: List[pd.DataFrame] = []
    joins_df_list: List[pd.DataFrame] = []
    dims_df_list: List[pd.DataFrame] = []
    measures_df_list: List[pd.DataFrame] = []

    if input_path.is_dir():
        # Directory mode: look for known filenames
        for section, filename in [
            ("cubes", "cubes.csv"),
            ("joins", "joins.csv"),
            ("dimensions", "dimensions.csv"),
            ("measures", "measures.csv"),
        ]:
            path = input_path / filename
            if not path.exists():
                if verbose:
                    print(f"[detect] {filename} not found in {input_path}, skipping.")
                continue
            raw = read_csv_safely(path)
            raw = drop_empty_rows_and_columns(raw)
            if raw.empty:
                if verbose:
                    print(f"[detect] {filename} is empty after cleanup, skipping.")
                continue
            ndf = normalize_columns(raw)
            remapped = remap_known_columns(ndf, section)
            if section == "cubes":
                cubes_df_list.append(remapped)
            elif section == "joins":
                joins_df_list.append(remapped)
            elif section == "dimensions":
                dims_df_list.append(remapped)
            elif section == "measures":
                measures_df_list.append(remapped)
            if verbose:
                print(f"[detect] Loaded {filename} as {section} with {len(remapped)} rows.")
    elif input_path.is_file():
        # Single CSV file: auto-detect which section
        raw = read_csv_safely(input_path)
        raw = drop_empty_rows_and_columns(raw)
        if raw.empty:
            if verbose:
                print(f"[detect] {input_path.name} is empty after cleanup.")
        else:
            ndf = normalize_columns(raw)
            best_section = None
            best_score = -1
            candidates: Dict[str, pd.DataFrame] = {}
            for section in ("cubes", "joins", "dimensions", "measures"):
                remapped = remap_known_columns(ndf, section)
                candidates[section] = remapped
                sc = score_section(set(remapped.columns), section, input_path.stem)
                if sc > best_score:
                    best_score = sc
                    best_section = section
            if best_section and best_score >= 2:
                if verbose:
                    print(f"[detect] File '{input_path.name}' => {best_section} (score={best_score})")
                chosen = candidates[best_section]
                if best_section == "cubes":
                    cubes_df_list.append(chosen)
                elif best_section == "joins":
                    joins_df_list.append(chosen)
                elif best_section == "dimensions":
                    dims_df_list.append(chosen)
                elif best_section == "measures":
                    measures_df_list.append(chosen)
            else:
                if verbose:
                    print(f"[detect] Could not confidently classify '{input_path.name}' (score={best_score}).")
    else:
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    cubes_df = pd.concat(cubes_df_list, ignore_index=True) if cubes_df_list else pd.DataFrame()
    joins_df = pd.concat(joins_df_list, ignore_index=True) if joins_df_list else pd.DataFrame()
    dims_df = pd.concat(dims_df_list, ignore_index=True) if dims_df_list else pd.DataFrame()
    measures_df = pd.concat(measures_df_list, ignore_index=True) if measures_df_list else pd.DataFrame()
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
    - Dynamically reflects any additions, updates, or deletions present in the source CSVs,
      because the YAML is built fresh from current CSV content each run.
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
      - Directory input with four CSVs:
        python utility.py -i ./examples/capacity_request -o ./output/capacity_request.yml --only-cube capacity_request --verbose
      - Single CSV input to auto-detect section:
        python utility.py -i ./examples/dimensions.csv -o ./output/dimensions.yml --verbose
    """
    parser = argparse.ArgumentParser(description="Convert CSV-based semantic template to YAML (cubes, joins, dimensions, measures). Accepts a folder containing cubes.csv/joins.csv/dimensions.csv/measures.csv, or a single CSV file.")
    parser.add_argument("-i", "--input", required=True, help="Path to input folder or CSV file")
    parser.add_argument("-o", "--output", required=True, help="Path to output YAML file (.yml)")
    parser.add_argument("--only-cube", help="If set, include only this cube by name and filter joins accordingly.")
    parser.add_argument("--no-include-unknown", action="store_true", help="Do not include unknown/extra columns in the output YAML.")
    parser.add_argument("--verbose", action="store_true", help="Print detection details.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cubes_df, joins_df, dims_df, measures_df = detect_csv_sections(input_path, verbose=args.verbose)
    if cubes_df.empty and joins_df.empty and dims_df.empty and measures_df.empty:
        print("Error: No recognizable data found. Check your CSV headers or use --verbose to see detection details.", file=sys.stderr)
        sys.exit(1)

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