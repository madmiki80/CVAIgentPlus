import streamlit as st

def render_timeline_tab(TIMELINE):
    st.subheader("Career Timeline")

    htmlcontent = '<div class="timeline-container">'
    for i, (period, role, company, summary) in enumerate(TIMELINE):
        htmlcontent += f'''
        <div class="timeline-item">
          <div class="timeline-content">
            <div class="period">{period}</div>
            <div class="role">{role}</div>
            <div class="company">{company}</div>
            <div class="summary">{summary}</div>
          </div>
        </div>'''
    htmlcontent += '</div>'
    st.markdown(htmlcontent, unsafe_allow_html=True)