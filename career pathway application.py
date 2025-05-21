import streamlit as st
import pandas as pd

# Sample Role Data
roles_data = {
    "Role": [
        "Junior Developer", "Developer", "Senior Developer", "Lead Developer", "Architect",
        "Analyst", "Senior Analyst", "Manager", "Senior Manager", "Director", "Developer","Senior Analyst"
    ],
    "Department": [
        "IT", "IT", "IT", "IT", "IT",
        "Business", "Business", "Management", "Management", "Executive", "IT","IT"
    ],
    "Paygrade": [
        "PG1", "PG2", "PG3", "PG4", "PG5",
        "PG1", "PG2", "PG3", "PG4", "PG5","PG3","PG3"
    ],
    "Paygrade Level": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 3, 3],
    "Band": [
        "B1", "B1", "B2", "B2", "B3",
        "B1", "B1", "B2", "B2", "B3", "B2", "B2"
    ]
}
role_df = pd.DataFrame(roles_data)

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


# Streamlit App
st.set_page_config(layout="wide")
st.title("Career Pathway Portal (Interactive)")

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

# Group roles by paygrade level
grouped = role_df.groupby("Paygrade Level")
st.markdown("---")
st.markdown("### Career Pathway")

# Step 3: Display career path with role highlights and interactivity
selected_new_role = None

# Inject CSS for horizontal scrolling and fixed width
st.markdown("""
    <style>
        .scroll-container {
            display: flex;
            overflow-x: auto;
            padding: 10px;
            gap: 16px;
        }
        .expander-wrapper {
            min-width: 300px;
            max-width: 300px;
            flex: 0 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

# Display expanders grouped by paygrade level in horizontal rows
for level in sorted(grouped.groups.keys()):
    st.markdown(f"#### Paygrade Level {level}")
    roles = grouped.get_group(level)

    # Start horizontal scroll container
    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

    for _, row in roles.iterrows():
        role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
        highlight = role_key == current_col
        expander_title = f"{'⭐ ' if highlight else ''}{row['Role']}"

        # Start expander wrapper
        st.markdown('<div class="expander-wrapper">', unsafe_allow_html=True)
        with st.expander(expander_title):
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Proficiency Required"})
            skill_info = skill_info[skill_info["Proficiency Required"] != '-']
            st.table(skill_info)

            if not highlight and row["Paygrade Level"] >= current_level:
                if st.button(f"Compare Skills with {row['Role']}", key=f"compare_{role_key}"):
                    selected_new_role = {
                        "Role": row['Role'],
                        "Band": row['Band'],
                        "Paygrade": row['Paygrade'],
                        "Level": row['Paygrade Level']
                    }
        # End expander wrapper
        st.markdown('</div>', unsafe_allow_html=True)

    # End horizontal scroll container
    st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Skill Gap Analysis (only for roles at or above current level)
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
