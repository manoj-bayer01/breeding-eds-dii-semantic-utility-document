# Architecture Documentation

## Breeding EDS DII Semantic Utility Document

### Project Overview

The **Breeding EDS DII Semantic Utility Document** is a Python-based data transformation utility designed to convert Excel templates containing semantic data models into structured YAML configurations. This tool facilitates the creation of business intelligence (BI) cubes, joins, dimensions, and measures from Excel-based data definitions, making it easier to maintain and deploy semantic data models in analytical systems.

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Excel Input   │───▶│  Semantic Utility │───▶│  YAML Output    │
│   (.xlsx)       │    │   (utility.py)    │    │   (.yml)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ • Cubes Sheet   │    │ • Column         │    │ • Structured    │
│ • Joins Sheet   │    │   Detection      │    │   YAML Schema   │
│ • Dimensions    │    │ • Data           │    │ • Ready for BI  │
│ • Measures      │    │   Validation     │    │   Integration   │
└─────────────────┘    │ • YAML Generation│    └─────────────────┘
                       └──────────────────┘
```

### Component Architecture

The system is built around a modular architecture with the following core components:

#### 1. Data Input Layer
- **Excel Reader**: Processes `.xlsx` files using `openpyxl` engine
- **Sheet Detection**: Automatically identifies cubes, joins, dimensions, and measures sheets
- **Column Normalization**: Standardizes header names and handles aliases

#### 2. Data Processing Layer
- **Data Cleaning**: Removes empty rows/columns, trims whitespace, handles quotes
- **Schema Validation**: Ensures required columns are present for each data type
- **Type Coercion**: Converts data types (strings, booleans, numbers)

#### 3. Business Logic Layer
- **Cube Builder**: Constructs cube definitions with metadata
- **Join Builder**: Creates relationship definitions between tables
- **Dimension Builder**: Generates dimension specifications
- **Measure Builder**: Defines aggregation measures

#### 4. Output Layer
- **YAML Serializer**: Converts processed data to YAML format
- **Custom Dumper**: Ensures consistent string formatting and structure

---

## Detailed Component Design

### Core Modules

#### 1. Data Utilities (`clean_str`, `coerce_bool`, `strip_outer_quotes`)
**Purpose**: Handle data cleaning and type conversion
- Removes outer quotes from values
- Handles null/empty value detection
- Converts various boolean representations

#### 2. DataFrame Processing (`drop_empty_rows_and_columns`, `normalize_columns`)
**Purpose**: Standardize and clean Excel data
- Removes completely empty rows/columns
- Normalizes column names to snake_case
- De-duplicates column names

#### 3. Sheet Detection System (`detect_sections`, `score_section`)
**Purpose**: Automatically identify sheet types
- Uses column presence scoring
- Considers sheet naming conventions
- Handles multiple sheets of the same type

#### 4. Schema Mapping (`ALIASES`, `remap_known_columns`)
**Purpose**: Handle variations in column naming
- Maps common synonyms to canonical names
- Supports different naming conventions
- Extensible alias system

#### 5. YAML Builder (`build_yaml_structure`)
**Purpose**: Convert processed data to target schema
- Maintains relationships between cubes and joins
- Handles filtering by cube name
- Preserves unknown columns when requested

---

## Data Flow Architecture

### Processing Pipeline

```
1. Input Validation
   ├── File existence check
   ├── Excel format validation
   └── Permission validation

2. Sheet Discovery
   ├── Read all sheets
   ├── Drop empty content
   ├── Normalize headers
   └── Score sheet types

3. Data Processing
   ├── Apply column aliases
   ├── Clean data values
   ├── Validate required fields
   └── Type conversion

4. Schema Building
   ├── Build cubes structure
   ├── Create joins with relationships
   ├── Define dimensions
   └── Configure measures

5. Output Generation
   ├── Apply filtering (if specified)
   ├── Serialize to YAML
   ├── Write to file
   └── Validation
```

### Data Transformation Flow

```
Excel Sheets ──┐
               │
               ├─── Column Detection ──┐
               │                       │
               ├─── Data Cleaning ─────┼─── Schema Validation
               │                       │
               └─── Type Conversion ────┘
                                       │
                                       ▼
                              YAML Structure Building
                                       │
                                       ▼
                              Output Serialization
```

---

## Schema Architecture

### Input Schema (Excel)

#### Cubes Sheet
| Column | Type | Required | Description |
|--------|------|----------|-------------|
| table | string | Yes | Physical table name |
| sql_table | string | Yes | SQL table reference |
| name | string | Yes | Cube identifier |
| description | string | No | Cube description |
| title | string | No | Display title |
| data_source | string | No | Source system |

#### Joins Sheet
| Column | Type | Required | Description |
|--------|------|----------|-------------|
| primary_table | string | Yes | Primary table name |
| secondary_table | string | Yes | Secondary table name |
| relationship | string | No | Join relationship type |
| primary_table_key_column | string | No | Primary key column |
| secondary_table_key_column | string | No | Foreign key column |

#### Dimensions Sheet
| Column | Type | Required | Description |
|--------|------|----------|-------------|
| name | string | Yes | Dimension name |
| sql | string | Yes | SQL expression |
| type | string | Yes | Data type |
| title | string | No | Display title |
| description | string | No | Description |
| primaryKey | boolean | No | Primary key flag |

#### Measures Sheet
| Column | Type | Required | Description |
|--------|------|----------|-------------|
| name | string | Yes | Measure name |
| sql | string | Yes | SQL expression |
| type | string | Yes | Aggregation type |
| title | string | No | Display title |
| description | string | No | Description |

### Output Schema (YAML)

```yaml
cubes:
  - name: string
    sql_table: string
    title: string
    description: string
    [additional_fields]: any

joins:
  - name: string
    relationship: string
    sql: string
    [additional_fields]: any

dimensions:
  - name: string
    title: string
    description: string
    sql: string
    type: string
    primaryKey: boolean
    [additional_fields]: any

measures:
  - name: string
    title: string
    description: string
    sql: string
    type: string
    [additional_fields]: any
```

---

## Configuration Architecture

### Command Line Interface

The utility supports the following configuration options:

```bash
python utility.py [OPTIONS]

Required Arguments:
  -i, --input PATH       Path to input Excel file (.xlsx)
  -o, --output PATH      Path to output YAML file (.yml)

Optional Arguments:
  --only-cube NAME       Filter to specific cube by name
  --no-include-unknown   Exclude unknown columns from output
  --verbose              Enable detailed logging
```

### Environment Configuration

The system uses the following environment setup:

- **Python Version**: 3.9+
- **Dependencies**: pandas>=2.2, openpyxl>=3.1, PyYAML>=6.0
- **File Encoding**: UTF-8
- **Memory Requirements**: Depends on Excel file size

---

## Deployment Architecture

### File Structure

```
breeding-eds-dii-semantic-utility-document/
├── utility.py              # Main application
├── requirements.txt         # Python dependencies
├── README.md               # User documentation
├── ARCHITECTURE.md         # This document
├── input/                  # Input Excel files
│   └── Semantic_design_template.xlsx
├── output/                 # Generated YAML files
│   └── semantic_output.yml
├── logs/                   # Application logs
│   └── log.md
└── data/                   # Version history
    ├── v1/
    ├── v2/
    ├── v3/
    ├── v4/
    └── v5/
```

### Execution Model

1. **Standalone Application**: Runs as command-line utility
2. **No External Services**: Self-contained processing
3. **File-based I/O**: Reads Excel, writes YAML
4. **Error Handling**: Graceful failure with informative messages

---

## Security Architecture

### Data Security
- **Local Processing**: No data transmitted over network
- **File Permissions**: Respects system file permissions
- **Input Validation**: Validates file formats and content

### Access Control
- **File System**: Uses standard OS file permissions
- **No Authentication**: Command-line utility requires no authentication
- **Audit Trail**: Optional verbose logging for processing details

---

## Performance Architecture

### Scalability Considerations

#### Memory Usage
- **Streaming Processing**: Processes sheets individually
- **Garbage Collection**: Cleans up DataFrames after processing
- **Memory Efficiency**: Uses pandas for optimized data operations

#### Processing Speed
- **Single-threaded**: Simple linear processing model
- **Optimized Libraries**: Uses optimized pandas operations
- **Minimal I/O**: Single read, single write operations

#### File Size Limits
- **Excel Limitations**: Bound by openpyxl library limits
- **Memory Constraints**: System RAM determines maximum file size
- **Performance Degradation**: Linear with file size

---

## Integration Architecture

### Input Integration
- **Excel Compatibility**: Supports Excel 2007+ (.xlsx format)
- **Template Flexibility**: Handles various column naming conventions
- **Multi-sheet Support**: Processes multiple sheets automatically

### Output Integration
- **YAML Standard**: Produces standard YAML 1.2 format
- **BI Tool Ready**: Compatible with common BI platforms
- **Version Control**: Text-based output supports version control

### API Considerations (Future)
While currently a CLI tool, the architecture supports future API integration:
- **Modular Design**: Core logic separated from CLI interface
- **Function-based**: Main processing functions are reusable
- **Configuration**: Supports programmatic configuration

---

## Monitoring and Logging

### Logging Architecture
- **Verbose Mode**: Detailed processing information
- **Error Reporting**: Clear error messages for troubleshooting
- **Progress Tracking**: Sheet detection and processing status

### Quality Assurance
- **Data Validation**: Ensures required fields are present
- **Format Checking**: Validates Excel structure
- **Output Verification**: Confirms YAML generation success

---

## Maintenance Architecture

### Code Organization
- **Single File**: All logic in utility.py for simplicity
- **Functional Design**: Pure functions for testability
- **Clear Separation**: Distinct phases for each processing step

### Extensibility
- **Alias System**: Easy addition of new column aliases
- **Custom Dumper**: Configurable YAML output formatting
- **Plugin Potential**: Architecture supports future plugin system

### Version Management
- **Requirements Lock**: Specific version dependencies
- **Backward Compatibility**: Maintains existing Excel template support
- **Change Log**: Version history in data/ directory

---

## Future Architecture Considerations

### Planned Enhancements
1. **Web Interface**: Browser-based file upload and conversion
2. **API Endpoints**: REST API for programmatic access
3. **Batch Processing**: Multiple file processing capabilities
4. **Template Validation**: Pre-processing template validation
5. **Custom Output Formats**: JSON, XML output options

### Scalability Roadmap
1. **Microservices**: Break into smaller, focused services
2. **Database Integration**: Direct database connectivity
3. **Cloud Deployment**: Container-based cloud deployment
4. **Streaming Processing**: Large file streaming capabilities

---

## Conclusion

The Breeding EDS DII Semantic Utility Document represents a focused, efficient solution for converting Excel-based semantic models to YAML configurations. Its modular architecture, robust data processing pipeline, and flexible configuration options make it suitable for both ad-hoc conversions and integration into larger data processing workflows.

The architecture prioritizes:
- **Simplicity**: Easy to understand and maintain
- **Reliability**: Robust error handling and validation
- **Flexibility**: Handles various input formats and naming conventions
- **Extensibility**: Supports future enhancements and integrations

This foundation provides a solid base for future enhancements while maintaining the tool's core value proposition of simple, reliable Excel-to-YAML conversion for semantic data models.