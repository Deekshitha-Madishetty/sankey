import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
from io import StringIO

# --- Helper function for cleaning college names (consistent with previous) ---
def clean_college_name(name):
    name = str(name).upper().strip()
    name = re.sub(r'\s*\(.*?\)\s*$', '', name) # Removes content in parentheses
    name = re.sub(r'\s*\*.+$', '', name)     # Removes " *" and anything after
    if ' - ' in name:
        name = name.split(' - ', 1)[1]

    name = name.replace("INSTITUTE OF SCI AND TECHNOLOGY", "INSTITUTE OF SCIENCE AND TECHNOLOGY")
    name = name.replace("ENGG", "ENGINEERING")
    name = name.replace("TECH", "TECHNOLOGY")
    name = name.replace("EDNL SOC GRP OF INSTNS", "EDUCATIONAL SOCIETY GROUP OF INSTITUTIONS")
    name = name.replace("INST", "INSTITUTE")
    name = name.replace("INSTT", "INSTITUTE")
    name = name.replace("SCI", "SCIENCE")
    name = name.replace("COLL", "COLLEGE")
    name = name.replace("COLLEGEEGE", "COLLEGE")
    name = name.replace("GEETANJALI", "GEETHANJALI") # Standardize

    # Normalize Malla Reddy variations (simplified for this example, expand if needed)
    if "MALLA REDDY" in name or "MALLAREDDY" in name:
        if "FOR WOMEN" in name or "WOMENS" in name:
            if "MANAGEMENT SCIENCES" not in name:
                 name = "MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN"
        elif "COLLEGE OF ENGINEERING AND MANAGEMENT SCIENCES" in name:
            name = "MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES"
        elif "INSTITUTE OF TECHNOLOGY AND SCIENCE" in name or "INST OF TECHNOLOGY AND SCI" in name :
             name = "MALLAREDDY INSTITUTE OF TECHNOLOGY AND SCIENCE"
        elif "UNIVERSITY" in name:
            name = "MALLA REDDY UNIVERSITY"
        elif "MALLA REDDY COLLEGE OF ENGG TECHNOLOGY" in name:
            name = "MALLA REDDY COLLEGE OF ENGINEERING TECHNOLOGY"
        elif "MALLAREDDY ENGINEERING COLLEGE" == name and "AUTONOMOUS" not in name:
            name = "MALLA REDDY COLLEGE OF ENGINEERING" # Base MRCE
        elif "MALLAREDDY INST OF ENGG AND TECHNOLOGY" == name:
            name = "MALLAREDDY INSTITUTE OF ENGINEERING AND TECHNOLOGY"
        elif "MALLA REDDY INSTITUTE OF TECHNOLOGY" == name:
             name = "MALLAREDDY INSTITUTE OF TECHNOLOGY"
        # Fallback for general Malla Reddy College of Engineering
        elif "MALLA REDDY COLLEGE OF ENGINEERING" in name and not any(s in name for s in ["FOR WOMEN", "MANAGEMENT SCIENCES", "TECHNOLOGY", "UNIVERSITY", "INSTITUTE"]):
            name = "Malla Reddy College of Engineering".upper()


    name = name.replace(" FOR WOMEN", " FOR WOMEN")
    name = name.rstrip(',.')
    return name.strip()

# --- Load Data (from provided CSV strings) ---
tech_leads_data_csv = """Affiliation (College/Company/Organization Name),Count
SNIS - SREENIDHI INSTITUTE OF SCI AND TECHNOLOGY,85
GCTC - GEETHANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),41
VJEC - V N R VIGNAN JYOTHI INSTITUTE OF ENGG AND TECH,31
STLW - STANLEY COLLEGE OF ENGG AND TECHNOLOGY FOR WOMEN (AUTONOMOUS),29
MRCE - MALLA REDDY COLLEGE OF ENGINEERING,28
KGRH - KG REDDY COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),27
JNTH - JNTU COLLEGE OF ENGG HYDERABAD,25
MGIT - MAHATMA GANDHI INSTITUTE OF TECHNOLOGY,24
BVRI - B V RAJU INSTITUTE OF TECHNOLOGY,23
NNRG - NALLA NARASIMHA REDDY EDNL SOC GRP OF INSTNS,20
GRRR - GOKARAJU RANGARAJU INSTITUTE OF ENGG AND TECH,19
SPEC - ST PETERS ENGINEERING COLLEGE (AUTONOMOUS),15
BITN - BALAJI INSTITUTE OF TECHNOLOGY AND SCI,14
VAGE - VAAGDEVI COLLEGE OF ENGINEERING,12
VJIT - VIDYAJYOTHI INSTITUTE OF TECHNOLOGY,9
GCTC - GEETANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),7
NREC - NALLAMALLA REDDY ENGINEERING COLLEGE (AUTONOMOUS),6
BVRW - BVRIT COLLEGE OF ENGINEERING FOR WOMEN,6
IITT - INDUR INSTITUTE OF ENGINEERING AND TECHNOLOGY,5
VMTW - VIGNANS INST OF MANAGEMENT AND TECH FOR WOMEN,5
GNTW - G NARAYNAMMA INSTITUTE OF TECHNOLOGY AND SCI,5
ANUG - ANURAG UNIVERSITY (FORMERLY ANURAG GRP OF INSTNS- CVSR COLL OF ENGG),5
VIT - VELLORE INSTITUTE OF TECHNOLOGY,5
MLRS - MARRI LAXMAN REDDY INST OF TECHNOLOGY AND MANAGEMENT (AUTONOMOUS),4
OUCE - OSMANIA UNIVERSITY COLLEGE OF ENGINEERING,4
JBIT - J B INSTITUTE OF ENGG AND TECHNOLOGY,3
VGNT - VIGNAN INSTITUTE OF TECHNOLOGY AND SCI,3
MECS - MATRUSRI ENGINEERING COLLEGE,3
VGWL - VAGDEVI ENGINEERING COLLEGE,2
SWRN - SWARNANDHRA COLLEGE OF ENGINEERING AND TECHNOLOGY,2
BREW - BHOJREDDY ENGINEERING COLLEGE FOR WOMEN,1
ACEG - A C E ENGINEERING COLLEGE (AUTONOMOUS),1
JNTHMT - JNTUH-5 YEAR INTEGRATED MTECH SELF FINANCE,1
IOES - GOVERNMENT INSTITUTE OF ELECTRONICS,1
GNIT - GURUNANAK INST OF TECHNOLOGY,1
CMRK - C M R COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),1
IIITH - INTERNATIONAL INSTITUTE OF INFORMATION AND TECHNOLOGY,1
BRIL - BRILLIANT INSTT OF ENGG AND TECHNOLOGY,1
KMIT - KESHAV MEMORIAL INSTITUTE OF TECHNOLOGY,1
KLH - K L UNIVERSITY,1
NGIT - NEIL GOGTE INSTITUTE OF TECHNOLOGY,1
NIAT,1
MRU – MALLA REDDY UNIVERSITY,1
MRIT - MALLAREDDY INST OF TECHNOLOGY AND SCI,1
MREM - MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES,1
MREW - MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN,1
MALLAREDDY COLLEGE OF ENGINEERING,1
KUWL - KAKATIYA UNIVERSITY,1
MVSR - M V S R ENGINEERING COLLEGE (AUTONOMOUS),1
NEXTWAVE,1
SRHP - SR UNIVERSITY ( FORMERLY S R ENGINEERING COLLEGE),1
SDEW - SRIDEVI WOMENS ENGINEERING COLLEGE,1
OUCE - OSMANIA UNIVERSITY,1
VBIT - VIGNAN BHARATI INSTITUTE OF TECHNOLOGY (AUTONOMOUS),1
"""

dev_intern_data_csv = """Institute Name,Registrations
ANURAG UNIVERSITY (FORMERLY ANURAG GRP OF INSTNS- CVSR COLL OF ENGG),898
C M R COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),555
VARDHAMAN COLLEGE OF ENGINEERING,444
M L R INSTITUTE OF TECHNOLOGY,440
JNTU COLLEGE OF ENGG HYDERABAD,411
V N R VIGNAN JYOTHI INSTITUTE OF ENGG AND TECH,368
M V S R ENGINEERING COLLEGE (AUTONOMOUS),366
VIDYAJYOTHI INSTITUTE OF TECHNOLOGY,273
GEETHANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),269
BVRIT COLLEGE OF ENGINEERING FOR WOMEN,241
SREENIDHI INSTITUTE OF SCI AND TECHNOLOGY,229
STANLEY COLLEGE OF ENGG AND TECHNOLOGY FOR WOMEN (AUTONOMOUS),217
CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY,198
INSTITUTE OF AERONAUTICAL ENGINEERING,182
MALLA REDDY COLLEGE OF ENGG TECHNOLOGY (AUTONOMOUS),178
GOKARAJU RANGARAJU INSTITUTE OF ENGG AND TECH,173
VAGDEVI ENGINEERING COLLEGE,133
MAHATMA GANDHI INSTITUTE OF TECHNOLOGY,128
PALLAVI ENGINEERING COLLEGE,128
MATRUSRI ENGINEERING COLLEGE,126
MALLA REDDY ENGG COLLEGE FOR WOMEN (AUTONOMOUS),125
MALLA REDDY COLLEGE OF ENGINEERING,111
NARSIMHAREDDY ENGINEERING COLLEGE (AUTONOMOUS),100
MARRI LAXMAN REDDY INST OF TECHNOLOGY AND MANAGEMENT (AUTONOMOUS),96
B V RAJU INSTITUTE OF TECHNOLOGY,94
NALLA NARASIMHA REDDY EDNL SOC GRP OF INSTNS,91
ST PETERS ENGINEERING COLLEGE (AUTONOMOUS),89
SRIDEVI WOMENS ENGINEERING COLLEGE,87
NALLAMALLA REDDY ENGINEERING COLLEGE (AUTONOMOUS),86
CMR TECHNICAL CAMPUS (AUTONOMOUS),83
A C E ENGINEERING COLLEGE (AUTONOMOUS),75
TEEGALA KRISHNA REDDY ENGINEERING COLLEGE (AUTONOMOUS),68
J B INSTITUTE OF ENGG AND TECHNOLOGY,59
VIGNAN INSTITUTE OF TECHNOLOGY AND SCI,53
SPHOORTHY ENGINEERING COLLEGE,51
G NARAYNAMMA INSTITUTE OF TECHNOLOGY AND SCI,48
VIGNAN BHARATI INSTITUTE OF TECHNOLOGY (AUTONOMOUS),43
METHODIST COLLEGE OF ENGINEERING AND TECHNOLOGY (AUTONOMOUS),41
BHARAT INSTITUTE OF ENGG AND TECHNOLOGY,39
KG REDDY COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),38
CVR COLLEGE OF ENGINEERING,33
HYDERABAD INST OF TECHNOLOGY AND MGMT (AUTONOMOUS),26
CMR INSTITUTE OF TECHNOLOGY (AUTONOMOUS),24
ANURAG ENGINEERING COLLGE,23
VIJAYA ENGINEERING COLLEGE,23
SIDDHARTHA INSTT OF ENGG AND TECHNOLOGY,16
VAAGDEVI COLLEGE OF ENGINEERING,16
D R K INSTITUTE OF SCI AND TECHNOLOGY,13
GOKARAJU LAILAVATHI WOMENS ENGINEERING COLLEGE,12
BALAJI INSTITUTE OF TECHNOLOGY AND SCI,11
MOTHER THERESA COLLEGE OF ENGG AND TECHNOLOGY,11
MALLAREDDY INST OF TECHNOLOGY AND SCI,10
GURUNANAK INST OF TECHNOLOGY,8
HOLY MARY INSTITUTE OF TECH SCIENCE (AUTONOMOUS),8
MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN,8
SREE DATTHA INSTITUTE OF ENGINEERING AND SCIENCE,8
AVANTHIS SCIENTIFIC TECH AND RESEARCH ACADEMY,7
AVANTHI INST OF ENGG AND TECHNOLOGY,6
M J COLLEGE OF ENGINEERING AND TECHNOLOGY,6
SIDDHARTHA INSTT OF TECHNOLOGY AND SCIENCES,6
GURUNANAK INSTTECH CAMPUS,5
INDUR INSTITUTE OF ENGINEERING AND TECHNOLOGY,4
MALLAREDDY INST OF ENGG AND TECHNOLOGY,4
AVN INST OF ENGG TECHNOLOGY,3
LORDS INSTITUTE OF ENGINEERING AND TECHNOLOGY (AUTONOMOUS),3
ELLENKI COLLGE OF ENGG AND TECHNOLOGY,2
MAHAVEER INSTITUTE OF SCI AND TECHNOLOGY,2
MALLA REDDY INSTITUTE OF TECHNOLOGY,2
VIGNANS INST OF MANAGEMENT AND TECH FOR WOMEN,2
D R K COLLEGE OF ENGINEERING AND TECHNOLOGY,1
JAYA PRAKASH NARAYAN COLLEGE OF ENGINEERING,1
MOTHER TERESA INSTITUTE OF SCI AND TECHNOLOGY,1
BHARAT INSTITUTE OF TECHNOLOGY,0
BOMMA INST OF TECHNOLOGY AND SCI,0
MALLAREDDY ENGINEERING COLLEGE (AUTONOMOUS),0
SREE DATTHA GRP OF INSTNS,0
T K R COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),0
"""

df_tech_leads = pd.read_csv(StringIO(tech_leads_data_csv))
df_devs = pd.read_csv(StringIO(dev_intern_data_csv))

# --- Preprocess Data ---
df_tech_leads.rename(columns={'Affiliation (College/Company/Organization Name)': 'College_Name', 'Count': 'Tech_Leads'}, inplace=True)
df_devs.rename(columns={'Institute Name': 'College_Name', 'Registrations': 'Developers'}, inplace=True)

df_tech_leads['Cleaned_Name'] = df_tech_leads['College_Name'].apply(clean_college_name)
df_devs['Cleaned_Name'] = df_devs['College_Name'].apply(clean_college_name)

df_tech_leads_agg = df_tech_leads.groupby('Cleaned_Name')['Tech_Leads'].sum().reset_index()
df_devs_agg = df_devs.groupby('Cleaned_Name')['Developers'].sum().reset_index()

df_merged = pd.merge(df_tech_leads_agg, df_devs_agg, on='Cleaned_Name', how='outer')
df_merged.fillna(0, inplace=True)
df_merged['Developers'] = df_merged['Developers'].astype(int)
df_merged['Tech_Leads'] = df_merged['Tech_Leads'].astype(int)

# Filter out non-college entries and those with no interns at all
df_merged = df_merged[~df_merged['Cleaned_Name'].isin(["NEXTWAVE", "NIAT"])]
df_merged = df_merged[(df_merged['Developers'] > 0) | (df_merged['Tech_Leads'] > 0)].copy()

# CRITICAL: Sort by Developers descending. This order determines the vertical position of college nodes.
df_merged.sort_values(by='Developers', ascending=False, inplace=True)
df_merged.reset_index(drop=True, inplace=True) # Reset index after sorting


# --- Prepare for Sankey Visualization (Slope Chart Style) ---

node_label_dev_category = "Developer Interns (by College)"
node_label_tl_category = "Tech Lead Interns (by College)"

# College names *from the sorted dataframe* will form the middle nodes
# Their order in node_labels list dictates their vertical position in the Sankey
college_node_labels = list(df_merged['Cleaned_Name'])

# Construct the full list of node labels in the desired order for Sankey columns
node_labels = [node_label_dev_category] + college_node_labels + [node_label_tl_category]
node_dict = {label: i for i, label in enumerate(node_labels)}

source_indices = []
target_indices = []
values = []
link_colors_sankey = []
link_hover_texts = []

# Generate distinct colors for each college path
import plotly.colors
# Combine palettes for more unique colors if many colleges
color_palette = plotly.colors.qualitative.Plotly + plotly.colors.qualitative.Alphabet + plotly.colors.qualitative.Light24
college_color_map = {
    name: color_palette[i % len(color_palette)]
    for i, name in enumerate(df_merged['Cleaned_Name']) # Use order from sorted df_merged
}

# Create links
for index, row in df_merged.iterrows():
    college_name = row['Cleaned_Name']
    dev_count = row['Developers']
    tl_count = row['Tech_Leads']
    college_sankey_color = college_color_map.get(college_name, 'rgba(200,200,200,0.7)') # Default color

    # Flow 1: From "Developer Interns Category" node to the College node
    if dev_count > 0: # Only create a link if there's a value
        source_indices.append(node_dict[node_label_dev_category])
        target_indices.append(node_dict[college_name]) # Target is the college node itself
        values.append(dev_count)
        link_colors_sankey.append(college_sankey_color)
        link_hover_texts.append(f"{college_name}<br>{dev_count} Developers")

    # Flow 2: From the College node to "Tech Lead Interns Category" node
    if tl_count > 0: # Only create a link if there's a value
        source_indices.append(node_dict[college_name]) # Source is the college node itself
        target_indices.append(node_dict[node_label_tl_category])
        values.append(tl_count)
        link_colors_sankey.append(college_sankey_color) # Use the same color for the college's path
        link_hover_texts.append(f"{college_name}<br>{tl_count} Tech Leads")


# Node Colors: Category nodes different, college nodes use their path color
sankey_node_colors_list = []
for label in node_labels:
    if label == node_label_dev_category:
        sankey_node_colors_list.append('rgba(31, 119, 180, 0.9)') # Blue
    elif label == node_label_tl_category:
        sankey_node_colors_list.append('rgba(255, 127, 14, 0.9)') # Orange
    else: # College node
        sankey_node_colors_list.append(college_color_map.get(label, 'rgba(220,220,220,0.8)')) # College's specific path color

# --- Create Sankey Diagram ---
if not source_indices: # Check if there are any links to draw
    print("No data to plot for Sankey diagram. Check data and filtering.")
else:
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap", # "snap", "perpendicular", "freeform"
        node=dict(
            pad=15, # Padding between nodes
            thickness=20, # Thickness of nodes
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=sankey_node_colors_list, # Apply node colors
            hovertemplate='%{label}<extra></extra>' # Simple hover for nodes
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors_sankey, # Color links by college path
            label=link_hover_texts, # Custom hover text for links
            hovertemplate='%{label}<extra></extra>' # Display only our custom label
        )
    )])

    fig.update_layout(
        title_text="College Intern Comparison: Developers vs. Tech Leads (Sankey Style)",
        font_size=10,
        height=max(600, len(df_merged) * 22), # Dynamic height based on number of colleges
        margin=dict(l=150, r=150, t=60, b=50) # Adjust margins if labels are cut off
    )
    fig.show()

print("\n--- Data for Sankey (Sorted by Developer Interns) ---")
# Display a few columns to verify order and data
print(df_merged[['Cleaned_Name', 'Developers', 'Tech_Leads']].head(20))