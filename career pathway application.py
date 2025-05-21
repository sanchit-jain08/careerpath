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

# UI Styling for Grid-Based Career Map
st.set_page_config(layout="wide")
st.title("Career Pathway Portal (Visual Map)")

# Define category based on department
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

# CSS Styling
st.markdown("""
<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(6, 200px);
    grid-auto-rows: 120px;
    gap: 16px;
    justify-content: center;
    padding: 20px;
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
}
.Technical { background-color: #e3f2fd; }
.Analytical { background-color: #fff3e0; }
.Leadership { background-color: #e8f5e9; }
.Strategic { background-color: #f3e5f5; }
</style>
""", unsafe_allow_html=True)

st.markdown("### Visual Career Progression Map")
st.markdown('<div class="grid-container">', unsafe_allow_html=True)

# Sort by level, then role
sorted_roles = role_df.sort_values(by=["Paygrade Level", "Role"])
for _, row in sorted_roles.iterrows():
    box = f"<div class='role-box {row['Category']}'>{row['Role']}<br><small>({row['Paygrade']})</small></div>"
    st.markdown(box, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.info("This view visually organizes career pathways by paygrade level and department grouping. You can extend this with arrows or modals for deeper interactivity.")
