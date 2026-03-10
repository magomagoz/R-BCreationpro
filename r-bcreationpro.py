import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile

# Configurazione frequenze (Standard)
def get_freq(note):
    freqs = {"Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
    return freqs.get(note, 261.63) # Default Do se non trova la nota

# Generatore di forma d'onda con inviluppo per evitare click/sibilo
def generate_tone(freq, duration=1.0, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), False)
    # Onda sinusoidale
    wave = np.sin(2 * np.pi * freq * t)
    # Applica un fade-in/out di 50ms per eliminare il click di attacco
    fade = 0.05
    fade_samples = int(fade * sr)
    envelope = np.ones_like(wave)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    return wave * envelope

st.title("🎹 R&B Sound Studio")

# Input utente
basso_note = st.selectbox("Basso", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])
rhodes_note = st.selectbox("Rhodes", ["-", "Do", "Re", "Mi", "Fa", "Sol", "La", "Si"])

if st.button("Genera Riff"):
    sr = 44100
    durata = 1.0
    
    # Generazione coerente
    basso_wave = generate_tone(get_freq(basso_note)/2) if basso_note != "-" else np.zeros(int(sr * durata))
    rhodes_wave = generate_tone(get_freq(rhodes_note)) if rhodes_note != "-" else np.zeros(int(sr * durata))
    
    # Mix bilanciato (Somma e Normalizzazione)
    mix = (basso_wave * 0.5) + (rhodes_wave * 0.4)
    mix = mix / np.max(np.abs(mix)) # Normalizzazione finale
    
    # Esportazione
    buffer = io.BytesIO()
    wavfile.write(buffer, sr, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")
