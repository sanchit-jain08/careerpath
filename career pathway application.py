import streamlit as st
import pandas as pd

# ------------------ Data ------------------ #
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

# ------------------ Streamlit Config ------------------ #
st.set_page_config(layout="wide")
st.title("🚀 Career Pathway Portal")
st.markdown("This portal allows employees to visualize career progression and identify skill gaps for their desired roles.")

# ------------------ Step 1: PS Number Input ------------------ #
employee_id = int(st.text_input("Enter your PS Number:", value="101"))

if employee_id in df_employee["PS Number"].values:
    employee_row = df_employee[df_employee["PS Number"] == employee_id].iloc[0]
    st.success(f"Welcome, {employee_row['Name']}!")
else:
    st.warning("PS Number not found. Using default user.")
    employee_row = df_employee.iloc[0]

# ------------------ Step 2: Role Selection ------------------ #
available_roles = role_df[role_df['Paygrade'] == employee_row['Paygrade']]['Role'].tolist()
current_role = st.selectbox("Select your current role (based on paygrade):", available_roles, index=0)

current_info = role_df[(role_df['Role'] == current_role) & (role_df['Paygrade'] == employee_row['Paygrade'])].iloc[0]
current_col = f"{current_info['Role']} & {current_info['Band']} & {current_info['Paygrade']}"
current_level = current_info['Paygrade Level']

grouped = role_df.groupby("Paygrade Level")
query_params = st.query_params
selected_key = query_params.get("compare", [None])[0] if isinstance(query_params.get("compare"), list) else query_params.get("compare")
selected_new_role = None

# ------------------ Step 3: Career Ladder ------------------ #
st.markdown("### 🧭 Career Pathway")
for level in sorted(grouped.groups.keys()):
    roles = grouped.get_group(level)
    st.markdown(f"#### 🪜 Paygrade Level {level}")
    cols = st.columns(len(roles))

    for i, (_, row) in enumerate(roles.iterrows()):
        role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
        highlight = role_key == current_col

        with cols[i].expander(f"{'⭐ ' if highlight else ''}{row['Role']} ({row['Paygrade']})"):
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Required Level"})
            skill_info = skill_info[skill_info["Required Level"] != '-']

            def color_level(val):
                return 'background-color: lightgrey'
    

            styled_df = skill_info.style.applymap(color_level, subset=["Required Level"])
            st.dataframe(styled_df, use_container_width=True, height=280)

            if not highlight and row["Paygrade Level"] >= current_level:
                if st.button(f"🔍 Compare Skills", key=f"compare_{role_key}"):
                    st.query_params.update(compare=role_key)
                    st.rerun()
    st.markdown("---")

# ------------------ Step 4: Check for Compare Param ------------------ #
if selected_key:
    try:
        parts = selected_key.split(" & ")
        role_match = role_df[
            (role_df['Role'] == parts[0]) &
            (role_df['Band'] == parts[1]) &
            (role_df['Paygrade'] == parts[2])
        ].iloc[0]
        selected_new_role = {
            "Role": role_match["Role"],
            "Band": role_match["Band"],
            "Paygrade": role_match["Paygrade"],
            "Level": role_match["Paygrade Level"]
        }
    except:
        selected_new_role = None

# ------------------ Step 5: Skill Gap Section Anchor ------------------ #
st.markdown('<div id="gap_section"></div>', unsafe_allow_html=True)

# ------------------ Step 6: Skill Gap Analysis ------------------ #
if selected_new_role:
    new_info = selected_new_role
    if new_info["Level"] >= current_level:
        st.markdown("---")
        st.subheader(f"🧠 Skill Gap Analysis: {current_role} → {new_info['Role']}")
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

        def gap_color(val):
            if val == "New Skill":
                return "background-color: #f8d7da"
            elif val == "Good to have":
                return "background-color: #fff3cd"
            elif isinstance(val, int) and val > 0:
                return "background-color: #d1ecf1"
            else:
                return ""

        if not filtered_gap_df.empty:
            styled_gap = filtered_gap_df.style.applymap(gap_color, subset=["Gap"])
            st.dataframe(styled_gap, use_container_width=True, height=300)
        else:
            st.info("✅ No skill gaps found for the selected role.")
    else:
        st.warning("❌ Cannot compare roles below your current paygrade level.")
else:
    st.info("ℹ️ Click on any eligible role above to compare skill requirements with your current role.")
