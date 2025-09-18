# Excel to YAML (Semantic) Utility

## Overview

The Excel to YAML (Semantic) Utility is a powerful tool designed to convert Excel templates into structured YAML files. This utility is particularly useful for data modeling and semantic design, allowing users to define cubes, joins, dimensions, and measures in an Excel format and seamlessly translate that into a YAML configuration.

## Features

This utility reads an Excel template containing the following sheets:

### 1. Cubes
- **table**: The name of the underlying table.
- **sql_table**: The SQL representation of the table.
- **name**: The name of the cube.
- **description**: A detailed description of the cube's purpose and functionality.
- **title**: The title for display purposes.

### 2. Joins
- **Primary Table**: The main table involved in the join.
- **Secondary Table**: The table that is being joined to the primary table.
- **relationship**: The nature of the relationship (e.g., one-to-many).
- **Primary Table Key Column**: The key column in the primary table.
- **Secondary Table Key Column**: The key column in the secondary table.

### 3. Dimensions
- **name**: The name of the dimension.
- **title**: A title for the dimension.
- **description**: A description detailing the dimension's role.
- **sql**: The SQL representation of the dimension.
- **primaryKey**: Indicates if the dimension is a primary key.
- **type**: The data type of the dimension.

### 4. Measures
- **name**: The name of the measure.
- **title**: A title for the measure.
- **description**: A description of the measure's purpose.
- **sql**: The SQL representation of the measure.
- **type**: The aggregation type (e.g., sum, average).

## Usage

To convert an Excel template to a YAML file, use the command line interface. Below is an example command to convert and filter to a specific cube:

```bash
python utility.py -i "input/Semantic_design_template.xlsx" -o "output/semantic_output.yml"
```

### Command-Line Options
- `-i`, `--input`: Required. Path to the input Excel file (.xlsx).
- `-o`, `--output`: Required. Path to the output YAML file (.yml).

## Requirements

This utility requires Python 3.9 or higher and the following Python packages:
- `pandas`: For data manipulation and analysis.
- `openpyxl`: For reading Excel files.
- `PyYAML`: For YAML file generation.

You can install the required packages using pip:

```bash
pip install pandas openpyxl PyYAML
```



## Current Architecture

*Last updated: 2025-09-18 15:24:00*

This repository contains semantic data models with the following components:

- **Data Cubes:** 8
- **Joins:** 8
- **Dimensions:** 4
- **Measures:** 4

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).