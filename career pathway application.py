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
st.title("Career Pathway Portal (Interactive)")

# Custom CSS for horizontal layout
st.markdown("""
<style>
.level-block {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 16px;
    padding: 10px 0px 30px 10px;
    margin-bottom: 20px;
    border-bottom: 1px dashed #ccc;
}
.role-box {
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    padding: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    width: 250px;
    min-width: 250px;
    flex-shrink: 0;
}
.Technical { background-color: #e3f2fd; }
.Analytical { background-color: #fff3e0; }
.Leadership { background-color: #e8f5e9; }
.Strategic { background-color: #f3e5f5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
This portal allows employees to visualize career progression and identify skill gaps for their desired roles.
""")

# Step 1: User inputs Employee ID
employee_id = st.text_input("Enter your Employee ID:", value="E101")

if employee_id in df_employee["Employee ID"].values:
    employee_row = df_employee[df_employee["Employee ID"] == employee_id].iloc[0]
    st.success(f"Welcome, {employee_row['Name']}! Your paygrade is: {employee_row['Paygrade']}")
else:
    st.warning("Employee ID not found. Using default user.")
    employee_row = df_employee.iloc[0]

# Step 2: User selects current role based on paygrade
available_roles = role_df[role_df['Paygrade'] == employee_row['Paygrade']]['Role'].tolist()
current_role = st.selectbox("Select your current role (based on paygrade):", available_roles)

# Get current role skill profile
current_info = role_df[role_df['Role'] == current_role]
current_info = current_info[current_info['Paygrade'] == employee_row['Paygrade']].iloc[0]
current_col = f"{current_info['Role']} & {current_info['Band']} & {current_info['Paygrade']}"
current_level = current_info['Paygrade Level']

# Step 3: Display career path
grouped = role_df.groupby("Paygrade Level")
st.markdown("---")
st.markdown("### Career Pathway")

selected_new_role = None

for level in sorted(grouped.groups.keys()):
    st.markdown(f"#### Paygrade Level {level}")
    st.markdown('<div class="level-block">', unsafe_allow_html=True)
    roles = grouped.get_group(level).sort_values("Role")

    html_blocks = ""

for _, row in roles.iterrows():
    role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
    highlight = role_key == current_col
    box_header = f"{'⭐ ' if highlight else ''}{row['Role']}"
    box_color = row['Category']
    
    skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Proficiency Required"})
    skill_info = skill_info[skill_info["Proficiency Required"] != '-']
    skills_list_html = ''.join([f"<li>{r['Skill']}: {r['Proficiency Required']}</li>" for _, r in skill_info.iterrows()])
    
    button_html = ""
    if not highlight and row["Paygrade Level"] >= current_level:
        compare_key = f"compare_{role_key.replace(' ', '_')}"
        # Since we can't trigger a Streamlit button from HTML directly, we keep track for fallback
        if st.button(f"Compare Skills with {row['Role']}", key=compare_key):
            selected_new_role = {
                "Role": row['Role'],
                "Band": row['Band'],
                "Paygrade": row['Paygrade'],
                "Level": row['Paygrade Level']
            }

    role_html = f"""
    <div class='role-box {box_color}'>
        <b>{box_header}</b><br>
        <small>({row['Paygrade']})</small><br><br>
        <details>
          <summary style='cursor:pointer;'>View Skills</summary>
          <ul style="text-align:left; padding-left:10px;">{skills_list_html}</ul>
        </details>
    </div>
    """
    html_blocks += role_html

st.markdown(f'<div class="level-block">{html_blocks}</div>', unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Skill Gap Analysis
if selected_new_role:
    new_info = selected_new_role
    if new_info["Level"] >= current_level:
        st.markdown("---")
        st.subheader(f"Skill Gap Analysis: {current_role} → {new_info['Role']}")
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
        st.table(gap_df)
    else:
        st.warning("Cannot compare roles below your current paygrade level.")
else:
    st.info("Click on any eligible role above to compare skill requirements with your current role.")
