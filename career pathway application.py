import streamlit as st
import pandas as pd

# Sample Role Data
roles_data = {
    "Role": [
        "Junior Developer", "Developer", "Senior Developer", "Lead Developer", "Architect",
        "Analyst", "Senior Analyst", "Manager", "Senior Manager", "Director"
    ],
    "Department": [
        "IT", "IT", "IT", "IT", "IT",
        "Business", "Business", "Management", "Management", "Executive"
    ],
    "Paygrade": [
        "PG1", "PG2", "PG3", "PG4", "PG5",
        "PG1", "PG2", "PG3", "PG4", "PG5"
    ],
    "Paygrade Level": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    "Band": [
        "B1", "B1", "B2", "B2", "B3",
        "B1", "B1", "B2", "B2", "B3"
    ]
}
role_df = pd.DataFrame(roles_data)

# Skill Matrix Data
skills = ["Python", "Data Analysis", "Project Management", "System Design", "Communication"]
skill_matrix_data = {"Skill": skills}
for index, row in role_df.iterrows():
    col_name = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
    skill_matrix_data[col_name] = [i + (index % 5) for i in range(5)]

skill_df = pd.DataFrame(skill_matrix_data)

# Streamlit App
st.set_page_config(layout="wide")
st.title("Career Pathway Portal (No Graphviz)")
st.markdown("""
This portal displays a career progression structure. Click on a role to view required skills.
""")

# Group roles by paygrade level
grouped = role_df.groupby("Paygrade Level")

# Display in a structured layout
for level in sorted(grouped.groups.keys()):
    st.markdown(f"### Paygrade Level {level}")
    roles = grouped.get_group(level)
    
    cols = st.columns(len(roles))  # dynamic columns for roles at this level
    for i, (_, row) in enumerate(roles.iterrows()):
        with cols[i].expander(row["Role"]):
            role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Proficiency Level"})
            st.table(skill_info)
