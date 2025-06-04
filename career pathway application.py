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
st.markdown("""
    <style>
        .header-container {
            background-color: #f0f2f6;
            padding: 30px;
            margin-bottom: 0px;
            text-align: center;
        }
        .header-title {
            font-size: calc(1.5rem + 1vw);
            font-weight: 800;
            color: #003366;
            margin-bottom: 10px;
        }
        .header-subtitle {
            font-size: calc(0.9rem + 0.3vw);
            color: #333333;
        }
        .input-wrapper {
            background-color: #f0f2f6;
            padding: 15px 20px;
        }
        label[data-testid="stWidgetLabel"] {
            font-weight: 600;
            background-color: #f0f2f6;
            font-size: 16px !important;
            color: #333333;
            padding: 8px
        }
        input[type="text"] {
            font-size: 16px !important;
            padding: 8px 10px !important;
            border: 1px solid #d4d4d4 !important;
            background-color: #f0f2f6 !important;
        }
    </style>
    <div class="header-container">
        <div class="header-title">🚀 Career Pathway Portal</div>
        <div class="header-subtitle">This portal helps to visualize career progression and identify skill gaps for their desired roles.</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 0px; height: 1px; background-color: #f0f2f6;'>", unsafe_allow_html=True)
# ------------------ Step 1: PS Number Input ------------------ #
employee_id = int(st.text_input("Enter your PS Number:", value="101"))

if employee_id in df_employee["PS Number"].values:
    employee_row = df_employee[df_employee["PS Number"] == employee_id].iloc[0]
    st.success(f"Welcome, {employee_row['Name']}!")
else:
    st.warning("PS Number not found. Using default user.")
    employee_row = df_employee.iloc[0]
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin: 5px 0; border: none; height: 1px; background-color: #f0f2f6;'>", unsafe_allow_html=True)
# ------------------ Step 2: Role Selection ------------------ #
available_roles = role_df[role_df['Paygrade'] == employee_row['Paygrade']]['Role'].tolist()
current_role = st.selectbox("Select your current role:", available_roles, index=0)

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
    st.markdown(f"#### Paygrade Level {level}")
    cols = st.columns(len(roles))

    for i, (_, row) in enumerate(roles.iterrows()):
        role_key = f"{row['Role']} & {row['Band']} & {row['Paygrade']}"
        highlight = role_key == current_col

        with cols[i].expander(f"{'⭐ ' if highlight else ''}{row['Role']}"):
            skill_info = skill_df[["Skill", role_key]].rename(columns={role_key: "Required Level"})
            skill_info = skill_info[skill_info["Required Level"] != '-']

            def color_level(val):
                return 'background-color: lightgrey'
    

            styled_df = skill_info
            st.dataframe(styled_df, use_container_width=True, height=280)

            if not highlight and row["Paygrade Level"] >= current_level:
                if st.button(f"🔍 Compare Skills", key=f"compare_{role_key}"):
                    st.query_params.update(compare=role_key)
                    st.rerun()
    st.markdown("<hr style='margin: 5px 0; border: none; height: 1px; background-color: #f0f2f6;'>", unsafe_allow_html=True)

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
