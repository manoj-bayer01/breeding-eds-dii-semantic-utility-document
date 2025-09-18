#!/usr/bin/env python3
"""
Documentation generator for the Semantic Utility project.
Automatically generates and updates documentation based on YAML outputs and code changes.
"""

import os
import sys
import json
import yaml
import datetime
from pathlib import Path
from typing import Dict, List, Any

def load_yaml_files() -> Dict[str, Any]:
    """Load all YAML files from the output directory."""
    output_dir = Path("output")
    yaml_data = {}
    
    if not output_dir.exists():
        return yaml_data
    
    for yaml_file in output_dir.glob("*.yml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                yaml_data[yaml_file.stem] = data
        except Exception as e:
            print(f"Warning: Could not load {yaml_file}: {e}")
    
    return yaml_data

def generate_cube_documentation(yaml_data: Dict[str, Any]) -> str:
    """Generate documentation for cubes from YAML data."""
    doc = []
    doc.append("# Data Cubes Documentation\n")
    
    for file_name, data in yaml_data.items():
        if 'cubes' in data and data['cubes']:
            doc.append(f"## {file_name.replace('_', ' ').title()}\n")
            
            for cube in data['cubes']:
                doc.append(f"### {cube.get('title', cube.get('name', 'Unknown Cube'))}\n")
                doc.append(f"**Name:** `{cube.get('name', 'N/A')}`\n")
                doc.append(f"**SQL Table:** `{cube.get('sql_table', 'N/A')}`\n")
                if cube.get('data_source'):
                    doc.append(f"**Data Source:** {cube.get('data_source')}\n")
                if cube.get('description'):
                    doc.append(f"**Description:** {cube.get('description')}\n")
                doc.append("")
    
    return "\n".join(doc)

def generate_joins_documentation(yaml_data: Dict[str, Any]) -> str:
    """Generate documentation for joins from YAML data."""
    doc = []
    doc.append("# Joins Documentation\n")
    
    for file_name, data in yaml_data.items():
        if 'joins' in data and data['joins']:
            doc.append(f"## {file_name.replace('_', ' ').title()}\n")
            
            for join in data['joins']:
                doc.append(f"### {join.get('name', 'Unknown Join')}\n")
                doc.append(f"**Relationship:** {join.get('relationship', 'N/A')}\n")
                if join.get('sql'):
                    doc.append(f"**SQL:** `{join.get('sql')}`\n")
                doc.append("")
    
    return "\n".join(doc)

def generate_dimensions_documentation(yaml_data: Dict[str, Any]) -> str:
    """Generate documentation for dimensions from YAML data."""
    doc = []
    doc.append("# Dimensions Documentation\n")
    
    for file_name, data in yaml_data.items():
        if 'dimensions' in data and data['dimensions']:
            doc.append(f"## {file_name.replace('_', ' ').title()}\n")
            
            for dim in data['dimensions']:
                doc.append(f"### {dim.get('title', dim.get('name', 'Unknown Dimension'))}\n")
                doc.append(f"**Name:** `{dim.get('name', 'N/A')}`\n")
                doc.append(f"**Type:** `{dim.get('type', 'N/A')}`\n")
                if dim.get('sql'):
                    doc.append(f"**SQL:** `{dim.get('sql')}`\n")
                if dim.get('primaryKey'):
                    doc.append(f"**Primary Key:** Yes\n")
                if dim.get('description'):
                    doc.append(f"**Description:** {dim.get('description')}\n")
                doc.append("")
    
    return "\n".join(doc)

def generate_measures_documentation(yaml_data: Dict[str, Any]) -> str:
    """Generate documentation for measures from YAML data."""
    doc = []
    doc.append("# Measures Documentation\n")
    
    for file_name, data in yaml_data.items():
        if 'measures' in data and data['measures']:
            doc.append(f"## {file_name.replace('_', ' ').title()}\n")
            
            for measure in data['measures']:
                doc.append(f"### {measure.get('title', measure.get('name', 'Unknown Measure'))}\n")
                doc.append(f"**Name:** `{measure.get('name', 'N/A')}`\n")
                doc.append(f"**Type:** `{measure.get('type', 'N/A')}`\n")
                if measure.get('sql'):
                    doc.append(f"**SQL:** `{measure.get('sql')}`\n")
                if measure.get('description'):
                    doc.append(f"**Description:** {measure.get('description')}\n")
                doc.append("")
    
    return "\n".join(doc)

def create_docs_directory():
    """Create docs directory if it doesn't exist."""
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir

def generate_summary_document(yaml_data: Dict[str, Any]) -> str:
    """Generate a summary document of all semantic data."""
    doc = []
    doc.append("# Semantic Data Model Summary\n")
    doc.append(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Count statistics
    total_cubes = sum(len(data.get('cubes', [])) for data in yaml_data.values())
    total_joins = sum(len(data.get('joins', [])) for data in yaml_data.values())
    total_dimensions = sum(len(data.get('dimensions', [])) for data in yaml_data.values())
    total_measures = sum(len(data.get('measures', [])) for data in yaml_data.values())
    
    doc.append("## Overview\n")
    doc.append(f"- **Total Cubes:** {total_cubes}")
    doc.append(f"- **Total Joins:** {total_joins}")
    doc.append(f"- **Total Dimensions:** {total_dimensions}")
    doc.append(f"- **Total Measures:** {total_measures}")
    doc.append(f"- **YAML Files:** {len(yaml_data)}\n")
    
    if yaml_data:
        doc.append("## Files Processed\n")
        for file_name in sorted(yaml_data.keys()):
            data = yaml_data[file_name]
            cubes_count = len(data.get('cubes', []))
            joins_count = len(data.get('joins', []))
            dims_count = len(data.get('dimensions', []))
            measures_count = len(data.get('measures', []))
            
            doc.append(f"### {file_name.replace('_', ' ').title()}")
            doc.append(f"- Cubes: {cubes_count}")
            doc.append(f"- Joins: {joins_count}")
            doc.append(f"- Dimensions: {dims_count}")
            doc.append(f"- Measures: {measures_count}\n")
    
    return "\n".join(doc)

def main():
    """Main documentation generation function."""
    print("🔄 Generating documentation from YAML files...")
    
    # Load YAML data
    yaml_data = load_yaml_files()
    
    if not yaml_data:
        print("⚠️  No YAML files found in output directory")
        return
    
    # Create docs directory
    docs_dir = create_docs_directory()
    
    # Generate different documentation sections
    docs_to_generate = [
        ("SUMMARY.md", generate_summary_document),
        ("CUBES.md", generate_cube_documentation),
        ("JOINS.md", generate_joins_documentation),
        ("DIMENSIONS.md", generate_dimensions_documentation),
        ("MEASURES.md", generate_measures_documentation),
    ]
    
    changes_made = []
    
    for doc_name, generator_func in docs_to_generate:
        doc_path = docs_dir / doc_name
        content = generator_func(yaml_data)
        
        # Check if content has changed
        content_changed = True
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                content_changed = existing_content != content
        
        if content_changed:
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(content)
            changes_made.append(doc_name)
            print(f"✅ Generated/Updated: {doc_name}")
        else:
            print(f"⏭️  Skipped (no changes): {doc_name}")
    
    # Create changes summary for PR comments
    if changes_made:
        changes_summary = f"""# Documentation Changes

The following documentation files were updated:

{chr(10).join(f'- {change}' for change in changes_made)}

Generated from {len(yaml_data)} YAML file(s) containing:
- {sum(len(data.get('cubes', [])) for data in yaml_data.values())} cubes
- {sum(len(data.get('joins', [])) for data in yaml_data.values())} joins  
- {sum(len(data.get('dimensions', [])) for data in yaml_data.values())} dimensions
- {sum(len(data.get('measures', [])) for data in yaml_data.values())} measures
"""
        
        with open(docs_dir / "CHANGES.md", 'w', encoding='utf-8') as f:
            f.write(changes_summary)
    
    print(f"📚 Documentation generation complete! Generated {len(changes_made)} updated files.")

if __name__ == "__main__":
    main()