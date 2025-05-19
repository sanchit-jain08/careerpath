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

# Sample Employee Data with Paygrade only
dummy_employees = {
    "E101": {"Name": "Alice", "Paygrade": "PG2"},
    "E102": {"Name": "Bob", "Paygrade": "PG3"},
    "E103": {"Name": "Charlie", "Paygrade": "PG4"}
}

# Streamlit App
st.set_page_config(layout="wide")
st.title("Career Pathway Portal (Interactive)")

st.markdown("""
This portal allows employees to visualize career progression and identify skill gaps for their desired roles.
""")

# Step 1: User inputs Employee ID
employee_id = st.text_input("Enter your Employee ID:", value="E101")

if employee_id in dummy_employees:
    employee = dummy_employees[employee_id]
    st.success(f"Welcome, {employee['Name']}! Your paygrade is: {employee['Paygrade']}")
else:
    st.warning("Employee ID not found. Using default user.")
    employee = dummy_employees["E101"]

# Step 2: User selects current role based on paygrade
available_roles = role_df[role_df['Paygrade'] == employee['Paygrade']]['Role'].tolist()
current_role = st.selectbox("Select your current role (based on paygrade):", available_roles)

# Get current role skill profile
current_info = role_df[role_df['Role'] == current_role].iloc[0]
current_col = f"{current_info['Role']} & {current_info['Band']} & {current_info['Paygrade']}"
current_skills = skill_df[["Skill", current_col]].rename(columns={current_col: "Current Proficiency"})

# Group roles by paygrade level
grouped = role_df.groupby("Paygrade Level")
st.markdown("---")
st.markdown("### Career Pathway")

# Step 3: Display career path with role highlights and interactivity
selected_new_role = None
for level in sorted(grouped.groups.keys()):
    st.markdown(f"#### Paygrade Level {level}")
    roles = grouped.get_group(level)
    cols = st.columns(len(roles))

    for i, (_, row) in enumerate(roles.iterrows()):
        highlight = row["Role"] == current_role
        with cols[i].expander(f"{'⭐ ' if highlight else ''}{row['Role']}"):
            role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Proficiency Required"})
            st.table(skill_info)

            if not highlight:
                if st.button(f"Compare Skills with {row['Role']}", key=f"compare_{row['Role']}"):
                    selected_new_role = row['Role']

# Step 4: Skill Gap Analysis
if selected_new_role:
    st.markdown("---")
    st.subheader(f"Skill Gap Analysis: {current_role} → {selected_new_role}")
    new_info = role_df[role_df['Role'] == selected_new_role].iloc[0]
    new_col = f"{new_info['Role']} & {new_info['Band']} & {new_info['Paygrade']}"

    gap_df = skill_df[["Skill", current_col, new_col]]
    gap_df.columns = ["Skill", "Your Level", "Required Level"]
    gap_df["Gap"] = gap_df["Required Level"] - gap_df["Your Level"]
    st.table(gap_df)
else:
    st.info("Click on any role above to compare skill requirements with your current role.")
