#!/usr/bin/env python3
"""
Architecture documentation updater for the Semantic Utility project.
Updates architecture diagrams and documentation based on YAML structure.
"""

import os
import yaml
import datetime
from pathlib import Path
from typing import Dict, List, Any, Set

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

def extract_relationships(yaml_data: Dict[str, Any]) -> Dict[str, Set[str]]:
    """Extract table relationships from join definitions."""
    relationships = {}
    
    for file_data in yaml_data.values():
        cubes = file_data.get('cubes', [])
        joins = file_data.get('joins', [])
        
        # Extract cube tables
        cube_tables = {cube.get('name', 'unknown') for cube in cubes if cube.get('name')}
        
        # Process joins
        for join in joins:
            primary = join.get('name', '').replace('_', ' ').title()
            if primary:
                if primary not in relationships:
                    relationships[primary] = set()
                
                # Extract related tables from SQL
                sql = join.get('sql', '')
                if sql:
                    # Simple extraction - look for table references
                    for cube_name in cube_tables:
                        if cube_name in sql:
                            relationships[primary].add(cube_name)
    
    return relationships

def generate_mermaid_diagram(yaml_data: Dict[str, Any]) -> str:
    """Generate a Mermaid diagram showing the data architecture."""
    lines = ["```mermaid", "graph TB"]
    
    # Track all entities
    all_cubes = set()
    all_joins = set()
    
    for file_name, file_data in yaml_data.items():
        cubes = file_data.get('cubes', [])
        joins = file_data.get('joins', [])
        
        # Add cubes
        for cube in cubes:
            cube_name = cube.get('name', 'unknown')
            cube_title = cube.get('title', cube_name)
            all_cubes.add(cube_name)
            lines.append(f"    {cube_name}[\"{cube_title}\"]")
            lines.append(f"    {cube_name} --> |contains| {cube_name}_data{{Data}}")
        
        # Add joins/relationships
        for join in joins:
            join_name = join.get('name', 'unknown')
            relationship = join.get('relationship', 'related_to')
            all_joins.add(join_name)
            
            # Connect related entities
            for cube_name in all_cubes:
                sql = join.get('sql', '')
                if cube_name in sql or cube_name in join_name:
                    lines.append(f"    {cube_name} -.-> |{relationship}| {join_name}")
    
    lines.append("```")
    return "\n".join(lines)

def generate_architecture_overview(yaml_data: Dict[str, Any]) -> str:
    """Generate comprehensive architecture documentation."""
    doc = []
    doc.append("# Data Architecture Overview\n")
    doc.append(f"*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Statistics
    total_files = len(yaml_data)
    total_cubes = sum(len(data.get('cubes', [])) for data in yaml_data.values())
    total_joins = sum(len(data.get('joins', [])) for data in yaml_data.values())
    total_dimensions = sum(len(data.get('dimensions', [])) for data in yaml_data.values())
    total_measures = sum(len(data.get('measures', [])) for data in yaml_data.values())
    
    doc.append("## Architecture Statistics\n")
    doc.append(f"| Component | Count |")
    doc.append(f"|-----------|-------|")
    doc.append(f"| Semantic Files | {total_files} |")
    doc.append(f"| Data Cubes | {total_cubes} |")
    doc.append(f"| Joins | {total_joins} |")
    doc.append(f"| Dimensions | {total_dimensions} |")
    doc.append(f"| Measures | {total_measures} |\n")
    
    # Architecture diagram
    doc.append("## Data Model Diagram\n")
    doc.append(generate_mermaid_diagram(yaml_data))
    doc.append("")
    
    # Detailed breakdown by file
    doc.append("## Components by File\n")
    for file_name, data in sorted(yaml_data.items()):
        doc.append(f"### {file_name.replace('_', ' ').title()}\n")
        
        cubes = data.get('cubes', [])
        if cubes:
            doc.append("**Data Cubes:**")
            for cube in cubes:
                name = cube.get('name', 'Unknown')
                title = cube.get('title', name)
                doc.append(f"- `{name}`: {title}")
            doc.append("")
        
        joins = data.get('joins', [])
        if joins:
            doc.append("**Relationships:**")
            for join in joins:
                name = join.get('name', 'Unknown')
                relationship = join.get('relationship', 'unknown')
                doc.append(f"- `{name}` ({relationship})")
            doc.append("")
        
        dimensions = data.get('dimensions', [])
        if dimensions:
            doc.append(f"**Dimensions:** {len(dimensions)} defined")
            doc.append("")
        
        measures = data.get('measures', [])
        if measures:
            doc.append(f"**Measures:** {len(measures)} defined")
            doc.append("")
    
    return "\n".join(doc)

def generate_data_lineage(yaml_data: Dict[str, Any]) -> str:
    """Generate data lineage documentation."""
    doc = []
    doc.append("# Data Lineage\n")
    doc.append(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Extract lineage information
    for file_name, data in yaml_data.items():
        cubes = data.get('cubes', [])
        joins = data.get('joins', [])
        
        if cubes:
            doc.append(f"## {file_name.replace('_', ' ').title()}\n")
            
            for cube in cubes:
                cube_name = cube.get('name', 'Unknown')
                sql_table = cube.get('sql_table', 'Unknown')
                
                doc.append(f"### {cube.get('title', cube_name)}\n")
                doc.append(f"**Source:** `{sql_table}`")
                doc.append(f"**Cube Name:** `{cube_name}`")
                
                # Find related joins
                related_joins = [j for j in joins if cube_name in j.get('sql', '')]
                if related_joins:
                    doc.append(f"**Related Joins:**")
                    for join in related_joins:
                        doc.append(f"- {join.get('name', 'Unknown')} ({join.get('relationship', 'unknown')})")
                
                doc.append("")
    
    return "\n".join(doc)

def update_readme_architecture_section():
    """Update the architecture section in README.md."""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("⚠️  README.md not found")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Load YAML data for stats
    yaml_data = load_yaml_files()
    
    if not yaml_data:
        return
    
    # Generate architecture section
    arch_section = f"""

## Current Architecture

*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

This repository contains semantic data models with the following components:

- **Data Cubes:** {sum(len(data.get('cubes', [])) for data in yaml_data.values())}
- **Joins:** {sum(len(data.get('joins', [])) for data in yaml_data.values())}
- **Dimensions:** {sum(len(data.get('dimensions', [])) for data in yaml_data.values())}
- **Measures:** {sum(len(data.get('measures', [])) for data in yaml_data.values())}

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

"""
    
    # Check if architecture section exists
    if "## Current Architecture" in content:
        # Replace existing section
        lines = content.split('\n')
        new_lines = []
        skip_section = False
        
        for line in lines:
            if line.startswith("## Current Architecture"):
                skip_section = True
                new_lines.append(arch_section.strip())
                continue
            elif skip_section and line.startswith("## "):
                skip_section = False
                new_lines.append(line)
            elif not skip_section:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
    else:
        # Add before conclusion if it exists, otherwise at the end
        if "## Conclusion" in content:
            new_content = content.replace("## Conclusion", arch_section + "\n## Conclusion")
        else:
            new_content = content + arch_section
    
    # Write back if changed
    if new_content != content:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Updated README.md architecture section")
    else:
        print("⏭️  README.md architecture section unchanged")

def main():
    """Main architecture documentation function."""
    print("🏗️  Updating architecture documentation...")
    
    # Load YAML data
    yaml_data = load_yaml_files()
    
    if not yaml_data:
        print("⚠️  No YAML files found in output directory")
        return
    
    # Create docs directory
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Generate architecture documents
    docs_to_generate = [
        ("ARCHITECTURE.md", generate_architecture_overview),
        ("DATA_LINEAGE.md", generate_data_lineage),
    ]
    
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
            print(f"✅ Generated/Updated: {doc_name}")
        else:
            print(f"⏭️  Skipped (no changes): {doc_name}")
    
    # Update README architecture section
    update_readme_architecture_section()
    
    print("🏗️  Architecture documentation update complete!")

if __name__ == "__main__":
    main()