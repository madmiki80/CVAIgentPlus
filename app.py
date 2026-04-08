import os
import json
from pathlib import Path
import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from collections import defaultdict
import re

from tabs.chat import render_chat_tab
from tabs.timeline import render_timeline_tab
from tabs.skills import render_skills_tab
from tabs.match import render_match_tab
from api import llm_answer, match_jd, build_context


def load_css():
    css_path = BASE_DIR / "styles.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "faiss_index"
CV_PATH = DATA_DIR / "micol_pinelli_cv_new.docx"
FACTS_PATH = DATA_DIR / "profile_facts.json"

PROFILE_FACTS = {
    "name": "Micol Pinelli",
    "headline": "Analista ERP · PM · RPA · BPM · AI Agent",
    "location": "Mantova, Italia",
    "summary_it": "Professionista con esperienza in analisi ERP, project management, RPA/BPM con AI, Web API e supporto al cliente.",
    "summary_en": "Professional with experience in ERP analysis, project management, RPA/BPM with AI, Web APIs, and customer support.",
    "strengths": [
        "Project management",
        "Analisi funzionale e tecnica",
        "Supporto al cliente",
        "Gestione team eterogenei",
        "Formazione e tutoraggio",
        "Curiosità verso nuove tecnologie"
    ]
}

TIMELINE = [
    ("2024 - oggi", "PM e Analista Soluzioni Custom per integrazione RPA con AI", "Centro Software S.p.A", "Analisi e sviluppo soluzioni custom su ERP, RPA e BPM con AI; supporto al cliente."),
    ("2019 - 2024", "PM e Analista Soluzioni Custom ERP", "Centro Software S.p.A", "Analisi e sviluppo soluzioni custom ERP, app reception multi-sede, backoffice presenze Cloud, tutoraggio stage."),
    ("2017 - 2019", "PM e Analista", "Touring Club Italiano (Touring Editore)", "Nuovo e-commerce, DEM targeting, API e flussi contenuti verso siti e app."),
    ("2008 - 2016", "PM, Web Designer, DB Admin e Analyst", "Touring Club Italiano", "Portali web, archivio digitale, CRM/BI, DB turistico-editoriale, help desk di secondo livello."),
    ("2006 - 2008", "Web Developer", "Dinamys S.r.l", "ASP/VBScript/JavaScript, SQL Server, Java/JSP/Ajax/XML/MySQL, batch e task.")
]

from collections import defaultdict
import re

def years_from_period(period: str) -> int:
    """
    Estrae anni di esperienza da stringhe tipo:
    '2008 - 2016', '2019 - 2024', '2024 - oggi'
    """
    now = 2026
    years = re.findall(r"\d{4}", period)
    if not years:
        return 0
    start = int(years[0])
    end = int(years[1]) if len(years) > 1 else now
    return max(0, end - start)


def compute_skill_years(timeline):
    skill_years = defaultdict(int)

    for period, role, company, summary in timeline:
        years = years_from_period(period)
        text = f"{role} {summary}".lower()

        if "pm" in text or "project" in text:
            skill_years["Project Management"] += years
        if any(k in text for k in ["erp", "rpa", "bpm", "ai"]):
            skill_years["ERP & Automation"] += years
        if any(k in text for k in ["developer", "svilupp", "asp", "java", "python"]):
            skill_years["Development"] += years
        if any(k in text for k in ["db", "sql", "database", "bi"]):
            skill_years["Data & DB"] += years
        if any(k in text for k in ["api", "web", "e-commerce", "portali"]):
            skill_years["Web & API"] += years

    # cap a 20 anni per leggibilità radar
    return {k: min(v, 20) for k, v in skill_years.items()}


SKILLS = {
    "ERP & Automation": ["ERP", "RPA", "BPM", "AI Agent", "Power Platform", "Web API"],
    "Programming": ["Python", "C#", "JavaScript", "Angular", "jQuery", "PHP", "ASP", "VBScript", "COBOL", "Ajax", "JSON", "XML"],
    "Data & Infra": ["MySQL", "SQL Server", "IIS", "Apache", "Git", "GitHub", "SVN"],
    "PM & Collaboration": ["Project Management", "Teamwork", "JIRA", "Confluence", "Trello", "Visio", "Office", "Tutoraggio"]
}

PRESETS = {
    "Italiano": [
        "Quali sono le competenze principali di Micol Pinelli?",
        "Riassumi il percorso professionale.",
        "Quali sono i suoi punti di forza?",
        "Con quali tecnologie ha lavorato?",
        "Scrivi una breve presentazione professionale.",
        "Ha esperienza in ERP, RPA e AI?"
    ],
    "English": [
        "What are Micol Pinelli's main skills?",
        "Summarize her career path.",
        "What are her strengths?",
        "Which technologies has she worked with?",
        "Write a short professional summary.",
        "Does she have experience in ERP, RPA, and AI?"
    ]
}

FREE_MODELS = ["openrouter/free", "meta-llama/llama-3.2-3b-instruct:free", "qwen/qwen3.6-plus:free", "deepseek/deepseek-r1:free"]

def load_csv_docs():
    import csv
    docs = []
    for csv_file in DATA_DIR.glob("*.csv"):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                content = f"File: {csv_file.name}\n"
                for row in reader:
                    content += "\n".join([f"{k}: {v}" for k, v in row.items() if v.strip()]) + "\n---\n"
                if content.strip():
                    docs.append(type("Doc", (), {"page_content": content, "metadata": {"source": str(csv_file)}})())
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    return docs


def load_docx_docs():
    docs = []
    for docx_file in DATA_DIR.glob("*.docx"):
        try:
            docs.extend(Docx2txtLoader(str(docx_file)).load())
        except Exception as e:
            print(f"Error loading {docx_file}: {e}")
    return docs


def ensure_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not FACTS_PATH.exists():
        FACTS_PATH.write_text(json.dumps(PROFILE_FACTS, ensure_ascii=False, indent=2), encoding="utf-8")


def load_vectorstore():
    ensure_data()
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENROUTER_EMBEDDINGS_MODEL", "text-embedding-3-small"),
        api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
    )
    if INDEX_DIR.exists():
        return FAISS.load_local(str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True)
    docs = []
    docs.extend(load_docx_docs())
    docs.append(type("Doc", (), {"page_content": FACTS_PATH.read_text(encoding="utf-8"), "metadata": {"source": str(FACTS_PATH)}})())
    docs.extend(load_csv_docs())
    chunks = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120).split_documents(docs)
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(str(INDEX_DIR))
    return vs


def reindex_data():
    import shutil
    if INDEX_DIR.exists():
        shutil.rmtree(INDEX_DIR)
    global vs, ctx, srcs
    vs = load_vectorstore()
    ctx, srcs = build_context(vs, "skills experience strengths ERP RPA BPM API project management")


def choose_model():
    return st.sidebar.selectbox("Free model", FREE_MODELS, index=0, key="model_select")


def badges(items):
    return "".join([f"<span class='chip'>{x}</span>" for x in items])


st.set_page_config(page_title="Micol Pinelli CVAIgent", page_icon="💼", layout="wide")
load_css()
ensure_data()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "Italiano"

with st.sidebar:
    st.title("⚙️ CVAIgent")
    # selected_lang = st.selectbox("Lingua / Language", ["Italiano", "English"], key="language_select")
    # st.session_state.language = selected_lang
    if st.button("Cambia lingua / Change language", key="change_language_button"):
        st.session_state.language = "English" if st.session_state.language == "Italiano" else "Italiano"
        st.rerun()
    model = choose_model()
    st.markdown("---")
    if st.button("🧹 Nuova chat / New chat", use_container_width=True, key="new_chat_button"):
        st.session_state.messages = []
        st.rerun()
    if st.button("🔄 Reindex Data / Reindicizza Dati", use_container_width=True, key="reindex_button"):
        with st.spinner("Reindicizzando dati..." if st.session_state.language == "Italiano" else "Reindexing data..."):
            reindex_data()
        st.success("Dati reindicizzati!" if st.session_state.language == "Italiano" else "Data reindexed!")
        st.rerun()
    #st.download_button("💾 Esporta cronologia JSON", json.dumps(st.session_state.messages, ensure_ascii=False, indent=2), "chat_history.json", "application/json", use_container_width=True)
    st.markdown("---")
    st.subheader("Domande rapide")
    for i, q in enumerate(PRESETS[st.session_state.language]):
        if st.button(q, key=f"p_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.pending = q
            st.rerun()
    st.markdown("---")
    st.caption("Modelli free OpenRouter, response grounded sul CV.")

st.markdown("<div class='hero'><h1>💼 Micol Pinelli CVAIgent</h1><p>Chat bilingue con modelli free, timeline professionale, skill map e job match.</p></div>", unsafe_allow_html=True)
st.markdown("""
<div class='metric-grid'>
  <div class='card metric'><div class='label'>Core</div><div class='value'>ERP · RPA · BPM · AI</div></div>
  <div class='card metric'><div class='label'>Background</div><div class='value'>PM · Analyst · Dev</div></div>
  <div class='card metric'><div class='label'>Languages</div><div class='value'>IT / EN</div></div>
  <div class='card metric'><div class='label'>LLM</div><div class='value'>OpenRouter Free</div></div>
</div>
""", unsafe_allow_html=True)

vs = load_vectorstore()
ctx, srcs = build_context(vs, "skills experience strengths ERP RPA BPM API project management")

if len(st.session_state.messages) == 0:
    st.info("Usa le domande rapide a sinistra oppure scrivi una domanda.")

chat_tab, timeline_tab, skills_tab, match_tab = st.tabs(["Chat", "Timeline", "Skill Map", "Job Match"])

with chat_tab:
    render_chat_tab(st.session_state, vs, model, st.session_state.language)

with timeline_tab:
    render_timeline_tab(TIMELINE)
    
with skills_tab:
    render_skills_tab(SKILLS, PROFILE_FACTS, st.session_state.language)
        
        

with match_tab:
    render_match_tab(vs, st.session_state.language, model)
