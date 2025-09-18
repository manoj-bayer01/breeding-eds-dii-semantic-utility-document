# Technical Specifications

## Breeding EDS DII Semantic Utility Document

### System Requirements

#### Runtime Environment
- **Python Version**: 3.9 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Memory**: Minimum 512MB RAM (recommended 1GB+ for large files)
- **Storage**: 100MB free space for installation and temporary files

#### Dependencies
- **pandas**: `>=2.2` - Data manipulation and analysis
- **openpyxl**: `>=3.1` - Excel file reading and writing
- **PyYAML**: `>=6.0` - YAML serialization and deserialization

---

## Input Specifications

### Supported File Formats
- **Excel Format**: `.xlsx` (Office Open XML)
- **Excel Version**: Excel 2007 and later
- **File Size**: Limited by available system memory
- **Encoding**: UTF-8 support for international characters

### Sheet Structure Requirements

#### Required Sheets (Auto-detected)
The utility automatically detects sheets based on column presence and naming conventions.

#### Cubes Sheet
**Required Columns:**
- `table` (string): Physical database table name
- `sql_table` (string): SQL-formatted table reference
- `name` (string): Unique cube identifier

**Optional Columns:**
- `description` (string): Detailed cube description
- `title` (string): Display-friendly cube title
- `data_source` (string): Source system identifier

**Column Aliases Supported:**
- `table_name`, `cube_table` → `table`
- `sqltable`, `sql table` → `sql_table`
- `cube_name`, `cube` → `name`
- `desc` → `description`

#### Joins Sheet
**Required Columns:**
- `primary_table` (string): Primary table in relationship
- `secondary_table` (string): Secondary table in relationship

**Optional Columns:**
- `relationship` (string): Join relationship type
- `primary_table_key_column` (string): Primary key column
- `secondary_table_key_column` (string): Foreign key column
- `sql` (string): Custom SQL join expression

**Column Aliases Supported:**
- `primary table` → `primary_table`
- `secondary table` → `secondary_table`
- `relation`, `relationship_type` → `relationship`
- `primary_table_key`, `primary key column` → `primary_table_key_column`
- `secondary_table_key`, `secondary key column` → `secondary_table_key_column`

#### Dimensions Sheet
**Required Columns:**
- `name` (string): Dimension identifier
- `sql` (string): SQL expression for dimension
- `type` (string): Data type specification

**Optional Columns:**
- `title` (string): Display title
- `description` (string): Dimension description
- `primaryKey` (boolean): Primary key indicator

**Column Aliases Supported:**
- `primary key`, `primary_key`, `is_primary_key`, `pk` → `primarykey`
- `datatype`, `data_type` → `type`

#### Measures Sheet
**Required Columns:**
- `name` (string): Measure identifier
- `sql` (string): SQL expression for measure
- `type` (string): Aggregation type

**Optional Columns:**
- `title` (string): Display title
- `description` (string): Measure description

**Column Aliases Supported:**
- `aggregation`, `aggregate`, `agg` → `type`

---

## Output Specifications

### YAML Format
- **Standard**: YAML 1.2
- **Encoding**: UTF-8
- **Indentation**: 2 spaces
- **String Quoting**: Double quotes for all strings
- **Line Width**: 4096 characters (prevents unwanted line breaks)

### Schema Structure

```yaml
cubes:
  - name: "string"
    sql_table: "string"
    title: "string"          # optional
    description: "string"    # optional, single-line formatted
    [custom_fields]: any     # when --include-unknown is used

joins:
  - name: "string"           # derived from secondary_table
    relationship: "string"   # optional
    sql: "string"           # auto-generated or custom
    [custom_fields]: any

dimensions:
  - name: "string"
    title: "string"          # optional
    description: "string"    # optional, single-line formatted
    sql: "string"
    type: "string"
    primaryKey: boolean      # optional, only when true
    [custom_fields]: any

measures:
  - name: "string"
    title: "string"          # optional
    description: "string"    # optional, single-line formatted
    sql: "string"
    type: "string"
    [custom_fields]: any
```

---

## Processing Specifications

### Data Cleaning Rules

#### String Processing
1. **Trimming**: Leading and trailing whitespace removed
2. **Quote Removal**: Outer single/double quotes stripped recursively
3. **Empty Handling**: Empty strings converted to null
4. **Multiline**: Descriptions converted to single-line format

#### Boolean Conversion
**Truthy Values**: `true`, `1`, `yes`, `y`, `t` (case-insensitive)
**Falsy Values**: `false`, `0`, `no`, `n`, `f` (case-insensitive)
**Null Values**: Empty, whitespace-only, or pandas NaN

#### Column Normalization
1. **Case**: Convert to lowercase
2. **Spaces**: Replace with underscores
3. **Deduplication**: Append `_2`, `_3` for duplicates
4. **Trimming**: Remove leading/trailing whitespace

### Sheet Detection Algorithm

#### Scoring System
Each sheet is scored for each section type based on:
- **Required Column Match**: +1 point per required column found
- **Sheet Name Hints**: +2 points for relevant keywords in sheet name
  - "cube" → cubes section
  - "join" or "relationship" → joins section
  - "dimension" or "dim" → dimensions section
  - "measure" or "metric" → measures section

#### Classification Threshold
- **Minimum Score**: 2 points required for classification
- **Best Match**: Highest scoring section type wins
- **Tie Breaking**: First match in order (cubes, joins, dimensions, measures)

### Join SQL Generation
When `sql` column is not provided:
```sql
{primary_table_key_column}={secondary_table_key_column}
```

---

## Performance Specifications

### Memory Usage
- **Base Overhead**: ~50MB for Python runtime and libraries
- **Per Sheet**: ~2-5MB per 1000 rows depending on data complexity
- **Peak Usage**: 2-3x file size during processing

### Processing Speed
- **Small Files** (<1MB): <1 second
- **Medium Files** (1-10MB): 1-5 seconds
- **Large Files** (10-100MB): 5-30 seconds
- **Very Large Files** (>100MB): May require memory optimization

### File Size Limits
- **Practical Limit**: 500MB (depends on available RAM)
- **Row Limit**: ~1 million rows per sheet
- **Column Limit**: 16,384 columns (Excel limit)

---

## Error Handling Specifications

### Input Validation Errors
```
FileNotFoundError: Input file not found
PermissionError: Cannot read input file
ValueError: Invalid Excel format
UnicodeError: File encoding issues
```

### Processing Errors
```
EmptyDataError: No recognizable sections found
ValidationError: Required columns missing
TypeError: Invalid data type in cell
MemoryError: File too large for available memory
```

### Output Errors
```
PermissionError: Cannot write to output location
OSError: Disk space insufficient
UnicodeError: Cannot encode characters to UTF-8
```

### Error Recovery
- **Graceful Degradation**: Continue processing valid sheets
- **Informative Messages**: Clear error descriptions with context
- **Exit Codes**: Standard POSIX exit codes (0=success, 1=error)

---

## Command Line Interface Specifications

### Syntax
```bash
python utility.py -i INPUT -o OUTPUT [OPTIONS]
```

### Arguments

#### Required Arguments
- `-i, --input PATH`: Input Excel file path
  - **Format**: File system path (absolute or relative)
  - **Validation**: File existence, read permissions, .xlsx extension
  
- `-o, --output PATH`: Output YAML file path
  - **Format**: File system path (absolute or relative)
  - **Validation**: Directory existence, write permissions
  - **Auto-creation**: Parent directories created if needed

#### Optional Arguments
- `--only-cube NAME`: Filter to specific cube
  - **Format**: String matching cube name exactly
  - **Effect**: Includes only matching cube and related joins
  
- `--no-include-unknown`: Exclude unknown columns
  - **Default**: Include unknown columns in output
  - **Effect**: Only known schema columns in output
  
- `--verbose`: Enable detailed logging
  - **Default**: Minimal output
  - **Effect**: Shows sheet detection details and processing steps

### Exit Codes
- `0`: Success
- `1`: General error (file not found, processing failed)
- `2`: Invalid arguments

---

## Security Specifications

### File System Security
- **Path Traversal**: No protection (relies on OS permissions)
- **File Permissions**: Respects system file permissions
- **Temporary Files**: None created during processing

### Data Security
- **Local Processing**: All processing performed locally
- **No Network**: No external network connections
- **Memory Cleanup**: DataFrames garbage collected after use

### Input Validation
- **File Format**: Validates Excel format before processing
- **Content Validation**: Checks for required columns and data types
- **Size Limits**: Limited by available system memory

---

## Integration Specifications

### API Compatibility (Future)
Current CLI interface supports future API integration:

```python
# Planned API usage
from utility import process_excel_to_yaml

result = process_excel_to_yaml(
    input_path="template.xlsx",
    output_path="output.yml",
    only_cube="capacity_request",
    include_unknown=True,
    verbose=False
)
```

### CI/CD Integration
- **Docker Support**: Can be containerized
- **Batch Processing**: Supports scripted execution
- **Exit Codes**: Standard for automated testing

### Version Control
- **Text Output**: YAML format is VCS-friendly
- **Deterministic**: Same input produces same output
- **Diff-Friendly**: Changes are human-readable

---

## Quality Assurance Specifications

### Input Validation
- **File Format**: Excel format verification
- **Sheet Structure**: Required column presence
- **Data Types**: Type validation where applicable
- **Character Encoding**: UTF-8 compatibility check

### Output Validation
- **YAML Syntax**: Valid YAML 1.2 format
- **Schema Compliance**: Matches expected structure
- **Character Encoding**: UTF-8 output encoding
- **File Integrity**: Complete file write verification

### Testing Approach
- **Unit Testing**: Individual function validation
- **Integration Testing**: End-to-end workflow testing
- **Edge Cases**: Empty files, malformed data, large files
- **Regression Testing**: Consistent output across versions

---

## Monitoring Specifications

### Logging Levels
- **Default**: Minimal output (errors and success message)
- **Verbose**: Detailed processing information
- **Debug**: Internal state and decision points (future)

### Metrics Collection
- **Processing Time**: Start to finish execution time
- **Memory Usage**: Peak memory consumption
- **File Statistics**: Input size, sheet count, row counts
- **Error Rates**: Failed processing attempts

### Health Checks
- **Dependency Check**: Verify required libraries
- **Permission Check**: File system access validation
- **Memory Check**: Available system memory
- **Disk Space**: Available storage for output

---

## Maintenance Specifications

### Code Quality Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Function signatures with type annotations
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Explicit exception handling

### Testing Requirements
- **Coverage**: Minimum 80% code coverage
- **Edge Cases**: Boundary condition testing
- **Performance**: Load testing with large files
- **Compatibility**: Multi-platform testing

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Backward Compatibility**: Maintain Excel template support
- **Change Log**: Documented changes between versions
- **Migration Guide**: Upgrade instructions when needed

---

## Future Enhancements

### Planned Features
1. **Batch Processing**: Multiple file processing
2. **Template Validation**: Pre-processing validation
3. **Custom Output Formats**: JSON, XML support
4. **Web Interface**: Browser-based conversion
5. **API Endpoints**: REST API for remote processing

### Architecture Evolution
1. **Microservices**: Decomposition into smaller services
2. **Database Integration**: Direct database connectivity
3. **Cloud Deployment**: Container orchestration support
4. **Streaming**: Large file streaming capabilities
5. **Plugin System**: Extensible processing pipeline

### Performance Optimization
1. **Parallel Processing**: Multi-threaded sheet processing
2. **Memory Optimization**: Streaming for large files
3. **Caching**: Intermediate result caching
4. **Compression**: Output file compression options

---

This technical specification provides the detailed implementation requirements and constraints for the Breeding EDS DII Semantic Utility Document system.