# Micol Pinelli CVAIgent

Agente AI personale con chat bilingue (IT/EN), timeline professionale, skill map, certificazioni, infografica e progetti GitHub.

## Funzioni
- **Chat** bilingue grounded sul CV con RAG (FAISS + OpenRouter)
- **Timeline** professionale interattiva
- **Skill Map** migliorata con dati LinkedIn (competenze, approvazioni, categorie, punti di forza)
- **Certificazioni** da Learnn, UiPath, Microsoft, JIRA
- **Infografica** personale
- **GitHub Projects** con link ai repository e anteprime
- **Job Description Match** (analisi fit via LLM)
- Modello free selezionabile
- Reindicizzazione dati sotto

## Avvio locale
```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key_here"
streamlit run app.py
```

## Modelli free consigliati
- openrouter/free
- moonshotai/kimi-k2.5
- qwen/qwen3-next-80b-a3b-instruct:free
- meta-llama/llama-3.3-70b-instruct:free

## Deploy Streamlit Cloud
Inserisci OPENROUTER_API_KEY nei Secrets.

## Deploy Docker
```bash
docker build -t cv-agent .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="your_key_here" cv-agent
```
