#!/usr/bin/env python3
"""
Project log updater for the Semantic Utility project.
Updates the project log with information about changes and processing.
"""

import os
import yaml
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Any

def get_git_changes() -> Dict[str, List[str]]:
    """Get recent git changes categorized by file type."""
    try:
        # Get files changed in the last commit
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode != 0:
            # If no previous commit, get all files
            result = subprocess.run(
                ['git', 'ls-files'],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
        
        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # Categorize files
        categories = {
            'python_files': [],
            'excel_files': [],
            'yaml_files': [],
            'markdown_files': [],
            'other_files': []
        }
        
        for file in changed_files:
            if file.endswith('.py'):
                categories['python_files'].append(file)
            elif file.endswith('.xlsx'):
                categories['excel_files'].append(file)
            elif file.endswith(('.yml', '.yaml')):
                categories['yaml_files'].append(file)
            elif file.endswith('.md'):
                categories['markdown_files'].append(file)
            else:
                categories['other_files'].append(file)
        
        return categories
    
    except Exception as e:
        print(f"Warning: Could not get git changes: {e}")
        return {
            'python_files': [],
            'excel_files': [],
            'yaml_files': [],
            'markdown_files': [],
            'other_files': []
        }

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

def generate_processing_summary(yaml_data: Dict[str, Any]) -> str:
    """Generate a summary of the current processing state."""
    if not yaml_data:
        return "No YAML files processed."
    
    summary = []
    summary.append(f"Processed {len(yaml_data)} semantic file(s):")
    
    for file_name, data in yaml_data.items():
        cubes_count = len(data.get('cubes', []))
        joins_count = len(data.get('joins', []))
        dimensions_count = len(data.get('dimensions', []))
        measures_count = len(data.get('measures', []))
        
        summary.append(f"  - {file_name}: {cubes_count} cubes, {joins_count} joins, {dimensions_count} dimensions, {measures_count} measures")
    
    return "\n".join(summary)

def update_project_log():
    """Update the project log with current changes and processing info."""
    log_path = Path("logs/log.md")
    
    if not log_path.exists():
        print("⚠️  Project log not found at logs/log.md")
        return
    
    # Load existing log
    with open(log_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # Get current state
    yaml_data = load_yaml_files()
    git_changes = get_git_changes()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate new log entry
    new_entry = []
    new_entry.append(f"\n## Auto-Documentation Update - {current_time}\n")
    
    # Processing summary
    processing_summary = generate_processing_summary(yaml_data)
    new_entry.append("### Processing Summary")
    new_entry.append(processing_summary)
    new_entry.append("")
    
    # Git changes summary
    if any(git_changes.values()):
        new_entry.append("### Files Changed")
        
        if git_changes['python_files']:
            new_entry.append(f"**Python Files:** {', '.join(git_changes['python_files'])}")
        
        if git_changes['excel_files']:
            new_entry.append(f"**Excel Files:** {', '.join(git_changes['excel_files'])}")
        
        if git_changes['yaml_files']:
            new_entry.append(f"**YAML Files:** {', '.join(git_changes['yaml_files'])}")
        
        if git_changes['markdown_files']:
            new_entry.append(f"**Documentation:** {', '.join(git_changes['markdown_files'])}")
        
        if git_changes['other_files']:
            new_entry.append(f"**Other Files:** {', '.join(git_changes['other_files'])}")
        
        new_entry.append("")
    
    # Documentation generation status
    docs_dir = Path("docs")
    if docs_dir.exists():
        doc_files = list(docs_dir.glob("*.md"))
        if doc_files:
            new_entry.append("### Documentation Generated")
            for doc_file in sorted(doc_files):
                new_entry.append(f"- {doc_file.name}")
            new_entry.append("")
    
    new_entry_text = "\n".join(new_entry)
    
    # Find insertion point (after the last log entry or before the final section)
    lines = existing_content.split('\n')
    insert_index = len(lines)
    
    # Look for a good insertion point
    for i, line in enumerate(lines):
        if line.startswith('## Example Output') or line.startswith('---') or line.strip() == '````':
            insert_index = i
            break
    
    # Insert the new entry
    new_lines = lines[:insert_index] + new_entry_text.split('\n') + lines[insert_index:]
    new_content = '\n'.join(new_lines)
    
    # Write back if content changed
    if new_content != existing_content:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Updated project log")
    else:
        print("⏭️  Project log unchanged")

def create_automated_changelog():
    """Create an automated changelog based on recent changes."""
    changelog_path = Path("CHANGELOG.md")
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Get git changes and YAML data
    git_changes = get_git_changes()
    yaml_data = load_yaml_files()
    
    changelog_entry = []
    changelog_entry.append(f"# Changelog\n")
    changelog_entry.append(f"## {current_date} - Automated Update\n")
    
    # Process changes
    if any(git_changes.values()):
        changelog_entry.append("### Changed")
        
        if git_changes['python_files']:
            changelog_entry.append("- Updated Python utility scripts")
            for file in git_changes['python_files']:
                changelog_entry.append(f"  - {file}")
        
        if git_changes['excel_files']:
            changelog_entry.append("- Updated Excel templates")
            for file in git_changes['excel_files']:
                changelog_entry.append(f"  - {file}")
        
        if git_changes['yaml_files']:
            changelog_entry.append("- Updated YAML semantic files")
            for file in git_changes['yaml_files']:
                changelog_entry.append(f"  - {file}")
        
        changelog_entry.append("")
    
    # Add processing statistics
    if yaml_data:
        total_cubes = sum(len(data.get('cubes', [])) for data in yaml_data.values())
        total_joins = sum(len(data.get('joins', [])) for data in yaml_data.values())
        total_dimensions = sum(len(data.get('dimensions', [])) for data in yaml_data.values())
        total_measures = sum(len(data.get('measures', [])) for data in yaml_data.values())
        
        changelog_entry.append("### Current State")
        changelog_entry.append(f"- Data Cubes: {total_cubes}")
        changelog_entry.append(f"- Joins: {total_joins}")
        changelog_entry.append(f"- Dimensions: {total_dimensions}")
        changelog_entry.append(f"- Measures: {total_measures}")
        changelog_entry.append("")
    
    # Load existing changelog if it exists
    existing_content = ""
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    new_content = "\n".join(changelog_entry)
    
    # Append to existing or create new
    if existing_content:
        # Check if today's entry already exists
        if current_date not in existing_content:
            # Insert after first line (header)
            lines = existing_content.split('\n')
            if lines and lines[0].startswith('# '):
                new_lines = lines[:1] + [''] + new_content.split('\n')[1:] + [''] + lines[1:]
                final_content = '\n'.join(new_lines)
            else:
                final_content = new_content + '\n' + existing_content
        else:
            final_content = existing_content
    else:
        final_content = new_content
    
    # Write changelog
    if final_content != existing_content:
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print("✅ Updated CHANGELOG.md")
    else:
        print("⏭️  CHANGELOG.md unchanged")

def main():
    """Main log update function."""
    print("📝 Updating project logs and changelog...")
    
    # Update the project log
    update_project_log()
    
    # Create/update changelog
    create_automated_changelog()
    
    print("📝 Log update complete!")

if __name__ == "__main__":
    main()