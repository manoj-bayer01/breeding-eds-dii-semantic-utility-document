# Documentation Index

## Breeding EDS DII Semantic Utility Document

Welcome to the comprehensive documentation for the Excel to YAML Semantic Utility. This index provides quick access to all documentation resources.

---

## Quick Start
- **[README.md](../README.md)** - Project overview, features, and basic usage
- **[Installation](../README.md#requirements)** - Dependencies and setup instructions
- **[Basic Usage](../README.md#usage)** - Command-line examples and options

---

## Architecture Documentation

### System Design
- **[Architecture Overview](../ARCHITECTURE.md)** - Complete system architecture documentation
- **[Architecture Diagrams](architecture-diagrams.md)** - Visual system diagrams and data flow
- **[Technical Specifications](technical-specifications.md)** - Detailed technical requirements and constraints

### Key Architecture Topics
- [High-Level Architecture](../ARCHITECTURE.md#system-architecture)
- [Component Design](../ARCHITECTURE.md#detailed-component-design)
- [Data Flow](../ARCHITECTURE.md#data-flow-architecture)
- [Schema Architecture](../ARCHITECTURE.md#schema-architecture)
- [Security Architecture](../ARCHITECTURE.md#security-architecture)
- [Performance Architecture](../ARCHITECTURE.md#performance-architecture)

---

## Operational Documentation

### Deployment
- **[Deployment Guide](deployment-guide.md)** - Complete deployment instructions
- [Installation Methods](deployment-guide.md#installation-methods)
- [Environment Configuration](deployment-guide.md#environment-configuration)
- [Deployment Scenarios](deployment-guide.md#deployment-scenarios)
- [Security Configuration](deployment-guide.md#security-configuration)

### Operations
- [Monitoring and Logging](deployment-guide.md#monitoring-and-logging)
- [Troubleshooting](deployment-guide.md#troubleshooting)
- [Backup and Recovery](deployment-guide.md#backup-and-recovery)
- [Maintenance Procedures](deployment-guide.md#maintenance-procedures)

---

## Technical Reference

### Specifications
- [System Requirements](technical-specifications.md#system-requirements)
- [Input Specifications](technical-specifications.md#input-specifications)
- [Output Specifications](technical-specifications.md#output-specifications)
- [Processing Specifications](technical-specifications.md#processing-specifications)
- [Performance Specifications](technical-specifications.md#performance-specifications)

### API Reference
- [Command Line Interface](technical-specifications.md#command-line-interface-specifications)
- [Error Handling](technical-specifications.md#error-handling-specifications)
- [Integration Specifications](technical-specifications.md#integration-specifications)

---

## User Guides

### Basic Usage
- [Getting Started](../README.md#usage)
- [Excel Template Structure](../README.md#features)
- [Command Line Options](../README.md#command-line-options)

### Advanced Usage
- [Filtering by Cube](technical-specifications.md#command-line-interface-specifications)
- [Custom Column Handling](technical-specifications.md#sheet-structure-requirements)
- [Verbose Output](deployment-guide.md#debug-mode)
- [Batch Processing](deployment-guide.md#scenario-2-serverbatch-processing)

### Data Modeling
- [Cubes Definition](../README.md#1-cubes)
- [Joins Configuration](../README.md#2-joins)
- [Dimensions Setup](../README.md#3-dimensions)
- [Measures Definition](../README.md#4-measures)

---

## Development Documentation

### Code Organization
- [Component Architecture](../ARCHITECTURE.md#detailed-component-design)
- [Processing Pipeline](../ARCHITECTURE.md#data-flow-architecture)
- [Module Structure](technical-specifications.md#processing-specifications)

### Quality Assurance
- [Testing Approach](technical-specifications.md#quality-assurance-specifications)
- [Code Quality Standards](technical-specifications.md#maintenance-specifications)
- [Performance Testing](deployment-guide.md#performance-monitoring)

### Future Development
- [Planned Enhancements](../ARCHITECTURE.md#future-architecture-considerations)
- [Extensibility](../ARCHITECTURE.md#maintenance-architecture)
- [Integration Roadmap](technical-specifications.md#future-enhancements)

---

## Troubleshooting Resources

### Common Issues
- [Installation Problems](deployment-guide.md#common-issues)
- [Processing Errors](deployment-guide.md#common-issues)
- [File Format Issues](deployment-guide.md#common-issues)
- [Performance Problems](deployment-guide.md#performance-tuning)

### Diagnostic Tools
- [Debug Mode](deployment-guide.md#debug-mode)
- [Health Checks](deployment-guide.md#health-check-script)
- [Performance Monitoring](deployment-guide.md#performance-monitoring)
- [Log Analysis](deployment-guide.md#log-configuration)

---

## Examples and Samples

### Input Examples
- **[Sample Template](../input/Semantic_design_template.xlsx)** - Reference Excel template
- [Sheet Structure Examples](technical-specifications.md#sheet-structure-requirements)
- [Column Naming Conventions](technical-specifications.md#column-aliases-supported)

### Output Examples
- **[Sample Output](../output/semantic_output.yml)** - Reference YAML output
- [Schema Examples](technical-specifications.md#schema-structure)
- [Processing Results](../logs/log.md)

### Command Examples
```bash
# Basic conversion
python utility.py -i input/template.xlsx -o output/result.yml

# Filtered conversion
python utility.py -i input/template.xlsx -o output/result.yml --only-cube my_cube

# Verbose processing
python utility.py -i input/template.xlsx -o output/result.yml --verbose

# Exclude unknown columns
python utility.py -i input/template.xlsx -o output/result.yml --no-include-unknown
```

---

## Integration Guides

### CI/CD Integration
- [GitHub Actions](deployment-guide.md#github-actions-example)
- [Jenkins Pipeline](deployment-guide.md#jenkins-pipeline-example)
- [Automated Processing](deployment-guide.md#batch-script-example)

### Environment Integration
- [Local Development](deployment-guide.md#scenario-1-local-desktop-usage)
- [Server Deployment](deployment-guide.md#scenario-2-serverbatch-processing)
- [Container Deployment](deployment-guide.md#method-3-docker-installation-future)

---

## Version History

### Current Version
- **Features**: Excel to YAML conversion, auto-detection, filtering
- **Dependencies**: pandas>=2.2, openpyxl>=3.1, PyYAML>=6.0
- **Python Support**: 3.9+

### Version Evolution
- **[v1](../data/v1/)** - Initial implementation
- **[v2](../data/v2/)** - Enhanced processing
- **[v3](../data/v3/)** - Clean output format
- **[v4](../data/v4/)** - Dynamic value handling
- **[v5](../data/v5/)** - Update/delete scenarios

### Change Management
- [Release Notes](../logs/log.md)
- [Migration Guide](technical-specifications.md#version-management)
- [Compatibility Matrix](technical-specifications.md#future-enhancements)

---

## Support Resources

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/manoj-bayer01/breeding-eds-dii-semantic-utility-document/issues)
- **Discussions**: Repository discussions
- **Documentation**: This documentation set
- **Community**: User forums and communities

### Contributing
- **Bug Reports**: Issue tracker with detailed reproduction steps
- **Feature Requests**: Enhancement proposals with use cases
- **Documentation**: Improvements and clarifications
- **Code Contributions**: Pull requests with tests

### Professional Support
- **Technical Consulting**: Architecture and integration guidance
- **Custom Development**: Feature development and customization
- **Training**: User and administrator training programs
- **Maintenance**: Ongoing support and updates

---

## Related Resources

### External Documentation
- **[pandas Documentation](https://pandas.pydata.org/docs/)** - Data manipulation library
- **[openpyxl Documentation](https://openpyxl.readthedocs.io/)** - Excel file handling
- **[PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)** - YAML processing

### Standards and Specifications
- **[YAML 1.2 Specification](https://yaml.org/spec/1.2/spec.html)** - YAML format standard
- **[Excel File Format](https://docs.microsoft.com/en-us/openspecs/office_file_formats/)** - Microsoft Excel specifications
- **[Python PEP 8](https://www.python.org/dev/peps/pep-0008/)** - Python style guide

### Tools and Utilities
- **[YAML Validators](https://yamlchecker.com/)** - Online YAML syntax checking
- **[Excel Viewers](https://products.office.com/excel)** - Microsoft Excel alternatives
- **[Git](https://git-scm.com/)** - Version control system

---

## Feedback and Improvement

### Documentation Feedback
We welcome feedback on this documentation. Please report:
- Unclear explanations or missing information
- Broken links or outdated content
- Suggestions for additional topics
- Examples that would be helpful

### Contact Information
- **Repository**: [breeding-eds-dii-semantic-utility-document](https://github.com/manoj-bayer01/breeding-eds-dii-semantic-utility-document)
- **Issues**: GitHub issue tracker
- **Discussions**: Repository discussions tab
- **Email**: Through GitHub contact system

---

## Document Maintenance

### Last Updated
- **Date**: Current with repository state
- **Version**: Aligned with utility version
- **Reviewer**: Repository maintainers

### Update Schedule
- **Regular Reviews**: Monthly documentation review
- **Version Updates**: Documentation updated with each release
- **User Feedback**: Incorporated as received
- **Continuous Improvement**: Ongoing refinement based on usage patterns

---

This documentation index serves as your central hub for all information about the Breeding EDS DII Semantic Utility Document. Whether you're a new user getting started or an experienced developer implementing advanced integrations, you'll find the resources you need here.

For quick access to the most commonly needed information, start with the [README](../README.md) and [Architecture Overview](../ARCHITECTURE.md). For detailed technical information, refer to the [Technical Specifications](technical-specifications.md) and [Deployment Guide](deployment-guide.md).
