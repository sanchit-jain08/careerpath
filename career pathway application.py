import streamlit as st
import pandas as pd

# Sample Role Data
roles_data = {
    "Role": [
        "Junior Developer", "Developer", "Senior Developer", "Lead Developer", "Architect",
        "Analyst", "Senior Analyst", "Manager", "Senior Manager", "Director", "Developer", "Senior Analyst"
    ],
    "Department": [
        "IT", "IT", "IT", "IT", "IT",
        "Business", "Business", "Management", "Management", "Executive", "IT", "IT"
    ],
    "Paygrade": [
        "PG1", "PG2", "PG3", "PG4", "PG5",
        "PG1", "PG2", "PG3", "PG4", "PG5", "PG3", "PG3"
    ],
    "Paygrade Level": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 3, 3],
    "Band": [
        "B1", "B1", "B2", "B2", "B3",
        "B1", "B1", "B2", "B2", "B3", "B2", "B2"
    ]
}
role_df = pd.DataFrame(roles_data)

# Add category for styling
def categorize(dept):
    if dept == "IT":
        return "Technical"
    elif dept == "Business":
        return "Analytical"
    elif dept == "Management":
        return "Leadership"
    elif dept == "Executive":
        return "Strategic"
    return "Other"

role_df['Category'] = role_df['Department'].apply(categorize)

# Skill Matrix Data with '-' indicating skill not required
skills = ["Python", "Data Analysis", "Project Management", "System Design", "Communication"]
skill_matrix_data = {"Skill": skills}
for index, row in role_df.iterrows():
    col_name = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
    skill_matrix_data[col_name] = [i + (index % 5) if (i + index) % 4 != 0 else '-' for i in range(5)]
skill_df = pd.DataFrame(skill_matrix_data)

# Employee DataFrame with Paygrade
df_employee = pd.DataFrame({
    "Employee ID": ["E101", "E102", "E103"],
    "Name": ["Alice", "Bob", "Charlie"],
    "Paygrade": ["PG2", "PG3", "PG4"]
})

# Streamlit App Config
st.set_page_config(layout="wide")
st.title("Career Pathway Portal")

st.markdown("""
This portal allows employees to visualize career progression and identify skill gaps for their desired roles.
""")

# Employee Input
employee_id = int(st.text_input("Enter your Employee ID:", value="8"))
if employee_id in df_employee["Employee ID"].values:
    employee_row = df_employee[df_employee["Employee ID"] == employee_id].iloc[0]
    st.success(f"Welcome, {employee_row['Name']}!")
else:
    st.warning("Employee ID not found. Using default user.")
    employee_row = df_employee.iloc[0]

# Filter roles based on paygrade
available_roles = role_df[role_df['Paygrade'] == employee_row['Paygrade']]['Role'].tolist()
current_role = st.selectbox("Select your current role (based on paygrade):", available_roles)

# Identify current role details
current_info = role_df[(role_df['Role'] == current_role) & (role_df['Paygrade'] == employee_row['Paygrade'])].iloc[0]
current_col = f"{current_info['Role']} & {current_info['Band']} & {current_info['Paygrade']}"
current_level = current_info['Paygrade Level']

# CSS for layout and arrows
st.markdown("""
    <style>
    .level-block {
        display: flex;
        overflow-x: auto;
        padding-bottom: 1rem;
        align-items: center;
        justify-content: flex-start;
    }
    .role-box {
        width: 250px;
        min-width: 250px;
        margin: 10px;
        border: 2px solid #DDD;
        padding: 10px;
        border-radius: 10px;
        background-color: #FAFAFA;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
    }
    .arrow-right {
        width: 40px;
        height: 30px;
        margin-left: -10px;
        margin-right: -10px;
    }
    .connector {
        display: flex;
        align-items: center;
    }
    .level-label {
        font-weight: bold;
        font-size: 1.2em;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Group by Paygrade Level
grouped = role_df.groupby("Paygrade Level")
selected_new_role = None

st.markdown("## 🛤 Career Pathway")

# Draw role pathway
sorted_levels = sorted(grouped.groups.keys())
for i, level in enumerate(sorted_levels):
    roles = grouped.get_group(level)
    st.markdown(f'<div class="level-label">Level {level}</div>', unsafe_allow_html=True)
    st.markdown('<div class="level-block">', unsafe_allow_html=True)

    for idx, (_, row) in enumerate(roles.iterrows()):
        role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
        highlight = role_key == current_col
        bg_color = "#FFF7D1" if highlight else "#FFFFFF"

        with st.container():
            with st.expander(f"{'⭐ ' if highlight else ''}{row['Role']}", expanded=False):
                skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Proficiency Required"})
                skill_info = skill_info[skill_info["Proficiency Required"] != '-']
                st.dataframe(skill_info, use_container_width=True, height=250)

                if not highlight and row["Paygrade Level"] >= current_level:
                    if st.button(f"Compare Skills", key=f"compare_{role_key}"):
                        selected_new_role = {
                            "Role": row['Role'],
                            "Band": row['Band'],
                            "Paygrade": row['Paygrade'],
                            "Level": row['Paygrade Level']
                        }

        # Draw horizontal arrow if not the last role in row
        if idx != len(roles) - 1:
            st.markdown('<svg class="arrow-right" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50">'
                        '<line x1="0" y1="25" x2="90" y2="25" stroke="gray" stroke-width="4"/>'
                        '<polygon points="90,20 100,25 90,30" fill="gray"/>'
                        '</svg>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Skill Gap Analysis Section
if selected_new_role:
    new_info = selected_new_role
    if new_info["Level"] >= current_level:
        st.markdown("---")
        st.subheader(f"📊 Skill Gap Analysis: {current_role} → {new_info['Role']}")
        new_col = f"{new_info['Role']} & {new_info['Band']} & {new_info['Paygrade']}"

        gap_df = skill_df[["Skill", current_col, new_col]].copy()
        gap_df.columns = ["Skill", "Your Level", "Required Level"]

        def compute_gap(row):
            if row["Required Level"] == '-' and row["Your Level"] != '-':
                return "Good to have"
            elif row["Required Level"] != '-' and row["Your Level"] == '-':
                return "New Skill"
            elif row["Required Level"] == '-' and row["Your Level"] == '-':
                return "Good to have"
            return int(row["Required Level"]) - int(row["Your Level"])

        gap_df["Gap"] = gap_df.apply(compute_gap, axis=1)
        filtered_gap_df = gap_df[gap_df["Gap"].apply(lambda x: isinstance(x, str) or x > 0)]
        if not filtered_gap_df.empty:
            st.dataframe(filtered_gap_df, use_container_width=True, height=300)
        else:
            st.info("✅ No skill gap found for the selected role.")
    else:
        st.warning("Cannot compare roles below your current level.")
else:
    st.info("Click on any eligible role above to compare skill requirements with your current role.")
