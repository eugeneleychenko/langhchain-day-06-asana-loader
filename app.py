import streamlit as st
import asana
from dotenv import find_dotenv, load_dotenv
import os


asanaapi = os.getenv("asana_key")
workspace = os.getenv("board_key")

# Set up Asana client
def setup_asana_client(api_key):
    client = asana.Client.access_token(api_key)
    return client

# Get all projects (boards) in a workspace
def get_projects(client, workspace_id):
    projects = client.projects.find_by_workspace(workspace_id, iterator_type=None)
    return projects

# Get all tasks (cards) in a project
def get_tasks(client, project_id):
    tasks = client.tasks.find_by_project(project_id, iterator_type=None)
    return tasks

# Get all members of a project
def get_members(client, project_id):
    members = client.projects.get_project(project_id)['members']
    return members

# Streamlit app
def main():
    load_dotenv(find_dotenv())
    st.title("Asana Boards and Cards Viewer")

    # Input workspace ID and Asana API key
    workspace_id = st.text_input("Enter Workspace ID", value = "1138695142391198")
    api_key = st.text_input("Enter Asana API Key", value = asanaapi)

    # Set up Asana client
    client = setup_asana_client(api_key)

    # Get all projects (boards) in the workspace
    projects = get_projects(client, workspace_id)

    # Prepare data for JSON
    data = {"workspaces": []}
    workspace = {"id": workspace_id, "projects": []}
    for project in projects:
        project_data = {"id": project['gid'], "name": project['name'], "tasks": []}
        tasks = get_tasks(client, project['gid'])
        for task in tasks:
            task_data = {"id": task['gid'], "name": task['name']}
            project_data["tasks"].append(task_data)
        workspace["projects"].append(project_data)
    data["workspaces"].append(workspace)

    # Display JSON
    st.json(data)

if __name__ == "__main__":
    main()