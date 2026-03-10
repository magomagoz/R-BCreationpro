import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, Triangle
import io

# Funzione per generare frequenze semplici (MIDI to Hz)
def note_to_freq(note_name):
    notes = {"Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
    return notes.get(note_name, 0)


#def genera_audio(basso, rhodes, chitarra, archi, vol_b, vol_rh, vol_ch, vol_ar):
    
def genera_audio(basso, rhodes, chitarra, archi):
    # Generiamo un secondo di audio per ogni strumento
    # Nota: il basso usa una forma d'onda più cupa (Square), il Rhodes più pura (Sine)
    basso_wave = Square(note_to_freq(basso)/2).to_audio_segment(duration=1000) if basso != "-" else AudioSegment.silent(duration=1000)
    rhodes_wave = Sine(note_to_freq(rhodes)).to_audio_segment(duration=1000) if rhodes != "-" else AudioSegment.silent(duration=1000)
    chitarra_wave = Triangle(note_to_freq(chitarra)).to_audio_segment(duration=1000) if chitarra != "-" else AudioSegment.silent(duration=1000)
    archi_wave = Sawtooth(note_to_freq(archi) * 2).to_audio_segment(duration=1000) if archi != "-" else AudioSegment.silent(duration=1000)

    # Aggiungiamo i parametri di gain (in dB)
    # Esempio: -5dB per abbassare, +2dB per alzare
    basso_wave = basso_wave.apply_gain(-2) 
    rhodes_wave = rhodes_wave.apply_gain(-5)
    chitarra_wave = chitarra_wave.apply_gain(-8)
    archi_wave = archi_wave.apply_gain(-10)
    
    # Aggiungi un attacco di 50 millisecondi a ogni traccia
    basso_wave = basso_wave.fade_in(50)
    rhodes_wave = rhodes_wave.fade_in(50)
    chitarra_wave = chitarra_wave.fade_in(50)
    archi_wave = archi_wave.fade_in(50)
    
    # Ora puoi sommarli nel mix finale
    # Dopo aver applicato i guadagni, normalizza il mix finale
    mix = basso_wave.overlay(rhodes_wave).overlay(chitarra_wave).overlay(archi_wave)
    mix = mix.normalize(headroom=3.0) # Lascia 3dB di spazio per evitare distorsioni

    # Esportiamo in un buffer
    buffer = io.BytesIO()
    mix.normalize().export(buffer, format="wav")
    return buffer

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

st.title("🎹 R&B Sound Studio")

basso = st.selectbox("🎸 Basso Synth", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
rhodes = st.selectbox("🎹 Piano Rhodes", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
chitarra = st.selectbox("🎼 Chitarra Clean", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
archi = st.selectbox("🎻 Tappeto Archi / Synth", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])

# Pulsante di generazione
st.markdown("---")
if st.button("Genera Riff R&B"):
    if basso == "-" and rhodes == "-" and chitarra == "-" and archi == "-":
        st.warning("Seleziona almeno uno strumento!")
    else:
        st.success("✨ Il tuo Riff R&B è pronto!")
        audio_buffer = genera_audio(basso, rhodes, chitarra, archi, None, None, None, None)
        st.audio(audio_buffer, format="audio/wav")
                
        # Mostra il risultato in una card formattata
        st.info(f"""
        **Il tuo Arrangiamento:**
        * **Basso:** {basso}
        * **Rhodes:** {rhodes}
        * **Chitarra:** {chitarra}
        * **Archi:** {archi}
        """)
    
