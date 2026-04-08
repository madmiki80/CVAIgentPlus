import os
from openai import OpenAI

SYSTEM_PROMPT = """
You are Micol Pinelli's career assistant. Answer only using the provided profile documents.
Do not invent facts. Reply in the selected language. Keep it concise, recruiter-friendly, and grounded.
"""

FREE_MODELS = ["openrouter/free", "meta-llama/llama-3.2-3b-instruct:free", "qwen/qwen3.6-plus:free", "deepseek/deepseek-r1:free"]


def client():
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
        api_key=api_key,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost:8501"),
            "X-Title": "Micol Pinelli CVAIgent"
        }
    )


def build_context(vs, query):
    docs = vs.similarity_search(query, k=5)
    context = "\n\n".join([d.page_content for d in docs])
    sources = sorted({d.metadata.get("source", "unknown") for d in docs})
    return context, sources


def llm_answer(question, language, model, context):
    c = client()
    if c is None:
        return "Imposta OPENROUTER_API_KEY (o OPENAI_API_KEY) per usare l'app.", ""
    resp = c.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": "Rispondi in italiano." if language == "Italiano" else "Reply in English."},
            {"role": "user", "content": f"CONTESTO:\n{context}\n\nDOMANDA:\n{question}"}
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content, getattr(resp, "model", model)


def match_jd(job_description, language, model, context):
    c = client()
    if c is None:
        return "Imposta OPENROUTER_API_KEY per usare l'app.", ""
    prompt = (
        f"Valuta il fit del profilo di Micol Pinelli rispetto a questa job description.\n"
        f"Usa solo il contesto fornito.\n\nCONTESTO:\n{context}\n\nJOB DESCRIPTION:\n{job_description}\n\n"
        f"Restituisci: summary, alignment points, gaps, positioning." if language == "Italiano" else
        f"Evaluate Micol Pinelli's fit for this job description. Use only the provided context.\n\nCONTEXT:\n{context}\n\nJOB DESCRIPTION:\n{job_description}\n\nReturn: summary, alignment points, gaps, positioning."
    )
    resp = c.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content, getattr(resp, "model", model)
