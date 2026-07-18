import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Tutor AI", page_icon="🎓")
st.title("🎓 Tutor AI Personale")

# Controllo se la chiave esiste nei secrets
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        
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
                response = model.generate_content(f"Sei un tutor esperto. Rispondi: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Errore durante l'inizializzazione: {e}")
else:
    st.error("Errore: La chiave 'GEMINI_API_KEY' non è stata trovata nei Secrets di Streamlit.")
