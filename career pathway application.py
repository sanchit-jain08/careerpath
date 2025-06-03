import streamlit as st
import pandas as pd

# --- Sample Data ---
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

skills = ["Python", "Data Analysis", "Project Management", "System Design", "Communication"]
skill_matrix_data = {"Skill": skills}
for index, row in role_df.iterrows():
    col_name = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
    skill_matrix_data[col_name] = [i + (index % 5) if (i + index) % 4 != 0 else '-' for i in range(5)]
skill_df = pd.DataFrame(skill_matrix_data)

df_employee = pd.DataFrame({
    "PS Number": [101, 102, 103], 
    "Name": ["Alice", "Bob", "Charlie"],
    "Paygrade": ["PG2", "PG3", "PG4"]
})

# --- Streamlit Config ---
st.set_page_config(layout="wide")
st.title("🌱 Career Pathway Portal")

st.markdown("""
Welcome to the Career Pathway Portal!  
This portal helps visualize career progression and highlights the **skill gaps** you need to address for your next role.
""")

# --- Step 1: Employee ID Input ---
employee_id = st.text_input("Enter your PS Number:", value="8")
try:
    employee_id = int(employee_id)
except:
    st.warning("Invalid input. Defaulting to first employee.")
    employee_id = df_employee.iloc[0]["PS Number"]

if employee_id in df_employee["PS Number"].values:
    employee_row = df_employee[df_employee["PS Number"] == employee_id].iloc[0]
    st.success(f"👋 Welcome, {employee_row['Name']}!")
else:
    st.warning("PS Number not found. Using default user.")
    employee_row = df_employee.iloc[0]

# --- Step 2: Select Role ---
available_roles = role_df[role_df['Paygrade'] == employee_row['Paygrade']]['Role'].tolist()
current_role = st.selectbox("🎯 Select your current role (based on Paygrade):", available_roles, index=0)

current_info = role_df[(role_df['Role'] == current_role) & (role_df['Paygrade'] == employee_row['Paygrade'])].iloc[0]
current_col = f"{current_info['Role']} & {current_info['Band']} & {current_info['Paygrade']}"
current_level = current_info['Paygrade Level']

# --- Career Pathway ---
st.markdown("### 📈 Career Pathway Explorer")
grouped = role_df.groupby("Paygrade Level")

selected_new_role = None

for level in sorted(grouped.groups.keys()):
    roles = grouped.get_group(level)
    cols = st.columns(len(roles))

    for i, (_, row) in enumerate(roles.iterrows()):
        role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
        highlight = role_key == current_col

        with cols[i].expander(f"{'⭐ ' if highlight else ''}{row['Role']} ({row['Paygrade']})"):
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Required Level"})
            skill_info = skill_info[skill_info["Required Level"] != '-']

            def color_level(val):
                if val == '-':
                    return 'background-color: lightgrey'
                try:
                    val = int(val)
                    if val >= 4:
                        return 'background-color: #a1d99b'  # green
                    elif val >= 2:
                        return 'background-color: #fdae6b'  # orange
                    else:
                        return 'background-color: #fcbba1'  # red
                except:
                    return ''

            styled_df = skill_info.style.applymap(color_level, subset=["Required Level"])
            st.dataframe(styled_df, use_container_width=True, height=280)

            if not highlight and row["Paygrade Level"] >= current_level:
                if st.button(f"🔍 Compare Skills", key=f"compare_{role_key}"):
                    selected_new_role = {
                        "Role": row['Role'],
                        "Band": row['Band'],
                        "Paygrade": row['Paygrade'],
                        "Level": row['Paygrade Level']
                    }

# --- Step 4: Skill Gap Analysis ---
if selected_new_role:
    new_info = selected_new_role
    new_col = f"{new_info['Role']} & {new_info['Band']} & {new_info['Paygrade']}"

    st.markdown("---")
    st.subheader(f"🧠 Skill Gap Analysis: `{current_role}` ➞ `{new_info['Role']}`")

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

    def gap_color(val):
        if val == "New Skill":
            return "background-color: #fcbba1"
        elif isinstance(val, int) and val > 0:
            return "background-color: #fdd49e"
        return ""

    styled_gap = filtered_gap_df.style.applymap(gap_color, subset=["Gap"])
    if not filtered_gap_df.empty:
        st.dataframe(styled_gap, use_container_width=True, height=300)
    else:
        st.info("✅ No skill gaps found. You’re ready for the next role!")

else:
    st.info("Click on any eligible role above to compare skill requirements with your current role.")
