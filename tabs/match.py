import streamlit as st
from api import build_context, match_jd

def render_match_tab(vs, language, model):
    st.subheader("Job description match")
    jd = st.text_area("JD", height=220, placeholder="Incolla qui la job description..." if language == "Italiano" else "Paste the job description here...", key="jd_text_area")
    if st.button("Analizza fit" if language == "Italiano" else "Analyze fit", use_container_width=True, key="analyze_button"):
        if jd.strip():
            ctx, srcs = build_context(vs, jd)
            ans, used_model = match_jd(jd, language, model, ctx)
            st.markdown(ans)
            st.caption(f"Model used: {used_model}")
            with st.expander("Fonti / Sources"):
                for s in srcs:
                    st.code(s)
        else:
            st.warning("Inserisci una job description." if language == "Italiano" else "Please paste a job description.")