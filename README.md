# Sankey Diagram Visualization for Internship Program Analysis

This project analyzes data from two CSV files regarding Tech Lead interns and Developer interns from various colleges. It aims to identify imbalances based on a defined ratio (e.g., 1 Tech Lead per 20 Developers) and visualizes these relationships and required adjustments using a Sankey diagram.

## Project Goals

*   Clean and standardize college names from two different data sources.
*   Merge data to get a comprehensive view of intern distribution.
*   Calculate the number of additional Tech Leads or Developer Interns needed per college to meet an ideal ratio.
*   Visualize the current distribution and recommended adjustments using an interactive Sankey diagram.

## Files in the Repository

*   `intern_sankey_analyzer.py`: The main Python script for data processing and visualization.
*   `sorted_affiliations_desc.csv`: CSV file containing counts of Tech Lead interns per affiliation.
*   `dev intern.csv`: CSV file containing counts of Developer interns per institute.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `README.md`: This file.

## Prerequisites

Before you can run this project, you need the following installed on your system:

1.  **Python 3:** Version 3.7 or higher is recommended. You can download it from [python.org](https://www.python.org/downloads/).
2.  **pip:** Python's package installer (usually comes with Python).
3.  **Git:** For cloning the repository (if you haven't already).

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://code.swecha.org/soai2025/techleads/sankey_visualization.git
    cd sankey_visualization
    ```

2.  **Create and activate a Python virtual environment (Recommended):**
    This keeps project dependencies isolated.
    ```bash
    # Navigate into the project directory if you're not already there
    # cd sankey_visualization 

    # Create a virtual environment (e.g., named 'myenv')
    python3 -m venv myenv

    # Activate the virtual environment
    # On Linux/macOS:
    source myenv/bin/activate
    # On Windows (Git Bash or WSL):
    # source myenv/Scripts/activate
    # On Windows (Command Prompt/PowerShell):
    # .\myenv\Scripts\activate
    ```
    You should see `(myenv)` at the beginning of your terminal prompt.

3.  **Install required Python packages:**
    Make sure your virtual environment is active.
    ```bash
    pip install pandas numpy plotly
    ```
    *   `pandas`: For data manipulation and reading CSV files.
    *   `numpy`: For numerical operations (a dependency for pandas).
    *   `plotly`: For creating the interactive Sankey diagram.

4.  **System Dependencies (Linux - Debian/Ubuntu based):**
    If you encounter import errors related to `libstdc++.so.6` when running the script (especially for `numpy`), you might need to ensure the C++ standard library is installed:
    ```bash
    sudo apt update
    sudo apt install libstdc++6
    ```
    After installing system libraries, it's a good idea to reinstall the Python packages within your activated virtual environment:
    ```bash
    pip uninstall numpy pandas -y
    pip install numpy pandas plotly
    ```

## Running the Script

Once the setup is complete and your virtual environment is active:

1.  **Navigate to the project directory** (e.g., `sankey_visualization`).
2.  **Run the Python script:**
    ```bash
    python intern_sankey_analyzer.py
    ```

## Expected Output

*   **Terminal Output:**
    *   Tables showing colleges present in both lists and their current intern counts.
    *   Lists of colleges primarily needing Developers or Tech Leads.
    *   Summary statistics of total interns and recommended additions.
*   **Sankey Diagram:**
    *   An interactive Sankey diagram will automatically open in your default web browser.
    *   This diagram visualizes:
        *   The flow of existing Tech Leads and Developer Interns to colleges.
        *   The recommended number of additional interns (Developers in blue, Tech Leads in green) needed by each college to meet the ideal ratio (currently 1 Tech Lead per 20 Developers).
    *   You can hover over nodes and links in the diagram to see exact counts.

## Customization

*   **Ideal Intern Ratio:** The ideal ratio of Developer Interns per Tech Lead is set by the `IDEAL_DEV_PER_LEAD` variable within the `intern_sankey_analyzer.py` script (currently set to `20`). You can modify this value and rerun the script to see different scenarios.
*   **Data Files:** The script reads data from `sorted_affiliations_desc.csv` and `dev intern.csv`. If you have updated data, replace these files (ensure the column names match the script's expectations: "Affiliation (College/Company/Organization Name)" and "Count" for tech leads; "Institute Name" and "Registrations" for developers).
*   **College Name Cleaning:** The `clean_college_name` function in the script handles standardization. If you find new variations in college names, you might need to add more cleaning rules to this function.

## Troubleshooting

*   **`ImportError: ... numpy ... libstdc++.so.6`:** See Step 4 in "Setup and Installation" regarding system dependencies on Linux.
*   **`fatal: not a git repository`:** Ensure you have run `git init` in your project directory if you are setting it up manually, or that you have successfully cloned the repository.
*   **File Not Found Errors for CSVs:** Make sure the script `intern_sankey_analyzer.py` and the CSV files (`sorted_affiliations_desc.csv`, `dev intern.csv`) are in the same directory when you run the script.
*   **Sankey Diagram Not Opening:** Check your terminal for any error messages from Plotly. Ensure you have a default web browser configured.

