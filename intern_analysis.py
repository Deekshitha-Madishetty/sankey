import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
from io import StringIO

# --- Helper function for cleaning college names (consistent) ---
# This function can be kept as is
def clean_college_name(name):
    name = str(name).upper().strip()
    name = re.sub(r'\s*\(.*?\)\s*$', '', name)
    name = re.sub(r'\s*\*.+$', '', name)
    
    if ' - ' in name:
        name = name.split(' - ', 1)[1].strip()

    name = name.replace("INSTITUTE OF SCI AND TECHNOLOGY", "INSTITUTE OF SCIENCE AND TECHNOLOGY")
    name = name.replace("EDNL SOC GRP OF INSTNS", "EDUCATIONAL SOCIETY GROUP OF INSTITUTIONS")
    name = name.replace("GEETANJALI", "GEETHANJALI")
    name = name.replace("O U COLLEGE OF ENGINEERING HYDERABAD", "OSMANIA UNIVERSITY COLLEGE OF ENGINEERING")
    name = name.replace("VIGNANA BHARATHI", "VIGNAN BHARATHI")

    name = re.sub(r'\bENGG\b', 'ENGINEERING', name)
    name = re.sub(r'\bTECH\b', 'TECHNOLOGY', name)
    name = re.sub(r'\bSCI\b', 'SCIENCE', name)
    name = re.sub(r'\bINST\b', 'INSTITUTE', name)
    name = re.sub(r'\bINSTT\b', 'INSTITUTE', name)
    name = re.sub(r'\bCOLL\b', 'COLLEGE', name)
    name = re.sub(r'\bWOMENS\b', 'FOR WOMEN', name)
    name = re.sub(r'\bWOMEN\'S\b', 'FOR WOMEN', name)

    name = name.replace("COLLEGEEGE", "COLLEGE")

    if "GITAM" in name:
        name = "GITAM UNIVERSITY"

    if "MALLA REDDY" in name or "MALLAREDDY" in name:
        if name == "MALLAREDDY ENGINEERING COLLEGE": name = "MALLA REDDY COLLEGE OF ENGINEERING"
        if name == "MALLAREDDY INST OF ENGG AND TECHNOLOGY": name = "MALLAREDDY INSTITUTE OF ENGINEERING AND TECHNOLOGY"
        if name == "MALLAREDDY INST OF TECHNOLOGY AND SCI": name = "MALLAREDDY INSTITUTE OF TECHNOLOGY AND SCIENCE"
        if name == "MALLAREDDY COLLEGE OF ENGG TECHNOLOGY": name = "MALLA REDDY COLLEGE OF ENGINEERING TECHNOLOGY"
        if name == "MALLA REDDY ENGG COLLEGE FOR WOMEN": name = "MALLA REDDY ENGINEERING COLLEGE FOR WOMEN"

        is_mrew = "FOR WOMEN" in name
        is_mrem = "MANAGEMENT SCIENCES" in name
        is_mrits = "INSTITUTE OF TECHNOLOGY AND SCIENCE" in name
        is_mru = "UNIVERSITY" in name
        is_mrcet = "COLLEGE OF ENGINEERING TECHNOLOGY" in name and "MALLA REDDY" in name
        is_mriet = "INSTITUTE OF ENGINEERING AND TECHNOLOGY" in name and "MALLAREDDY" in name and not is_mrits
        is_mrit_short = "INSTITUTE OF TECHNOLOGY" in name and "MALLAREDDY" in name and not is_mrits and not is_mriet
        
        if is_mrew and not is_mrem: name = "MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN"
        elif is_mrem: name = "MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES"
        elif is_mrits: name = "MALLAREDDY INSTITUTE OF TECHNOLOGY AND SCIENCE"
        elif is_mru: name = "MALLA REDDY UNIVERSITY"
        elif is_mrcet: name = "MALLA REDDY COLLEGE OF ENGINEERING TECHNOLOGY"
        elif is_mriet: name = "MALLAREDDY INSTITUTE OF ENGINEERING AND TECHNOLOGY"
        elif is_mrit_short: name = "MALLAREDDY INSTITUTE OF TECHNOLOGY"
        elif "MALLA REDDY COLLEGE OF ENGINEERING" in name and not any([is_mrew, is_mrem, is_mrcet, is_mru, is_mrits, is_mriet]):
             name = "MALLA REDDY COLLEGE OF ENGINEERING"

    name = name.replace(" FOR WOMEN", " FOR WOMEN") # Standardize spacing
    name = name.rstrip(',.')
    cleaned = ' '.join(name.split())
    return cleaned.strip()

# --- Data (Keep this directly in the script for now) ---
tech_leads_data_csv_str = """﻿,CollegeName,TotalRegistrations
1,SNIS - SREENIDHI INSTITUTE OF SCI AND TECHNOLOGY,116
2,VJEC - V N R VIGNAN JYOTHI INSTITUTE OF ENGG AND TECH,83
3,ANUG - ANURAG UNIVERSITY (FORMERLY ANURAG GRP OF INSTNS- CVSR COLL OF ENGG),68
4,GCTC - GEETHANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),49
5,MRCE - MALLA REDDY COLLEGE OF ENGINEERING,35
6,KGRH - KG REDDY COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),32
7,STLW - STANLEY COLLEGE OF ENGG AND TECHNOLOGY FOR WOMEN (AUTONOMOUS),30
8,MGIT - MAHATMA GANDHI INSTITUTE OF TECHNOLOGY,30
9,GRRR - GOKARAJU RANGARAJU INSTITUTE OF ENGG AND TECH,27
10,JNTH - JNTU COLLEGE OF ENGG HYDERABAD,27
11,BVRI - B V RAJU INSTITUTE OF TECHNOLOGY,26
12,NNRG - NALLA NARASIMHA REDDY EDNL SOC GRP OF INSTNS,21
13,SPEC - ST PETERS ENGINEERING COLLEGE (AUTONOMOUS),19
14,NREC - NALLAMALLA REDDY ENGINEERING COLLEGE (AUTONOMOUS),19
15,BITN - BALAJI INSTITUTE OF TECHNOLOGY AND SCI,18
16,VAGE - VAAGDEVI COLLEGE OF ENGINEERING,15
17,VJIT - VIDYAJYOTHI INSTITUTE OF TECHNOLOGY,11
18,MECS - MATRUSRI ENGINEERING COLLEGE,10
19,VMEG - VARDHAMAN COLLEGE OF ENGINEERING,9
20,VIT - VELLORE INSTITUTE OF TECHNOLOGY,9
21,IITT - INDUR INSTITUTE OF ENGINEERING AND TECHNOLOGY,8
22,College,6
23,GLWC - GOKARAJU LAILAVATHI WOMENS ENGINEERING COLLEGE,6
24,VGNT - VIGNAN INSTITUTE OF TECHNOLOGY AND SCI,6
25,GNTW - G NARAYNAMMA INSTITUTE OF TECHNOLOGY AND SCI,6
26,BVRW - BVRIT COLLEGE OF ENGINEERING FOR WOMEN,6
27,VMTW - VIGNANS INST OF MANAGEMENT AND TECH FOR WOMEN,5
28,OUCE - OSMANIA UNIVERSITY COLLEGE OF ENGINEERING,5
29,MLRS - MARRI LAXMAN REDDY INST OF TECHNOLOGY AND MANAGEMENT (AUTONOMOUS),4
30,JBIT - J B INSTITUTE OF ENGG AND TECHNOLOGY,4
31,GCTC - GEETHANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),4
32,MRTN - ST MARTINS ENGINEERING COLLEGE (AUTONOMOUS),3
33,SRHP - SR UNIVERSITY ( FORMERLY S R ENGINEERING COLLEGE),3
34,SMSK - SAMSKRUTHI COLLEGE OF ENGG AND TECHNOLOGY,3
35,BREW - BHOJREDDY ENGINEERING COLLEGE FOR WOMEN,3
36,VBIT - VIGNAN BHARATI INSTITUTE OF TECHNOLOGY (AUTONOMOUS),2
37,MVGR COLLEGE OF ENGINEERING,2
38,GITAM HYDERABAD,2
39,MLID - M L R INSTITUTE OF TECHNOLOGY,2
40,JNTHMT - JNTUH-5 YEAR INTEGRATED MTECH SELF FINANCE,2
41,INDI - SRI INDU INSTITUTE OF ENGINEERING AND TECHNOLOGY,2
42,MLRD - MALLA REDDY COLLEGE OF ENGG TECHNOLOGY (AUTONOMOUS),2
43,VGWL - VAGDEVI ENGINEERING COLLEGE,2
44,GNIT - GURUNANAK INST OF TECHNOLOGY,1
45,GEETHANJALI COLLEGE OF ENGINEERING AND TECHNOLOGY,1
46,GLWC - GOKARAJU LAILAVATHI ENGINEERING COLLEGE,1
47,AMRITA VISHWA VIDHYAPEETHAM,1
48,ANRK - ANURAG ENGINEERING COLLGE,1
49,ACEG - A C E ENGINEERING COLLEGE (AUTONOMOUS),1
50,GITAM - GITAM UNIVERSITY,1
"""

ai_developers_data_csv_str = """﻿,CollegeName,TotalRegistrations
1,ANUG - ANURAG UNIVERSITY (FORMERLY ANURAG GRP OF INSTNS- CVSR COLL OF ENGG),997
2,CMRK - C M R COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),575
3,JNTH - JNTU COLLEGE OF ENGG HYDERABAD,550
4,VMEG - VARDHAMAN COLLEGE OF ENGINEERING,536
5,VJEC - V N R VIGNAN JYOTHI INSTITUTE OF ENGG AND TECH,458
6,MLID - M L R INSTITUTE OF TECHNOLOGY,456
7,COLLEGE,412
8,MVSR - M V S R ENGINEERING COLLEGE (AUTONOMOUS),368
9,SNIS - SREENIDHI INSTITUTE OF SCI AND TECHNOLOGY,357
10,BVRW - BVRIT COLLEGE OF ENGINEERING FOR WOMEN,328
11,VJIT - VIDYAJYOTHI INSTITUTE OF TECHNOLOGY,299
12,GCTC - GEETHANJALI COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS),256
13,CBIT - CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY,249
14,STLW - STANLEY COLLEGE OF ENGG AND TECHNOLOGY FOR WOMEN (AUTONOMOUS),224
15,GRRR - GOKARAJU RANGARAJU INSTITUTE OF ENGG AND TECH,224
16,IARE - INSTITUTE OF AERONAUTICAL ENGINEERING,202
17,MLRD - MALLA REDDY COLLEGE OF ENGG TECHNOLOGY (AUTONOMOUS),189
18,RITW - RISHI MS INST OF ENGG AND TECH FOR WOMEN,169
19,CMRG - CMR TECHNICAL CAMPUS (AUTONOMOUS),158
20,MGIT - MAHATMA GANDHI INSTITUTE OF TECHNOLOGY,144
21,MECS - MATRUSRI ENGINEERING COLLEGE,137
22,GITAM,131
23,VGWL - VAGDEVI ENGINEERING COLLEGE,129
24,PALV - PALLAVI ENGINEERING COLLEGE,128
25,KPRT - KOMMURI PRATAP REDDY INST OF TECHNOLOGY,128
26,MRCW - MALLA REDDY ENGG COLLEGE FOR WOMEN (AUTONOMOUS),123
27,GNTW - G NARAYNAMMA INSTITUTE OF TECHNOLOGY AND SCI,121
28,MRCE - MALLA REDDY COLLEGE OF ENGINEERING,118
29,BVRI - B V RAJU INSTITUTE OF TECHNOLOGY,114
30,VASV - VASAVI COLLEGE OF ENGINEERING,108
31,NRCM - NARSIMHAREDDY ENGINEERING COLLEGE (AUTONOMOUS),106
32,VIGNANA BHARATHI INSTITUTE OF TECHNOLOGY,105
33,MLRS - MARRI LAXMAN REDDY INST OF TECHNOLOGY AND MANAGEMENT (AUTONOMOUS),104
34,NREC - NALLAMALLA REDDY ENGINEERING COLLEGE (AUTONOMOUS),98
35,NNRG - NALLA NARASIMHA REDDY EDNL SOC GRP OF INSTNS,97
36,OUCE - O U COLLEGE OF ENGG HYDERABAD,94
37,SPEC - ST PETERS ENGINEERING COLLEGE (AUTONOMOUS),94
38,ACEG - A C E ENGINEERING COLLEGE (AUTONOMOUS),91
39,SDEW - SRIDEVI WOMENS ENGINEERING COLLEGE,89
40,ICFAI,79
41,SRYS - SREYAS INST OF ENGG AND TECHNOLOGY,78
42,JBIT - J B INSTITUTE OF ENGG AND TECHNOLOGY,77
43,JAYA - JAYAMUKHI INSTITUTE OF TECHNOLOGY AND SCIS,75
44,VBIT - VIGNAN BHARATI INSTITUTE OF TECHNOLOGY (AUTONOMOUS),75
45,TKEM - TEEGALA KRISHNA REDDY ENGINEERING COLLEGE (AUTONOMOUS),72
46,JNTR - JNTU COLLEGE OF ENGINEERING RAJANNA SIRCILLA,69
47,VGNT - VIGNAN INSTITUTE OF TECHNOLOGY AND SCI,68
48,GD GOENKA UNIVERSITY,68
49,RAJEEV GANDHI MEMORIAL COLLEGE OF ENGINEERING AND TECHNOLOGY,63
50,KMIT - KESHAV MEMORIAL INST OF TECHNOLOGY,58
"""

@st.cache_data 
def load_and_process_data(tech_leads_csv, devs_csv):
    df_tech_leads = pd.read_csv(StringIO(tech_leads_csv), usecols=['CollegeName', 'TotalRegistrations'])
    df_devs = pd.read_csv(StringIO(devs_csv), usecols=['CollegeName', 'TotalRegistrations'])

    df_tech_leads.rename(columns={'CollegeName': 'College_Name', 'TotalRegistrations': 'Tech_Leads'}, inplace=True)
    df_devs.rename(columns={'CollegeName': 'College_Name', 'TotalRegistrations': 'Developers'}, inplace=True)

    df_tech_leads['Cleaned_Name'] = df_tech_leads['College_Name'].apply(clean_college_name)
    df_devs['Cleaned_Name'] = df_devs['College_Name'].apply(clean_college_name)

    df_tech_leads_agg = df_tech_leads.groupby('Cleaned_Name')['Tech_Leads'].sum().reset_index()
    df_devs_agg = df_devs.groupby('Cleaned_Name')['Developers'].sum().reset_index()

    df_merged = pd.merge(df_tech_leads_agg, df_devs_agg, on='Cleaned_Name', how='outer')
    df_merged.fillna(0, inplace=True)
    df_merged['Developers'] = df_merged['Developers'].astype(int)
    df_merged['Tech_Leads'] = df_merged['Tech_Leads'].astype(int)

    filter_out_list = [
        "NEXTWAVE", "NIAT", "VIT", "KLH", "KUWL", "IIITH", 
        "GOVERNMENT INSTITUTE OF ELECTRONICS", 
        "JNTUH-5 YEAR INTEGRATED MTECH SELF FINANCE", "COLLEGE",
        "ICFAI", "GD GOENKA UNIVERSITY", "AMRITA VISHWA VIDHYAPEETHAM"
    ]
    df_merged = df_merged[~df_merged['Cleaned_Name'].isin(filter_out_list)]
    df_merged = df_merged[(df_merged['Developers'] > 0) | (df_merged['Tech_Leads'] > 0)].copy().reset_index(drop=True)
    return df_merged

# MODIFIED: Function now returns the processed DataFrame along with the figure
def create_sankey_figure_and_get_df(df_merged_input):
    # Make a copy to avoid modifying the input DataFrame directly if it's cached
    df_merged_processed = df_merged_input.copy()

    IDEAL_DEVS_PER_TL = 20
    df_merged_processed['Link_Color'] = 'rgba(200, 200, 200, 0.7)'
    df_merged_processed['Imbalance_Status'] = 'Balanced or Other'

    for index, row in df_merged_processed.iterrows():
        devs, tls = row['Developers'], row['Tech_Leads']
        link_color_to_set, status_to_set = df_merged_processed.loc[index, 'Link_Color'], df_merged_processed.loc[index, 'Imbalance_Status']

        if devs > 0 and (tls == 0 or tls < np.ceil(devs / IDEAL_DEVS_PER_TL)):
            link_color_to_set = 'rgba(255,0,0,0.7)'
            status_to_set = 'Critically Needs Tech Leads (0 TLs)' if tls == 0 else 'Needs Tech Leads'
        elif tls > 0 and (devs == 0 or devs < tls * IDEAL_DEVS_PER_TL):
            link_color_to_set = 'rgba(0,0,255,0.7)'
            status_to_set = 'Critically Needs Dev Interns (0 Devs)' if devs == 0 else 'Needs Dev Interns'
        
        df_merged_processed.loc[index, ['Link_Color', 'Imbalance_Status']] = link_color_to_set, status_to_set

    dev_sorted_df = df_merged_processed.sort_values(by=['Developers', 'Cleaned_Name'], ascending=[False, True], kind='mergesort').reset_index(drop=True)
    tl_sorted_df = df_merged_processed.sort_values(by=['Tech_Leads', 'Cleaned_Name'], ascending=[False, True], kind='mergesort').reset_index(drop=True)

    sankey_node_display_labels, sankey_node_id_labels, sankey_node_colors_list = [], [], []
    sankey_node_x_coords, sankey_node_y_coords = [], []
    node_color_dev_side, node_color_tl_side = 'rgba(173,216,230,0.8)', 'rgba(255,223,186,0.8)'

    num_dev_nodes = len(dev_sorted_df)
    if num_dev_nodes > 0:
        for i, row_dev in dev_sorted_df.iterrows():
            name, dev_count = row_dev['Cleaned_Name'], row_dev['Developers']
            sankey_node_id_labels.append(f"{name}_Dev")
            sankey_node_display_labels.append(f"{name} ({dev_count} Dev Interns)")
            sankey_node_colors_list.append(node_color_dev_side)
            sankey_node_x_coords.append(0.01)
            sankey_node_y_coords.append(i / max(1, num_dev_nodes - 1) if num_dev_nodes > 1 else 0.5)

    num_tl_nodes = len(tl_sorted_df)
    if num_tl_nodes > 0:
        for i, row_tl in tl_sorted_df.iterrows():
            name, tl_count = row_tl['Cleaned_Name'], row_tl['Tech_Leads']
            sankey_node_id_labels.append(f"{name}_TL")
            sankey_node_display_labels.append(f"{name} ({tl_count} Tech Leads)")
            sankey_node_colors_list.append(node_color_tl_side)
            sankey_node_x_coords.append(0.99)
            sankey_node_y_coords.append(i / max(1, num_tl_nodes - 1) if num_tl_nodes > 1 else 0.5)

    sankey_node_dict = {label: i for i, label in enumerate(sankey_node_id_labels)}
    source_indices, target_indices, values, link_colors_for_sankey, link_hover_texts = [], [], [], [], []

    for _, row in df_merged_processed.iterrows():
        college_name, dev_count, tl_count = row['Cleaned_Name'], row['Developers'], row['Tech_Leads']
        link_color_from_df, status_text = row['Link_Color'], row['Imbalance_Status']
        source_node_id, target_node_id = f"{college_name}_Dev", f"{college_name}_TL"
        
        if source_node_id in sankey_node_dict and target_node_id in sankey_node_dict:
            source_indices.append(sankey_node_dict[source_node_id])
            target_indices.append(sankey_node_dict[target_node_id])
            values.append(max(1, dev_count + tl_count))
            link_colors_for_sankey.append(link_color_from_df)
            link_hover_texts.append(f"{college_name}<br>Dev Interns: {dev_count}<br>Tech Leads: {tl_count}<br>Status: {status_text}")

    if not source_indices: return None, df_merged_processed # Return None for fig, but still return df

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(pad=15, thickness=15, line=dict(color="black", width=0.5),
                  label=sankey_node_display_labels, color=sankey_node_colors_list,
                  x=sankey_node_x_coords, y=sankey_node_y_coords,
                  customdata=sankey_node_display_labels, hovertemplate='<b>%{customdata}</b><extra></extra>',
                  align="justify" 
                  ),
        link=dict(source=source_indices, target=target_indices, value=values,
                  color=link_colors_for_sankey, label=link_hover_texts,
                  hovertemplate='<br>%{label}<extra></extra>'))])
    
    fig.update_layout(
        font_size=10,
        height=max(800, len(df_merged_processed) * 21 + 200), 
        margin=dict(l=480, r=480, t=50, b=50) 
    )
    return fig, df_merged_processed # Return both

# --- Streamlit App ---
st.set_page_config(layout="wide") 

st.title("College Intern Imbalance: AI Dev Interns vs. Tech Leads")

st.markdown("""
**Ideal Ratio: 1 Tech Lead : 20 AI Dev Interns**

**Link Colors:**
- <span style='color:red; font-weight:bold;'>Red Link:</span> College primarily needs Tech Leads.
- <span style='color:blue; font-weight:bold;'>Blue Link:</span> College primarily needs AI Dev Interns.

Numbers on nodes: (Dev Interns) = AI Dev Intern count, (Tech Leads) = Tech Lead count.
""", unsafe_allow_html=True)


df_colleges_initial = load_and_process_data(tech_leads_data_csv_str, ai_developers_data_csv_str)

if df_colleges_initial.empty:
    st.warning("No data available after processing and filtering. Sankey diagram cannot be generated.")
else:
    # Generate the Sankey figure and get the DataFrame with imbalance status
    sankey_fig, df_colleges_with_status = create_sankey_figure_and_get_df(df_colleges_initial) 

    if sankey_fig:
        st.plotly_chart(sankey_fig, use_container_width=True)
        
        with st.expander("View Processed Data Table"):
            # Use df_colleges_with_status here as it contains the Link_Color and Imbalance_Status
            st.dataframe(df_colleges_with_status[['Cleaned_Name', 'Developers', 'Tech_Leads', 'Imbalance_Status', 'Link_Color']].sort_values(by='Developers', ascending=False))
    else:
        st.error("Could not generate the Sankey diagram.")