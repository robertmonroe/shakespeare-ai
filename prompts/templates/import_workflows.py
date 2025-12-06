import requests
import json
import uuid

# N8N configuration
N8N_URL = "http://localhost:5678"
USERNAME = "cgartandweb@gmail.com"
PASSWORD = "MyN8N1@#17"

def import_workflow_to_n8n(workflow_file_path):
    """Import a workflow JSON file directly into N8N"""
    try:
        # Read the workflow JSON file
        with open(workflow_file_path, 'r') as file:
            workflow_data = json.load(file)
        
        # Create session and login
        session = requests.Session()
        
        # Try login
        login_data = {
            'emailOrLdapLoginId': USERNAME,
            'password': PASSWORD
        }
        
        login_response = session.post(f'{N8N_URL}/rest/login', json=login_data)
        
        if login_response.status_code == 200:
            print(f"✅ Logged in successfully")
            
            # Generate new UUIDs for nodes to avoid conflicts
            for node in workflow_data['nodes']:
                if node.get('type') == 'n8n-nodes-base.webhook':
                    new_webhook_id = str(uuid.uuid4())
                    node['parameters']['path'] = new_webhook_id
                    node['webhookId'] = new_webhook_id
                
                # Update node IDs to avoid conflicts
                node['id'] = str(uuid.uuid4())
            
            # Create the workflow
            response = session.post(f'{N8N_URL}/rest/workflows', json=workflow_data)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Successfully imported: {workflow_data['name']}")
                return result
            else:
                print(f"❌ Failed to import {workflow_data['name']}: {response.status_code} - {response.text}")
                return None
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error importing {workflow_file_path}: {e}")
        return None

# List of workflow files to import
workflow_files = [
    'scene_generator_workflow.json',
    'scene_outliner_workflow.json',
    'fact_checker_workflow.json',
    'researcher_workflow.json',
    'worldbuilding_workflow.json',
    'plagiarism_checker_workflow.json'
]

print("Importing LibriScribe workflows into N8N...")
print("=" * 50)

imported_count = 0
total_workflows = len(workflow_files)

for workflow_file in workflow_files:
    print(f"\nImporting {workflow_file}...")
    result = import_workflow_to_n8n(workflow_file)
    if result:
        imported_count += 1

print("=" * 50)
print(f"Import complete: {imported_count}/{total_workflows} workflows imported successfully")

if imported_count == total_workflows:
    print("🎉 All LibriScribe workflows are now in your N8N instance!")
    print("Your complete LibriScribe system (13/13 agents) is ready to use.")
else:
    print(f"⚠️  {total_workflows - imported_count} workflows failed to import. Check the error messages above.")
