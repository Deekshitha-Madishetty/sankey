import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go

# --- Helper function for cleaning college names ---
def clean_college_name(name):
    name = str(name).upper().strip()
    # Remove content within parentheses like (AUTONOMOUS), (FORMERLY...)
    name = re.sub(r'\s*\(.*?\)', '', name)
    # Handle abbreviation prefixes like "SNIS - "
    if ' - ' in name:
        name = name.split(' - ', 1)[1] # Take the part after the first ' - '
    
    # Specific common substitutions (can be expanded)
    name = name.replace("INSTITUTE OF SCI AND TECHNOLOGY", "INSTITUTE OF SCIENCE AND TECHNOLOGY")
    name = name.replace("ENGG", "ENGINEERING")
    name = name.replace("TECH", "TECHNOLOGY")
    name = name.replace("EDNL SOC GRP OF INSTNS", "EDUCATIONAL SOCIETY GROUP OF INSTITUTIONS")
    name = name.replace("INST", "INSTITUTE")
    name = name.replace("INSTT", "INSTITUTE")
    name = name.replace("SCI", "SCIENCE")
    name = name.replace("COLL", "COLLEGE") # For ANURAG ENGINEERING COLLGE
    name = name.replace("COLLEGEEGE", "COLLEGE") # Typo correction if any

    # Correct specific known issues like GEETHANJALI vs GEETANJALI
    name = name.replace("GEETANJALI", "GEETHANJALI")
    
    # Normalize Malla Reddy variations
    if "MALLA REDDY" in name or "MALLAREDDY" in name:
        if "FOR WOMEN" in name or "WOMENS" in name: # MREW / MALLA REDDY ENGG COLLEGE FOR WOMEN
            if "MANAGEMENT SCIENCES" not in name: # Exclude MREM which isn't for women
                 name = "MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN"
        elif "COLLEGE OF ENGINEERING AND MANAGEMENT SCIENCES" in name: # MREM
            name = "MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES"
        elif "INSTITUTE OF TECHNOLOGY AND SCIENCE" in name: # MRIT
             name = "MALLAREDDY INSTITUTE OF TECHNOLOGY AND SCIENCE" # Keep MRIT distinct
        elif "UNIVERSITY" in name: # MRU
            name = "MALLA REDDY UNIVERSITY"
        elif "MALLA REDDY COLLEGE OF ENGG TECHNOLOGY" in name: # From dev intern list
            name = "MALLA REDDY COLLEGE OF ENGINEERING TECHNOLOGY"
        elif "MALLAREDDY ENGINEERING COLLEGE" == name: # from sorted_affiliations
            name = "MALLA REDDY COLLEGE OF ENGINEERING"
        # Add more specific Malla Reddy rules if needed.
        # The goal is to map to the most common/complete name.

    # Standardize common endings
    name = name.replace(" FOR WOMEN", " FOR WOMEN") # Ensure spacing consistency
    
    # Remove trailing commas or periods
    name = name.rstrip(',.')
    return name.strip()

# --- Load Data ---
# Simulating file loading
tech_leads_data = """Affiliation (College/Company/Organization Name),Count
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

dev_intern_data = """Institute Name,Registrations
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

from io import StringIO
df_tech_leads = pd.read_csv(StringIO(tech_leads_data))
df_devs = pd.read_csv(StringIO(dev_intern_data))

# --- Preprocess Data ---
df_tech_leads.rename(columns={'Affiliation (College/Company/Organization Name)': 'College_Name', 'Count': 'Tech_Leads'}, inplace=True)
df_devs.rename(columns={'Institute Name': 'College_Name', 'Registrations': 'Developers'}, inplace=True)

# Apply cleaning function
df_tech_leads['Cleaned_Name'] = df_tech_leads['College_Name'].apply(clean_college_name)
df_devs['Cleaned_Name'] = df_devs['College_Name'].apply(clean_college_name)

# Aggregate counts for tech leads in case cleaning results in duplicates (e.g. GCTC)
df_tech_leads_agg = df_tech_leads.groupby('Cleaned_Name')['Tech_Leads'].sum().reset_index()

# Aggregate counts for developers (though less likely to have duplicates after cleaning in this specific file)
df_devs_agg = df_devs.groupby('Cleaned_Name')['Developers'].sum().reset_index()

# --- Merge Data ---
df_merged = pd.merge(df_tech_leads_agg, df_devs_agg, on='Cleaned_Name', how='outer')
df_merged.fillna(0, inplace=True) # Colleges not in one list get 0 for that intern type

# Filter out entries with 0 for both, if any, or non-college entries
df_merged = df_merged[(df_merged['Tech_Leads'] > 0) | (df_merged['Developers'] > 0)]
# Specific filter for "NEXTWAVE" and "NIAT" which are likely not colleges in this context
df_merged = df_merged[~df_merged['Cleaned_Name'].isin(["NEXTWAVE", "NIAT"])]


# --- Calculate Imbalances and Required Interns ---
IDEAL_DEV_PER_LEAD = 22 # 1 TL per 22 Devs

df_merged['Devs_To_Add'] = 0
df_merged['TLs_To_Add'] = 0

for index, row in df_merged.iterrows():
    current_tls = row['Tech_Leads']
    current_devs = row['Developers']
    
    if current_tls > 0:
        target_devs_for_current_tls = current_tls * IDEAL_DEV_PER_LEAD
        if current_devs < target_devs_for_current_tls:
            df_merged.loc[index, 'Devs_To_Add'] = target_devs_for_current_tls - current_devs
    
    # This condition should be independent, consider it even if Devs_To_Add was calculated
    # (e.g. 1 TL, 500 Devs. Devs_To_Add will be 0, but TLs_To_Add will be high)
    if current_devs > 0: # only try to add TLs if there are devs to lead
        target_tls_for_current_devs = np.ceil(current_devs / IDEAL_DEV_PER_LEAD)
        if current_tls < target_tls_for_current_devs:
             # Only add TLs if we are NOT already adding devs for existing TLs
             # This logic gets tricky: if we add devs, the TL requirement might change.
             # Let's calculate TLs_To_Add based on *current* devs.
             # If a college needs both, it implies a significant misalignment.
             df_merged.loc[index, 'TLs_To_Add'] = target_tls_for_current_devs - current_tls

# Refinement: If a college needs devs, it shouldn't simultaneously need TLs for *those same devs it doesn't have yet*.
# So, if Devs_To_Add > 0, it implies current TLs are underutilized. We wouldn't add more TLs then.
# If TLs_To_Add > 0, it implies current Devs are under-supervised.
# It's possible for both to be > 0 if, for example, a college has 1 TL and 100 Devs.
# It needs Devs_To_Add = (1*22) - 100 = -78 (so 0).
# It needs TLs_To_Add = ceil(100/22) - 1 = ceil(4.54) - 1 = 5 - 1 = 4. This is correct.

# Consider a case: 10 TLs, 10 Devs
# Devs_To_Add = (10*22) - 10 = 220 - 10 = 210.
# TLs_To_Add = ceil(10/22) - 10 = 1 - 10 = -9 (so 0). Correct.

df_merged['Devs_To_Add'] = df_merged['Devs_To_Add'].clip(lower=0)
df_merged['TLs_To_Add'] = df_merged['TLs_To_Add'].clip(lower=0)

# If a college needs Developers, it means its existing Tech Leads are underutilized.
# So, for these colleges, we should not simultaneously suggest adding Tech Leads.
# If TLs_To_Add > 0, it means existing Devs need more TLs. Devs_To_Add should be 0.
# The logic above should handle this: if Devs_To_Add is calculated, TLs_To_Add will be based on current devs.

# Only keep rows where an action is needed or there are existing interns
df_analysis = df_merged[
    (df_merged['Tech_Leads'] > 0) | \
    (df_merged['Developers'] > 0) | \
    (df_merged['Devs_To_Add'] > 0) | \
    (df_merged['TLs_To_Add'] > 0)
].copy()

# --- Prepare for Sankey Visualization ---
# Create labels for nodes
node_labels = ["Existing Tech Leads Pool", "Existing Developer Interns Pool"]
node_labels += list(df_analysis['Cleaned_Name'].unique())
node_labels += ["Action: Increase Developers", "Action: Increase Tech Leads"]

node_dict = {label: i for i, label in enumerate(node_labels)}

# Initialize Sankey lists
source_indices = []
target_indices = []
values = []
link_colors = [] # For the "Action" links

# 1. Flows for Existing Interns
# From "Existing Tech Leads Pool" to College
for _, row in df_analysis.iterrows():
    if row['Tech_Leads'] > 0:
        source_indices.append(node_dict["Existing Tech Leads Pool"])
        target_indices.append(node_dict[row['Cleaned_Name']])
        values.append(row['Tech_Leads'])
        link_colors.append("rgba(128,128,128,0.5)") # Grey for existing

# From "Existing Developer Interns Pool" to College
for _, row in df_analysis.iterrows():
    if row['Developers'] > 0:
        source_indices.append(node_dict["Existing Developer Interns Pool"])
        target_indices.append(node_dict[row['Cleaned_Name']])
        values.append(row['Developers'])
        link_colors.append("rgba(128,128,128,0.5)") # Grey for existing

# 2. Flows for Actions (Needed Interns)
# From College to "Action: Increase Developers"
for _, row in df_analysis.iterrows():
    if row['Devs_To_Add'] > 0:
        source_indices.append(node_dict[row['Cleaned_Name']])
        target_indices.append(node_dict["Action: Increase Developers"])
        values.append(row['Devs_To_Add'])
        link_colors.append("rgba(0,0,255,0.7)") # Blue

# From College to "Action: Increase Tech Leads"
for _, row in df_analysis.iterrows():
    if row['TLs_To_Add'] > 0:
        source_indices.append(node_dict[row['Cleaned_Name']])
        target_indices.append(node_dict["Action: Increase Tech Leads"])
        values.append(row['TLs_To_Add'])
        link_colors.append("rgba(0,128,0,0.7)") # Green

# Define node colors - Pools and Actions distinct, colleges neutral or based on primary need
node_colors_list = []
for label in node_labels:
    if "Pool" in label:
        node_colors_list.append("orange")
    elif "Action: Increase Developers" == label:
        node_colors_list.append("blue")
    elif "Action: Increase Tech Leads" == label:
        node_colors_list.append("green")
    else: # College nodes
        # Optional: Color college nodes based on primary action. For now, keep them neutral.
        node_colors_list.append("lightblue")


# --- Create Sankey Diagram ---
if not source_indices: # Check if there's anything to plot
    print("No data to plot for Sankey diagram after filtering. Check cleaning and calculations.")
else:
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25, # Increased padding
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors_list # Apply node colors
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors # Apply specific colors to links
        )
    )])

    fig.update_layout(
        title_text="Internship Program Analysis: Current Distribution & Recommended Adjustments<br>(Ideal Ratio: 1 Tech Lead per 22 Developers)",
        font_size=10,
        height=1200  # Adjust height for better readability if many colleges
    )
    fig.show()

# --- Display Key Tables for Analysis ---
print("\n--- Merged and Processed College Data ---")
print(df_analysis[['Cleaned_Name', 'Tech_Leads', 'Developers', 'Devs_To_Add', 'TLs_To_Add']].sort_values(by=['Devs_To_Add', 'TLs_To_Add'], ascending=False).head(20))

print("\n--- Colleges Primarily Needing Developers ---")
needs_devs = df_analysis[df_analysis['Devs_To_Add'] > 0].sort_values(by='Devs_To_Add', ascending=False)
print(needs_devs[['Cleaned_Name', 'Tech_Leads', 'Developers', 'Devs_To_Add']].head(10))


print("\n--- Colleges Primarily Needing Tech Leads ---")
needs_tls = df_analysis[df_analysis['TLs_To_Add'] > 0].sort_values(by='TLs_To_Add', ascending=False)
print(needs_tls[['Cleaned_Name', 'Tech_Leads', 'Developers', 'TLs_To_Add']].head(10))

print(f"\nTotal Tech Leads currently: {df_analysis['Tech_Leads'].sum()}")
print(f"Total Developer Interns currently: {df_analysis['Developers'].sum()}")
print(f"Total Recommended Additional Developers: {df_analysis['Devs_To_Add'].sum()}")
print(f"Total Recommended Additional Tech Leads: {df_analysis['TLs_To_Add'].sum()}")