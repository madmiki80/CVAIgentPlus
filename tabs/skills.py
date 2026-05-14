import csv
from pathlib import Path
from collections import Counter
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


CATEGORY_MAP = {
    "ERP & Automation": [
        "ERP", "RPA", "Automation", "UiPath", "Agentic Automation",
        "Flussi di lavoro agentici", "Microsoft Power Apps",
        "Enterprise Resource Planning (ERP)", "ERP Software", "ERP Implementations",
    ],
    "Programming": [
        "Python", "C#", "JavaScript", "Angular", "Angular Material",
        "jQuery", "PHP", "ASP", "ASP.NET", "ASP.NET MVC", "AJAX",
        "JSON", "XML", "Java", "Entity Framework", "Entity Framework (EF) Core",
        ".NET Framework", "Model–view–controller (MVC)", "Front-end Development",
        "Programming", "Software Development",
    ],
    "Data & Infra": [
        "SQL", "Microsoft SQL Server", "MySQL", "Database Design",
        "Git", "Apache", "Windows", "Visual Studio", "Slack",
    ],
    "PM & Collaboration": [
        "Project Management", "JIRA", "Confluence", "Training", "Teaching",
        "Vocational Education", "Problem Solving", "Analysis",
        "Product Customization", "E-commerce", "Marketing via email",
        "Google Analytics", "CRM", "CMS",
    ],
    "Web & Design": [
        "Web Development", "Web Design", "Applicazioni Web",
        "Progressive Web Applications (PWAs)", "CSS", "HTML", "UML",
    ],
}


def _classify_skills(skills_list):
    grouped = {cat: [] for cat in CATEGORY_MAP}
    unmatched = []
    for s in skills_list:
        found = False
        for cat, keywords in CATEGORY_MAP.items():
            if s in keywords:
                grouped[cat].append(s)
                found = True
                break
        if not found:
            unmatched.append(s)
    if unmatched:
        grouped["Altro / Other"] = unmatched
    return grouped


def _load_endorsements():
    rows = _load_csv("Endorsement_Received_Info.csv")
    return Counter(
        row.get("Skill Name", "") for row in rows
        if row.get("Endorsement Status") == "ACCEPTED"
    )


def render_skills_tab(SKILLS, PROFILE_FACTS, language):
    t = lambda it, en: it if language == "Italiano" else en

    st.subheader(t("Mappa delle Competenze", "Skill Map"))

    # --- Load data ---
    raw_skills = _load_csv("Skills.csv")
    linkedin_skills = sorted(set(
        row.get("Name", "").strip()
        for row in raw_skills if row.get("Name")
    ), key=str.casefold)

    endorsements = _load_endorsements()
    grouped = _classify_skills(linkedin_skills)

    total_skills = len(linkedin_skills)
    total_endorsements = sum(endorsements.values())

    # --- Metric cards ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<div class='skill-metric'><div class='skill-metric-value'>{total_skills}</div>"
            f"<div class='skill-metric-label'>{t('Competenze', 'Skills')}</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='skill-metric'><div class='skill-metric-value'>{total_endorsements}</div>"
            f"<div class='skill-metric-label'>{t('Approvazioni', 'Endorsements')}</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='skill-metric'><div class='skill-metric-value'>{len(grouped)}</div>"
            f"<div class='skill-metric-label'>{t('Categorie', 'Categories')}</div></div>",
            unsafe_allow_html=True,
        )

    # --- Category cards ---
    gradient_colors = [
        ("#4f46e5", "#7c3aed"),
        ("#059669", "#10b981"),
        ("#d97706", "#f59e0b"),
        ("#dc2626", "#ef4444"),
        ("#0891b2", "#06b6d4"),
        ("#7c3aed", "#a855f7"),
    ]

    for i, (cat, skills) in enumerate(grouped.items()):
        if not skills:
            continue
        color1, color2 = gradient_colors[i % len(gradient_colors)]
        skills_html = "".join(
            f"<span class='skill-chip'>{s}</span>" for s in sorted(set(skills), key=str.casefold)
        )
        st.markdown(
            f"""
            <div class='skill-category-card' style='border-top:4px solid {color1}'>
                <div class='skill-category-header' style='color:{color1}'>
                    <span style='font-weight:700;font-size:1.1rem'>{cat}</span>
                    <span class='skill-count-badge' style='background:{color1}15;color:{color1}'>{len(skills)}</span>
                </div>
                <div class='skill-category-body'>{skills_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Strengths ---
    st.markdown(
        f"<div style='font-size:1.15rem;font-weight:700;color:#ffffff;margin:1.5rem 0 0.75rem 0;padding:0.5rem 1rem;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:10px'>{t('Punti di forza', 'Strengths')}</div>",
        unsafe_allow_html=True,
    )
    strengths_html = "".join(
        f"<span class='strength-chip'>⭐ {s}</span>" for s in PROFILE_FACTS["strengths"]
    )
    st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:0.5rem'>{strengths_html}</div>", unsafe_allow_html=True)
