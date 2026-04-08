# Micol Pinelli CV Agent v4

Versione 4 con modelli free via OpenRouter.

## Funzioni
- chat bilingue grounded
- modello free selezionabile
- timeline professionale
- skill map
- job description match
- cronologia export JSON

## Avvio locale
```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key_here"
# opzionale
export OPENROUTER_API_BASE="https://openrouter.ai/api/v1"
streamlit run app.py
```

## Modelli free consigliati
- openrouter/free
- meta-llama/llama-3.2-3b-instruct:free
- qwen/qwen3.6-plus:free
- deepseek/deepseek-r1:free

## Deploy Streamlit Cloud
Inserisci OPENROUTER_API_KEY nei Secrets.

## Deploy Docker
```bash
docker build -t cv-agent-v4 .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="your_key_here" cv-agent-v4
```
