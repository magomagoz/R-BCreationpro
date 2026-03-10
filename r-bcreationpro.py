import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile

# Mappatura frequenze standard
def get_freq(note):
    freqs = {"Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
    return freqs.get(note, 261.63)

# Generatore di tono con inviluppo (ADSR semplificato) per evitare clipping/click
def generate_tone(freq, duration=1.0, sr=44100):
    if freq == 0: return np.zeros(int(sr * duration))
    t = np.linspace(0, duration, int(sr * duration), False)
    wave = np.sin(2 * np.pi * freq * t)
    
    # Inviluppo per eliminare il "click" iniziale e finale
    fade = 0.05
    fade_samples = int(fade * sr)
    envelope = np.ones_like(wave)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    return wave * envelope

st.title("🎹 R&B Sound Studio - Pro Edition")

# Interfaccia input
basso_note = st.selectbox("Basso", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
rhodes_note = st.selectbox("Rhodes", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
chitarra_note = st.selectbox("Chitarra", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
archi_note = st.selectbox("Archi", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])

if st.button("Genera Riff"):
    sr = 44100
    durata = 1.0
    
    # Generazione coerente degli strumenti
    basso_wave = generate_tone(get_freq(basso_note)/2) if basso_note != "-" else np.zeros(int(sr * durata))
    rhodes_wave = generate_tone(get_freq(rhodes_note)) if rhodes_note != "-" else np.zeros(int(sr * durata))
    chitarra_wave = generate_tone(get_freq(chitarra_note)) if chitarra_note != "-" else np.zeros(int(sr * durata))
    archi_wave = generate_tone(get_freq(archi_note)*2) if archi_note != "-" else np.zeros(int(sr * durata))
    
    # Mix bilanciato: sommiamo le onde e normalizziamo il risultato
    mix = (basso_wave * 0.4) + (rhodes_wave * 0.3) + (chitarra_wave * 0.2) + (archi_wave * 0.1)
    
    # Normalizzazione per evitare distorsioni digitali (clipping)
    if np.max(np.abs(mix)) > 0:
        mix = mix / np.max(np.abs(mix))
    
    # Esportazione in formato wav per Streamlit
    buffer = io.BytesIO()
    wavfile.write(buffer, sr, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")
