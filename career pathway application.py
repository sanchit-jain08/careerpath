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
