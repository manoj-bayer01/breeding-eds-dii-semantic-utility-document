# Deployment Guide

## Breeding EDS DII Semantic Utility Document

### Overview
This guide provides comprehensive instructions for deploying and operating the Excel to YAML Semantic Utility in various environments.

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.9 or higher
- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Storage**: 100MB free space
- **Network**: None required (standalone application)

### User Permissions
- **File System**: Read access to input files, write access to output directory
- **Python**: Permission to install Python packages (pip)
- **Environment**: Ability to execute Python scripts

---

## Installation Methods

### Method 1: Direct Installation (Recommended)

#### Step 1: Clone Repository
```bash
git clone https://github.com/manoj-bayer01/breeding-eds-dii-semantic-utility-document.git
cd breeding-eds-dii-semantic-utility-document
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Verify Installation
```bash
python utility.py --help
```

### Method 2: Virtual Environment Installation

#### Step 1: Create Virtual Environment
```bash
python -m venv semantic-utility-env
```

#### Step 2: Activate Environment
**Windows:**
```cmd
semantic-utility-env\Scripts\activate
```

**macOS/Linux:**
```bash
source semantic-utility-env/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Method 3: Docker Installation (Future)

```dockerfile
# Dockerfile (planned)
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY utility.py .
COPY input/ input/
COPY output/ output/

ENTRYPOINT ["python", "utility.py"]
```

---

## Environment Configuration

### Development Environment

#### Directory Structure
```
breeding-eds-dii-semantic-utility-document/
├── utility.py                    # Main application
├── requirements.txt               # Dependencies
├── README.md                     # User documentation
├── ARCHITECTURE.md               # Architecture documentation
├── docs/                         # Additional documentation
│   ├── architecture-diagrams.md
│   ├── technical-specifications.md
│   └── deployment-guide.md
├── input/                        # Input Excel files
│   └── Semantic_design_template.xlsx
├── output/                       # Generated YAML files
│   └── semantic_output.yml
├── logs/                         # Application logs
│   └── log.md
└── data/                         # Version history
    ├── v1/
    ├── v2/
    ├── v3/
    ├── v4/
    └── v5/
```

#### Environment Variables
Currently no environment variables are required. Future versions may include:
```bash
# Planned environment variables
export SEMANTIC_UTILITY_LOG_LEVEL=INFO
export SEMANTIC_UTILITY_MAX_FILE_SIZE=500MB
export SEMANTIC_UTILITY_OUTPUT_FORMAT=yaml
```

### Production Environment

#### Recommended Structure
```
/opt/semantic-utility/
├── bin/
│   └── utility.py
├── config/
│   └── settings.conf
├── input/
├── output/
├── logs/
└── data/
```

#### Service Configuration (systemd)
```ini
# /etc/systemd/system/semantic-utility.service
[Unit]
Description=Semantic Utility Service
After=network.target

[Service]
Type=oneshot
User=semantic-user
Group=semantic-group
WorkingDirectory=/opt/semantic-utility
ExecStart=/usr/bin/python3 /opt/semantic-utility/bin/utility.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## Deployment Scenarios

### Scenario 1: Local Desktop Usage

#### Setup
1. Install Python 3.9+
2. Download/clone repository to user directory
3. Install dependencies in user space
4. Create desktop shortcuts for common operations

#### Usage
```bash
# Navigate to utility directory
cd ~/semantic-utility

# Process standard template
python utility.py -i input/template.xlsx -o output/result.yml

# Process with filtering
python utility.py -i input/template.xlsx -o output/result.yml --only-cube my_cube

# Verbose processing
python utility.py -i input/template.xlsx -o output/result.yml --verbose
```

### Scenario 2: Server/Batch Processing

#### Setup
1. Install on server with appropriate permissions
2. Configure cron jobs for scheduled processing
3. Set up log rotation and monitoring
4. Implement error notification

#### Cron Configuration
```bash
# Process files every hour
0 * * * * /usr/bin/python3 /opt/semantic-utility/utility.py -i /data/input/template.xlsx -o /data/output/$(date +\%Y\%m\%d_\%H).yml

# Daily batch processing
0 2 * * * /opt/semantic-utility/scripts/batch_process.sh
```

#### Batch Script Example
```bash
#!/bin/bash
# batch_process.sh

INPUT_DIR="/data/input"
OUTPUT_DIR="/data/output"
LOG_DIR="/var/log/semantic-utility"

for file in "$INPUT_DIR"/*.xlsx; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .xlsx)
        output_file="$OUTPUT_DIR/${filename}_$(date +%Y%m%d_%H%M).yml"
        
        python3 /opt/semantic-utility/utility.py \
            -i "$file" \
            -o "$output_file" \
            --verbose >> "$LOG_DIR/batch_$(date +%Y%m%d).log" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "Successfully processed $file"
        else
            echo "Error processing $file" >&2
        fi
    fi
done
```

### Scenario 3: CI/CD Integration

#### GitHub Actions Example
```yaml
# .github/workflows/semantic-processing.yml
name: Process Semantic Templates

on:
  push:
    paths:
      - 'templates/*.xlsx'

jobs:
  process:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Process templates
      run: |
        python utility.py -i templates/template.xlsx -o output/semantic.yml --verbose
    
    - name: Commit results
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add output/semantic.yml
        git commit -m "Update semantic configuration" || exit 0
        git push
```

#### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Process') {
            steps {
                sh '''
                    python utility.py \
                        -i input/template.xlsx \
                        -o output/semantic_${BUILD_NUMBER}.yml \
                        --verbose
                '''
            }
        }
        
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'output/*.yml'
            }
        }
    }
    
    post {
        failure {
            emailext (
                subject: "Semantic Processing Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "The semantic processing job has failed. Please check the logs.",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

---

## Security Configuration

### File Permissions

#### Linux/macOS
```bash
# Set appropriate permissions
chmod 755 utility.py
chmod 644 requirements.txt
chmod 700 input/    # Restrict input access
chmod 755 output/   # Allow output access
chmod 600 logs/     # Restrict log access
```

#### Windows
```cmd
# Set permissions via Properties > Security
# or using icacls command
icacls input /grant Users:F
icacls output /grant Users:F
icacls logs /grant Administrators:F
```

### Access Control

#### User Creation (Linux)
```bash
# Create dedicated user
sudo useradd -m -s /bin/bash semantic-user
sudo usermod -a -G semantic-group semantic-user

# Set ownership
sudo chown -R semantic-user:semantic-group /opt/semantic-utility
```

#### Service Account (Windows)
1. Create service account in Active Directory
2. Grant necessary file system permissions
3. Configure service to run under service account

### Network Security
- **No Network Access Required**: Application runs offline
- **Firewall**: No special firewall rules needed
- **VPN**: Can operate within VPN-restricted environments

---

## Monitoring and Logging

### Log Configuration

#### Basic Logging
```python
# Add to utility.py for enhanced logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/semantic-utility.log'),
        logging.StreamHandler()
    ]
)
```

#### Log Rotation
```bash
# /etc/logrotate.d/semantic-utility
/var/log/semantic-utility/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 semantic-user semantic-group
}
```

### Monitoring Setup

#### Health Check Script
```bash
#!/bin/bash
# health_check.sh

UTILITY_PATH="/opt/semantic-utility"
LOG_FILE="/var/log/semantic-utility/health.log"

# Check if utility is accessible
if python3 "$UTILITY_PATH/utility.py" --help >/dev/null 2>&1; then
    echo "$(date): Utility health check PASSED" >> "$LOG_FILE"
    exit 0
else
    echo "$(date): Utility health check FAILED" >> "$LOG_FILE"
    exit 1
fi
```

#### Performance Monitoring
```bash
#!/bin/bash
# performance_monitor.sh

INPUT_FILE="test_template.xlsx"
OUTPUT_FILE="test_output.yml"
LOG_FILE="/var/log/semantic-utility/performance.log"

start_time=$(date +%s)
python3 utility.py -i "$INPUT_FILE" -o "$OUTPUT_FILE"
end_time=$(date +%s)

duration=$((end_time - start_time))
echo "$(date): Processing completed in ${duration} seconds" >> "$LOG_FILE"
```

---

## Troubleshooting

### Common Issues

#### Issue 1: ModuleNotFoundError
**Symptom**: `ModuleNotFoundError: No module named 'pandas'`
**Solution**:
```bash
pip install -r requirements.txt
# or
pip install pandas openpyxl PyYAML
```

#### Issue 2: Permission Denied
**Symptom**: `PermissionError: [Errno 13] Permission denied`
**Solution**:
```bash
# Check file permissions
ls -la input/ output/
# Fix permissions
chmod 644 input/*.xlsx
chmod 755 output/
```

#### Issue 3: File Not Found
**Symptom**: `FileNotFoundError: Input file not found`
**Solution**:
```bash
# Verify file path
ls -la input/
# Use absolute path
python utility.py -i /full/path/to/input.xlsx -o /full/path/to/output.yml
```

#### Issue 4: Memory Error
**Symptom**: `MemoryError: Unable to allocate array`
**Solution**:
- Reduce Excel file size
- Increase system memory
- Process smaller subsets of data

#### Issue 5: Unicode Error
**Symptom**: `UnicodeDecodeError: 'utf-8' codec can't decode`
**Solution**:
- Save Excel file with UTF-8 encoding
- Check for special characters in data
- Use Excel's "Save As" with UTF-8 option

### Debug Mode

#### Enable Verbose Logging
```bash
python utility.py -i input.xlsx -o output.yml --verbose
```

#### Python Debug Mode
```bash
python -u utility.py -i input.xlsx -o output.yml --verbose 2>&1 | tee debug.log
```

### Performance Tuning

#### Memory Optimization
```python
# For large files, consider processing in chunks
import gc

# Force garbage collection after processing each sheet
gc.collect()
```

#### Disk I/O Optimization
- Use SSD storage for better performance
- Ensure sufficient free disk space (3x file size)
- Place input/output on different drives if possible

---

## Backup and Recovery

### Data Backup Strategy

#### Input Files
```bash
# Daily backup of input files
rsync -av --backup input/ backup/input/$(date +%Y%m%d)/
```

#### Output Files
```bash
# Version-controlled output storage
git add output/*.yml
git commit -m "Automated backup $(date)"
git push origin main
```

#### Configuration Backup
```bash
# Backup entire installation
tar -czf semantic-utility-backup-$(date +%Y%m%d).tar.gz \
    utility.py requirements.txt input/ output/ logs/
```

### Recovery Procedures

#### Application Recovery
1. Restore from backup archive
2. Reinstall dependencies
3. Verify permissions
4. Test with sample file

#### Data Recovery
1. Restore input files from backup
2. Reprocess with known good configuration
3. Compare output with previous versions
4. Validate data integrity

---

## Maintenance Procedures

### Regular Maintenance

#### Weekly Tasks
- Check log files for errors
- Verify disk space availability
- Test processing with sample files
- Review output quality

#### Monthly Tasks
- Update dependencies if needed
- Archive old log files
- Performance baseline testing
- Documentation updates

#### Quarterly Tasks
- Full system backup
- Security review
- Capacity planning
- User training updates

### Update Procedures

#### Dependency Updates
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade pandas

# Update all packages
pip install --upgrade -r requirements.txt
```

#### Application Updates
1. Backup current installation
2. Download new version
3. Test in development environment
4. Deploy to production
5. Verify functionality
6. Document changes

---

## Support and Documentation

### Getting Help
- **Repository Issues**: GitHub issue tracker
- **Documentation**: README.md and architecture docs
- **Community**: User forums or discussion boards
- **Professional Support**: Contact maintainers

### Documentation Maintenance
- Keep deployment guide updated with environment changes
- Document any custom configurations
- Maintain troubleshooting knowledge base
- Regular review of procedures and scripts

---

This deployment guide provides comprehensive instructions for deploying and maintaining the Breeding EDS DII Semantic Utility Document in various environments and scenarios.