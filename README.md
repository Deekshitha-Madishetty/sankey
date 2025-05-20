# College Intern Imbalance Analyzer: AI Dev Interns vs. Tech Leads

This Streamlit application visualizes the balance (or imbalance) between the number of AI Developer Interns and Tech Lead Interns sourced from various colleges. It uses a Sankey diagram to represent the flow and highlight potential needs for either more Dev Interns or more Tech Leads based on an ideal ratio.

**Live App:** [Link to your deployed Streamlit App (e.g., on Streamlit Community Cloud or Hugging Face Spaces)]

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]((https://internanalysis.streamlit.app/))

## Features

*   **Interactive Sankey Diagram:** Visualizes colleges on two sides:
    *   Left Side: Colleges sorted by the number of **AI Developer Interns** (descending).
    *   Right Side: Colleges sorted by the number of **Tech Lead Interns** (descending).
*   **Dynamic Node Labels:** College names are displayed with their respective counts (e.g., "College Name (X Dev Interns)" or "College Name (Y Tech Leads)").
*   **Imbalance Indication:**
    *   Links between the same college on both sides are colored to indicate imbalance:
        *   **Red Link:** College primarily needs Tech Leads.
        *   **Blue Link:** College primarily needs AI Dev Interns.
        *   **Grey Link:** College is relatively balanced or has other non-critical status.
    *   The ideal ratio used for this calculation is 1 Tech Lead : 20 AI Dev Interns.
*   **Data-Driven Insights:** Helps identify colleges that are strong sources for one role versus the other, or where recruitment efforts might need to be balanced.
*   **Underlying Data View:** An expandable section allows users to see the processed data table.

## Data Source

The application uses two primary data sources (currently embedded within the script):
1.  A list of colleges and the count of **Tech Lead Interns** from each.
2.  A list of colleges and the count of **AI Developer Interns** from each.

*Note: The college names undergo a cleaning and normalization process to ensure accurate aggregation and matching.*

## Technologies Used

*   **Python:** Core programming language.
*   **Streamlit:** For building the interactive web application.
*   **Pandas:** For data manipulation and cleaning.
*   **NumPy:** For numerical operations (especially for ratio calculations).
*   **Plotly:** For generating the Sankey diagram.

## How It Works

1.  **Data Loading:** Reads the counts of AI Dev Interns and Tech Leads for various colleges.
2.  **Data Cleaning:** College names are standardized using a custom cleaning function (`clean_college_name`) to handle variations in naming, abbreviations, and to remove extraneous information.
3.  **Data Aggregation & Merging:** Counts are summed up for identically cleaned college names, and the two datasets (Dev Interns and Tech Leads) are merged.
4.  **Imbalance Calculation:** For each college, the script determines if it needs more Tech Leads or more Dev Interns based on an ideal ratio (1 TL : 20 Devs). Link colors are assigned accordingly.
5.  **Sankey Diagram Generation:**
    *   Nodes for the left (Dev Interns) and right (Tech Leads) sides are created. Colleges on the left are sorted by Dev Intern count, and on the right by Tech Lead count.
    *   Node labels include the college name and the respective count (e.g., "College X (100 Dev Interns)").
    *   Links connect the Dev Intern node of a college to its Tech Lead node. Link thickness can represent the total number of interns (Devs + TLs) from that college.
    *   Link colors reflect the calculated imbalance status.
6.  **Streamlit App Display:** The Plotly Sankey diagram is rendered within a Streamlit web application, along with a descriptive title and legend.

## Setup and Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[Your GitHub Username]/[Your Repository Name].git
    cd [Your Repository Name]
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure your `requirements.txt` file includes `streamlit`, `pandas`, `numpy`, and `plotly`)*
4.  **Run the Streamlit app:**
    ```bash
    streamlit run intern_analysis.py  # Or your main Python script name
    ```
    The app should open in your default web browser.

## `requirements.txt`
