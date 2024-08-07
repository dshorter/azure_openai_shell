from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Workflow of Combining RAG and Grounding in a Legal AI System')

# Define the workflow steps
steps = {
    "Query Received": "Lawyer asks a legal question",
    "Information Retrieval": "RAG retrieves case law and analyses",
    "Response Generation": "Model drafts a summary of findings",
    "Grounding and Verification": "Cross-check against legal texts and databases",
    "Final Response": "Provide verified, legally sound response"
}

# Add nodes with detailed descriptions
for step, description in steps.items():
    dot.node(step, f"{step}\n{description}")

# Define the workflow connections
connections = [
    ("Query Received", "Information Retrieval"),
    ("Information Retrieval", "Response Generation"),
    ("Response Generation", "Grounding and Verification"),
    ("Grounding and Verification", "Final Response")
]

# Add edges between nodes
for start, end in connections:
    dot.edge(start, end)

# Render the graph to a specified file path and format
output_path = 'workflow'
dot.render(f'{output_path}.gv', format='png', view=True)
