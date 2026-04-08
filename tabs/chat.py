import streamlit as st
from api import llm_answer, build_context

def render_chat_tab(st_session_state, vs, model, language):
    for msg in st_session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    q = st.chat_input("Fai una domanda sul CV..." if language == "Italiano" else "Ask about the CV...", key="chat_input")
    if q:
        st.session_state.pending = q
        st.experimental_rerun()

    if getattr(st_session_state, 'pending', None):
        q = st_session_state.pending
        ctx, srcs = build_context(vs, q)
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            with st.spinner("Sto rispondendo..." if language == "Italiano" else "Thinking..."):
                answer, used_model = llm_answer(q, language, model, ctx)
                st.markdown(answer)
                st.caption(f"Model used: {used_model}")
                with st.expander("Fonti / Sources"):
                    for s in srcs:
                        st.code(s)
        st_session_state.messages.append({"role": "user", "content": q})
        st_session_state.messages.append({"role": "assistant", "content": answer})
        del st.session_state.pending
        st.rerun()
