from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_PATH = BASE_DIR / "data" / "inphographic.png"


def render_infographic_tab(language):
    st.subheader("Infografica" if language == "Italiano" else "Infographic")

    if IMG_PATH.exists():
        st.image(str(IMG_PATH))
    else:
        st.warning("Immagine non trovata." if language == "Italiano" else "Image not found.")
