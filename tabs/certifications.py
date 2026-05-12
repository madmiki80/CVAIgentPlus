from pathlib import Path
import streamlit as st

CERTIFICATIONS = {
    "Learnn": [
        "Agenti AI",
        "AI Workflow",
        "Prompt & Skill Engineering",
        "Claude Chat & Cowork",
        "Vibe Coding MVP",
        "Lovable & Vibe Coding",
        "AI & ChatGPT",
        "Automazioni n8n, WhatsApp e CRM",
        "Cursor per marketer",
        "AI per il lavoro",
        "Project Management",
    ],
    "UiPath": [
        "Introduction to Automation",
        "Introduction to Agentic Automation",
    ],
    "Microsoft": [
        "Concetti fondamentali dell'intelligenza artificiale",
        "Nozioni fondamentali sull'intelligenza artificiale generativa",
        "Nozioni fondamentali sui servizi di intelligenza artificiale di Azure",
        "Creare soluzioni in linguaggio naturale con il Servizio OpenAI di Azure",
        "Configurazione di un modello semantico",
        "Gestire gli agenti in Microsoft Copilot Studio",
        "Implementare una soluzione di IA generativa responsabile in Microsoft Foundry",
        "Estrarre i dati dai moduli con Azure Document intelligence",
        "Scegliere un approccio Agile allo sviluppo software",
        "Valutare il processo di sviluppo software esistente",
        "Informazioni sulle potenzialità di Power BI",
        "Descrizione delle funzionalità di Microsoft Power BI",
        "Descrivere i modelli di Power BI Desktop",
        "Dati del modello in Power BI",
        "Recupero di dati con Power BI Desktop",
        "Introduzione a GitHub",
        "Introduzione ai prodotti GitHub",
        "Introduzione all'amministrazione GitHub",
        "Gestire un repository sicuro con le procedure consigliate per GitHub",
        "Introduzione alle app canvas di Power Apps",
        "Personalizzazione di un'app canvas in Power Apps",
        "Identificazione dei componenti di Microsoft Power Automate",
    ],
    "JIRA": [
        "Jira Work Management Fundamentals Badge",
    ],
}


def render_certifications_tab(language):
    st.subheader("Certificazioni" if language == "Italiano" else "Certifications")

    for authority, items in CERTIFICATIONS.items():
        items_html = "".join(f'<li>{c}</li>' for c in items)
        st.markdown(
            f"""
            <div class="panel">
                <div style="font-weight:700; font-size:1.1rem; color:#4f46e5; margin-bottom:0.45rem">{authority}</div>
                <ul style="margin:0; padding-left:1.2rem; color:#1e293b; line-height:1.7">{items_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
