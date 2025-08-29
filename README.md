Excel to YAML (Semantic) Utility

This utility reads an Excel template with sheets for:
- Cubes: table, sql_table, name, description, title
- Joins: Primary Table, Secondary Table, relationship, Primary Table Key Column, Secondary Table Key Column
- Dimensions: name, title, description, sql, primaryKey, type
- Measures: name, title, description, sql, type

Usage:
- Convert and filter to one cube (recommended):
  python excel_to_yaml.py -i "examples/2rough_semantic_design_template - Copy - Copy.xlsx" -o output/capacity_request.yml --only-cube capacity_request

Requires Python 3.9+, pandas, openpyxl, PyYAML.