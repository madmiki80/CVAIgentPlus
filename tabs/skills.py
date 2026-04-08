import streamlit as st

def render_skills_tab(SKILLS, PROFILE_FACTS, language):
    st.subheader("Skill map")

    for group, items in SKILLS.items():
        skills_text = ", ".join(items)
        st.markdown(
            f"""
            <div class='panel'>
                <strong>{group}</strong>
                <div style='margin-top:0.45rem'>
                    {skills_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader(
        "Punti di forza" if language == "Italiano" else "Strengths"
    )

    for s in PROFILE_FACTS["strengths"]:
        st.markdown(f"- {s}")