import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="Tutor AI Personale", page_icon="🎓")

st.title("🎓 Tutor AI Personale")
st.write("Ciao! Sono qui per aiutarti a studiare. Inserisci la tua chiave e chiedimi quello che vuoi.")

# Input per la API Key (salvata nella sessione per non doverla riscrivere)
if "api_key" not in st.session_state:
    st.session_state.api_key = st.text_input("Inserisci la tua API Key di Gemini:", type="password")

if st.session_state.api_key:
    try:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Area di chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostra messaggi precedenti
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input utente
        if prompt := st.chat_input("Cosa vuoi imparare oggi?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(f"Sei un tutor scolastico esperto. Rispondi in modo incoraggiante e chiaro a: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Errore: {e}. Controlla che la API Key sia corretta.")
else:
    st.warning("Per favore, inserisci la tua API Key per iniziare.")
