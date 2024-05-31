import nbformat
import openai
import os

# Load your OpenAI API key
openai.api_key = 'sk-proj-VgSLg6QmAzC1vljNBlbIT3BlbkFJGmzXkbjYazTRHdPNjzFd'


def extract_code_from_notebook(notebook_path):
    with open(notebook_path, 'r') as f:
        notebook = nbformat.read(f, as_version=4)

    code_cells = [cell['source'] for cell in notebook.cells if cell.cell_type == 'code']
    return code_cells


def generate_wave_dashboard_code(code_snippets):
    prompt = """
    Convert the following Jupyter notebook code snippets into an H2O Wave dashboard code.
    Ensure to include the necessary imports:
    from h2o_wave import main, app, Q, ui, on, run_on
    from typing import Optional, List
    import pandas as pd
    import numpy as np

    Use the following structure for the Wave dashboard code:

    1. Define the functions add_card and clear_cards.
    2. Implement the page functions to handle the main page logic.
    3. Implement the init function to initialize the dashboard layout.
    4. Implement the serve function to start the Wave app.
    5. Create 7 pages with 7 charts, each page includes a chart and a summary.
    6. Main page should include statistical values in horizontal cards and charts in vertical cards.

    Jupyter notebook code snippets:
    {}

    H2O Wave dashboard code:
    """.format("\n\n".join(code_snippets))

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    wave_dashboard_code = response['choices'][0]['message']['content'].strip()
    return wave_dashboard_code


def save_wave_dashboard_code(file_path, code):
    with open(file_path, 'w') as f:
        f.write(code)


# Paths to the Jupyter notebooks
notebooks_path = './notebooks'
notebook_files = ['TimeSeriesVisualization.ipynb']

# Extract and generate code for each notebook
all_code = ""
for notebook_file in notebook_files:
    notebook_path = os.path.join(notebooks_path, notebook_file)
    code_snippets = extract_code_from_notebook(notebook_path)
    wave_dashboard_code = generate_wave_dashboard_code(code_snippets)
    all_code += wave_dashboard_code + "\n\n"

# Save the combined code to app.py
save_wave_dashboard_code('app.py', all_code)
print("Wave dashboard code saved to app.py")
