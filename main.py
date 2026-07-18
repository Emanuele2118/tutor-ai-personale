import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Tutor AI", page_icon="🎓")
st.title("🎓 Tutor AI Personale")

# Legge la chiave e rimuove eventuali a capo inseriti dal browser
try:
    raw_key = st.secrets["API_KEY"]
    api_key = raw_key.replace("\n", "").replace("\r", "")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Cosa vuoi imparare oggi?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(f"Sei un tutor scolastico esperto. Rispondi: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
except Exception as e:
    st.error("Errore di configurazione. Controlla i Secrets su Streamlit.")
