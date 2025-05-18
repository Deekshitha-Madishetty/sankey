import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
from io import StringIO

# --- Helper function for cleaning college names (consistent) ---
def clean_college_name(name):
    original_name_for_debugging = name
    name = str(name).upper().strip()
    name = re.sub(r'\s*\(.*?\)\s*$', '', name)
    name = re.sub(r'\s*\*.+$', '', name)
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
    name = name.replace("GEETANJALI", "GEETHANJALI")

    if "MALLA REDDY" in name or "MALLAREDDY" in name:
        is_mrew = "FOR WOMEN" in name or "WOMENS" in name
        is_mrem = "MANAGEMENT SCIENCES" in name
        is_mrit = "INSTITUTE OF TECHNOLOGY AND SCIENCE" in name or "INST OF TECHNOLOGY AND SCI" in name
        is_mru = "UNIVERSITY" in name
        is_mrcet = "COLLEGE OF ENGG TECHNOLOGY" in name
        is_mrec_base_sorted = "MALLAREDDY ENGINEERING COLLEGE" == name and "AUTONOMOUS" not in name
        is_mriet = "MALLAREDDY INST OF ENGG AND TECHNOLOGY" == name
        is_mrit_short = "MALLA REDDY INSTITUTE OF TECHNOLOGY" == name

        if is_mrew and not is_mrem:
            name = "MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN"
        elif is_mrem:
            name = "MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES"
        elif is_mrit:
            name = "MALLAREDDY INSTITUTE OF TECHNOLOGY AND SCIENCE"
        elif is_mru:
            name = "MALLA REDDY UNIVERSITY"
        elif is_mrcet:
            name = "MALLA REDDY COLLEGE OF ENGINEERING TECHNOLOGY"
        elif is_mriet:
             name = "MALLAREDDY INSTITUTE OF ENGINEERING AND TECHNOLOGY"
        elif is_mrit_short:
             name = "MALLAREDDY INSTITUTE OF TECHNOLOGY"
        elif is_mrec_base_sorted:
            name = "MALLA REDDY COLLEGE OF ENGINEERING"
        elif "MALLA REDDY COLLEGE OF ENGINEERING" in name and not any([is_mrew, is_mrem, is_mrcet, is_mru]):
             name = "MALLA REDDY COLLEGE OF ENGINEERING"
    name = name.replace(" FOR WOMEN", " FOR WOMEN")
    name = name.rstrip(',.')
    cleaned = name.strip()
    return cleaned

# --- Load Data ---
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

df_merged = df_merged[~df_merged['Cleaned_Name'].isin(["NEXTWAVE", "NIAT", "VIT", "KLH", "KUWL"])]
# Keep colleges even if one count is zero, as the link value will handle it
df_merged = df_merged[(df_merged['Developers'] > 0) | (df_merged['Tech_Leads'] > 0)].copy()


# --- Determine Link Color Based on Imbalance ---
IDEAL_DEVS_PER_TL = 20
df_merged['Link_Color'] = 'rgba(128, 128, 128, 0.7)' # Default Grey
df_merged['Imbalance_Status'] = 'Balanced or N/A'

for index, row in df_merged.iterrows():
    devs = row['Developers']
    tls = row['Tech_Leads']

    needs_tls = False
    needs_devs = False

    if devs > 0: # Check if TLs are needed for existing devs
        ideal_tls_for_devs = np.ceil(devs / IDEAL_DEVS_PER_TL)
        if tls < ideal_tls_for_devs:
            needs_tls = True

    if tls > 0: # Check if Devs are needed for existing TLs
        ideal_devs_for_tls = tls * IDEAL_DEVS_PER_TL
        if devs < ideal_devs_for_tls:
            needs_devs = True
    
    # Assign color based on the primary imbalance
    # If needs TLs (RED condition for link: Devs exist, not enough TLs)
    if needs_tls and not needs_devs: # Clearly needs TLs
        df_merged.loc[index, 'Link_Color'] = 'rgba(255, 0, 0, 0.7)'  # Red
        df_merged.loc[index, 'Imbalance_Status'] = 'Needs Tech Leads (Red Link)'
    elif needs_devs and not needs_tls: # Clearly needs Devs
        df_merged.loc[index, 'Link_Color'] = 'rgba(0, 0, 255, 0.7)'  # Blue
        df_merged.loc[index, 'Imbalance_Status'] = 'Needs Developers (Blue Link)'
    elif needs_tls and needs_devs: # Both are low, e.g. 1 TL, 1 Dev. What's the priority?
        # Let's say if it needs TLs, that's a more critical shortage to show.
        df_merged.loc[index, 'Link_Color'] = 'rgba(255, 0, 0, 0.7)'  # Red (prioritize needing TLs)
        df_merged.loc[index, 'Imbalance_Status'] = 'Critically Low: Needs TLs & Devs (Red Link)'
    elif devs == 0 and tls > 0: # Has TLs, 0 Devs --> Needs Devs
        df_merged.loc[index, 'Link_Color'] = 'rgba(0, 0, 255, 0.7)'  # Blue
        df_merged.loc[index, 'Imbalance_Status'] = 'Needs Developers (Blue Link)'
    elif tls == 0 and devs > 0: # Has Devs, 0 TLs --> Needs TLs
        df_merged.loc[index, 'Link_Color'] = 'rgba(255, 0, 0, 0.7)'  # Red
        df_merged.loc[index, 'Imbalance_Status'] = 'Needs Tech Leads (Red Link)'


# Sort colleges by Developer count for vertical ordering on both sides
df_merged.sort_values(by='Developers', ascending=False, inplace=True)
df_merged.reset_index(drop=True, inplace=True)

# --- Prepare for Sankey Visualization ---
# We need two sets of nodes for colleges: one for Dev side, one for TL side
# Their labels will be the same (college name), but their indices will be different.
college_names_sorted = list(df_merged['Cleaned_Name'])

node_labels_dev_side = [f"{name}_Dev" for name in college_names_sorted]
node_labels_tl_side = [f"{name}_TL" for name in college_names_sorted]

# All unique node labels for the Sankey
sankey_node_labels = node_labels_dev_side + node_labels_tl_side
sankey_node_dict = {label: i for i, label in enumerate(sankey_node_labels)}

source_indices = []
target_indices = []
values = [] # The value of the link will be the sum of Devs + TLs for thickness, or just 1 if only connection
link_colors_sankey = []
link_hover_texts = []

# Node colors: all college nodes can be a neutral color, link color shows imbalance
node_color_dev_side = 'rgba(200, 220, 255, 0.8)' # Light blue for dev side nodes
node_color_tl_side = 'rgba(255, 220, 200, 0.8)' # Light orange for TL side nodes

sankey_node_colors = [node_color_dev_side] * len(node_labels_dev_side) + \
                     [node_color_tl_side] * len(node_labels_tl_side)


# Create Links
for index, row in df_merged.iterrows():
    college_name = row['Cleaned_Name']
    dev_count = row['Developers']
    tl_count = row['Tech_Leads']
    link_color = row['Link_Color']
    status_text = row['Imbalance_Status']

    source_node_label = f"{college_name}_Dev"
    target_node_label = f"{college_name}_TL"

    # The value of the link can be based on total interns, or a fixed value for visibility
    # Using total interns can make links for colleges with 0 on one side look odd.
    # Let's use a combination: if one is 0, use the other. If both >0, use sum.
    # Or, for this visual, the link value *should* represent the flow from devs to TLs for that college.
    # What does the link *value* represent?
    # If it's just a connection, value=1. If it represents total interns, value = dev+tl
    # The thickness of the link should ideally represent the number of *students* at that college.
    # However, the color is key here.
    # Let's make the link value the max of Devs or TLs to give some thickness, or 1 if both are 0 (filtered out)
    link_value = max(1, dev_count, tl_count) # Ensure a minimum thickness for visibility if counts are low

    source_indices.append(sankey_node_dict[source_node_label])
    target_indices.append(sankey_node_dict[target_node_label])
    values.append(link_value)
    link_colors_sankey.append(link_color)
    link_hover_texts.append(f"{college_name}<br>Devs: {dev_count}, TLs: {tl_count}<br>Status: {status_text}")


# --- Create Sankey Diagram ---
if not source_indices:
    print("No data to plot for Sankey diagram.")
else:
    fig = go.Figure(data=[go.Sankey(
        arrangement="perpendicular", # "snap", "perpendicular", "freeform", "fixed"
        node=dict(
            pad=15, # Padding between nodes in the same column
            thickness=15,
            line=dict(color="black", width=0.5),
            label=[name.replace("_Dev", "").replace("_TL", "") for name in sankey_node_labels], # Show clean names
            color=sankey_node_colors, # Nodes are neutral, links show status
            customdata=sankey_node_labels, # Store original suffixed labels for hover if needed
            hovertemplate='College: %{customdata}<extra></extra>' # Or show clean name: %{label}
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors_sankey, # CRITICAL: Link color shows imbalance
            label=link_hover_texts,
            hovertemplate='%{label}<extra></extra>'
        )
    )])

    fig.update_layout(
        title_text="College Intern Imbalance: Developers vs. Tech Leads (1 TL : 20 Devs Ratio)<br>Red Link: Needs TLs | Blue Link: Needs Devs",
        font_size=10,
        height=max(700, len(df_merged) * 22 + 150), # Dynamic height
        # To place labels on left and right, we might need to adjust margins and axis settings.
        # For pure Sankey, the nodes themselves are the columns.
        xaxis=dict(showticklabels=False), # Hide x-axis ticks for cleaner look
        yaxis=dict(showticklabels=False), # Hide y-axis ticks
        margin=dict(l=200, r=200, t=100, b=50) # Ample margin for college names
    )
    # Add annotations for column headers if desired (more complex for dynamic Sankey)
    # For now, the title conveys the left/right meaning.

    fig.show()

print("\n--- College Imbalance Status (Sorted by Developer Count) ---")
print(df_merged[['Cleaned_Name', 'Developers', 'Tech_Leads', 'Imbalance_Status', 'Link_Color']].head(30))