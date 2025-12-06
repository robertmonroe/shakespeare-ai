#!/usr/bin/env python3
"""
Update Inanna 4 project to use Auto mode with 20 passes
"""
import json
import sys

project_file = "projects/Inanna 4/project_data.json"

try:
    # Load project data
    with open(project_file, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
    
    # Update settings
    project_data['auto_review_mode'] = True
    project_data['auto_review_passes'] = 20
    
    # Save updated data
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, indent=4)
    
    print("✅ Updated Inanna 4 project settings:")
    print(f"   • Auto Review Mode: True")
    print(f"   • Auto Review Passes: 20")
    print(f"\nNext chapter will run 20 automated passes!")
    
except FileNotFoundError:
    print(f"❌ Error: {project_file} not found")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
