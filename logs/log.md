# Project Log: Semantic Utility

### Overview
This log documents the development and progress of the Excel to YAML (Semantic) Utility project. The utility converts Excel templates into structured YAML files for data modeling and semantic design.


## Auto-Documentation Update - 2025-09-18 09:18:46

### Processing Summary
Processed 1 semantic file(s):
  - semantic_output: 2 cubes, 2 joins, 1 dimensions, 1 measures

### Documentation Generated
- ARCHITECTURE.md
- CHANGES.md
- CUBES.md
- DATA_LINEAGE.md
- DIMENSIONS.md
- JOINS.md
- MEASURES.md
- SUMMARY.md

---

## Log Entries

#
- **Initial Setup**
  - Created the project repository.
  - Set up the development environment with Python 3.9+.
  - Installed required packages: `pandas`, `openpyxl`, `PyYAML`.

#
- **Feature Implementation**
  - Developed core functionality to read Excel files using `pandas`.
  - Implemented normalization of column names to ensure consistency across different sheets.
  - Created functions to handle cubes, joins, dimensions, and measures.

#
- **YAML Generation**
  - Implemented logic to convert the structured data into YAML format.
  - Ensured proper indentation and formatting for readability.
  - Added functionality to handle optional parameters for filtering cubes.

#
- **Command-Line Interface**
  - Developed a command-line interface (CLI) using `argparse` for user interaction.
  - Added options for input and output file paths, filtering by cube, and verbose output.

#
- **Testing and Validation**
  - Validated the output YAML files against sample input Excel templates.
  - Fixed issues related to formatting and unnecessary spaces in descriptions.

#
- **Documentation**
  - Created a README file detailing the utility's features, usage, and installation instructions.
  - Documented the structure of the Excel template and the expected output format.

#
- **Final Review**
  - Reviewed the code for optimization and readability.
  - Ensured all features are functioning correctly and documentation is complete.
  - Prepared for project handoff or deployment.

---

## Example Output

The generated YAML file from the utility currently looks like this:

```yaml
cubes:
- description: Capacity Request in Velocity is a workflow designed to enable researchers to request space for experimental or seed production workflows in Open Fields, Controlled Environments, and Labs across Bayer's Crop Science business units. It offers various functionalities, including creating new requests, saving requests in draft mode, and checking the status of existing requests. It stores information for all the capacity requests.
  name: capacity_request
  sql_table: '`bcs-breeding-datasets.velocity.capacity_request`'
  title: Capacity Request
  data_source: Breeding
- description: abc2
  name: capacity_request2
  sql_table: '`bcs-breeding-datasets.velocity.capacity_request2`'
  title: Capacity Request2
  data_source: Breeding2
joins:
- name: experiment_sets_entries
  relationship: one_to_many
  sql: '{CUBE.capacity_request_id}={experiment_sets_entries.capacity_request_id}'
- name: experiment_sets_entries2
  relationship: one_to_many
  sql: '{CUBE.capacity_request_id2}={experiment_sets_entries.capacity_request_id2}'
dimensions:
- name: capacity_request_id
  title: Capacity Request ID
  description: The Capacity Request ID in Velocity is a unique identifier assigned to each capacity request made within the Capacity Request workflow in the Velocity application This ID helps users track and manage their requests effectively throughout the process.
  sql: '{CUBE}.capacity_request_id'
  type: number
  primaryKey: true
- name: capacity_request_id2
  title: Capacity Request ID2
  description: abc2
  sql: '{CUBE}.capacity_request_name'
  type: boolean
  primaryKey: true
measures:
- name: sum_of_total_sq_ft
  title: Sum of Total Sq Ft
  description: This is to get sum of total Sq Feet recorded in the velocity application
  sql: '{CUBE}.total_sq_ft'
  type: sum
```

---

## Next Steps
- Gather user feedback on the utility.
- Plan for future enhancements based on user requirements.
- Consider adding support for additional output formats (e.g., JSON).

---

## Notes
- Ensure to regularly update this log with new developments, issues encountered, and resolutions.
- Keep track of any changes made to the requirements or scope of the project.

---