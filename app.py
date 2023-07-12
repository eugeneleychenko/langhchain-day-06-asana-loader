import streamlit as st
import asana

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

# Streamlit app
def main():
    st.title("Asana Boards and Cards Viewer")

    # Input workspace ID and Asana API key
    workspace_id = st.text_input("Enter Workspace ID")
    api_key = st.text_input("Enter Asana API Key")

    # Set up Asana client
    client = setup_asana_client(api_key)

    # Get all projects (boards) in the workspace
    projects = get_projects(client, workspace_id)

    # Display projects (boards) and their tasks (cards)
    for project in projects:
        st.subheader(f"Project: {project['name']}")
        tasks = get_tasks(client, project['gid'])
        for task in tasks:
            st.write(f"- {task['name']}")

if __name__ == "__main__":
    main()