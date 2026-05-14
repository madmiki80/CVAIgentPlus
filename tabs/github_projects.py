import base64
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
ICON_PATH = BASE_DIR / "data" / "github_icon.png"


def _icon_html(size=20):
    if ICON_PATH.exists():
        b64 = base64.b64encode(ICON_PATH.read_bytes()).decode()
        return f'<img src="data:image/png;base64,{b64}" width="{size}" height="{size}" style="vertical-align:middle">'
    return "🐙"


PROJECTS = [
    {
        "name": "AsteroidChecker",
        "github": "https://github.com/madmiki80/AsteroidChecker",
        "description": "App di consultazione asteroidi orbitanti intorno alla Terra da API NASA, realizzata per il concorso di Arkemis.",
        "preview": "https://asteroidchecker.streamlit.app/",
        "preview_label": "Anteprima QUI",
    },
    {
        "name": "CVAIgentPlus",
        "github": "https://github.com/madmiki80/CVAIgentPlus",
        "description": "Agente AI per CV personale che risponde a domande e mostra le competenze.",
        "preview": "https://cvaigentplusmp.streamlit.app/",
        "preview_label": "Anteprima QUI",
    },
    {
        "name": "BANDIAI",
        "github": "https://github.com/madmiki80/BANDIAI",
        "description": "Agente per ricerca associazioni sul territorio e selezione bandi del terzo settore, in collaborazione con Informatici di Quartiere.",
        "preview": None,
        "preview_label": "Anteprima ancora non rilasciata",
    },
]


def render_github_projects_tab(language):
    gh_icon = _icon_html()
    st.subheader("Progetti GitHub" if language == "Italiano" else "GitHub Projects")
    preview_text = "Anteprima" if language == "Italiano" else "Preview"
    not_released = "Anteprima ancora non rilasciata" if language == "Italiano" else "Preview not yet available"

    for p in PROJECTS:
        preview_html = ""
        label = not_released if not p["preview"] else f"🚀 {preview_text}"
        if p["preview"]:
            preview_html = f'<a href="{p["preview"]}" target="_blank" class="project-link">{label}</a>'
        else:
            preview_html = f'<span style="color:#94a3b8;font-size:0.9rem">⏳ {label}</span>'

        st.markdown(
            f"""
            <div class="panel">
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.4rem">
                    <span style="font-weight:700;font-size:1.15rem;color:#1e293b">{p["name"]}</span>
                    <a href="{p["github"]}" target="_blank" style="font-size:0.85rem;color:#4f46e5;text-decoration:none">{gh_icon} GitHub</a>
                </div>
                <div style="color:#475569;margin-bottom:0.4rem">{p["description"]}</div>
                <div>{preview_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
