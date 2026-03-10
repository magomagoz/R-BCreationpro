import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="R&B Riff Station", page_icon="🎹", layout="centered")

# Stile personalizzato opzionale per dare un tocco R&B anni '90
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #e94560;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #d13d55;
        border-color: #d13d55;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione
st.title("🎹 R&B Riff Station - '90s Vibe")
st.write("Componi il tuo giro armonico ispirato a Toni Braxton, Janet Jackson, Monica e Brandy. Seleziona le note per ogni strumento:")

# Lista delle note (con pausa iniziale)
note = ["-", "Do", "Do#", "Re", "Mib", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "Sib", "Si"]

# Creiamo due colonne per un layout più compatto su iPad
col1, col2 = st.columns(2)

with col1:
    st.subheader("Groove & Basso")
    basso = st.selectbox("🎸 Basso Synth / Slap", note, index=0)
    rhodes = st.selectbox("🎹 Fender Rhodes", note, index=0)

with col2:
    st.subheader("Melodia & Atmosfera")
    chitarra = st.selectbox("🎼 Chitarra Clean", note, index=0)
    archi = st.selectbox("🎻 Tappeto Archi / Synth", note, index=0)

# Pulsante di generazione
st.markdown("---")
if st.button("Genera Riff R&B"):
    # Controllo se è stato inserito qualcosa
    if basso == "-" and rhodes == "-" and chitarra == "-" and archi == "-":
        st.warning("Ehi producer, inserisci almeno una nota per far partire la magia!")
    else:
        st.success("✨ Il tuo Riff R&B è pronto!")
        
        # Mostra il risultato in una card formattata
        st.info(f"""
        **Il tuo Arrangiamento:**
        * **Basso:** {basso}
        * **Rhodes:** {rhodes}
        * **Chitarra:** {chitarra}
        * **Archi:** {archi}
        """)
        
        st.write("🎵 *Immagina queste note suonate su un beat TR-808 lento (circa 85 BPM), con un po' di swing e tanto riverbero...*")
