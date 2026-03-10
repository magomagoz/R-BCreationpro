import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile

# Funzione per generare il tono con inviluppo
def generate_tone(freq, duration=0.5, sr=44100):
    if freq == 0: return np.zeros(int(sr * duration))
    t = np.linspace(0, duration, int(sr * duration), False)
    wave = np.sin(2 * np.pi * freq * t)
    fade = 0.05
    fade_samples = int(fade * sr)
    envelope = np.ones_like(wave)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    return wave * envelope

st.title("🎹 R&B Loop Station - 4 Battute")

# Definizione delle frequenze
note_map = {"Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}

# Input per ogni battuta
st.subheader("Componi la tua sequenza (4 battute)")
cols = st.columns(4)
basso_seq = [cols[i].selectbox(f"Battuta {i+1}", ["-", "Do", "Re", "Mi", "Fa", "Sol"], key=f"b_{i}") for i in range(4)]

if st.button("Genera il Loop R&B"):
    sr = 44100
    # Genera la sequenza concatenando le battute
    basso_loop = np.concatenate([generate_tone(note_map.get(n, 0)/2) if n != "-" else np.zeros(int(sr*0.5)) for n in basso_seq])
    
    # Normalizzazione finale
    mix = basso_loop / np.max(np.abs(basso_loop)) if np.max(np.abs(basso_loop)) > 0 else basso_loop
    
    buffer = io.BytesIO()
    wavfile.write(buffer, sr, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")
