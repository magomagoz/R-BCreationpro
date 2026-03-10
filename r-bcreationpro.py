import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile

# Configurazione base
NOTE_MAP = {"-": 0, "Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
SR = 44100
DURATA_BATTUTA = 0.8 # Durata in secondi di ogni battuta

def generate_tone(freq, duration, type="sine"):
    if freq == 0: return np.zeros(int(SR * duration))
    t = np.linspace(0, duration, int(SR * duration), False)
    # Forme d'onda diverse per distinguere gli strumenti
    if type == "square": wave = np.sign(np.sin(2 * np.pi * freq * t)) # Basso
    elif type == "saw": wave = 2 * (t * freq - np.floor(0.5 + t * freq)) # Archi
    else: wave = np.sin(2 * np.pi * freq * t) # Rhodes/Chitarra
    
    # Fade per evitare click
    fade = 0.05
    fade_samples = int(fade * SR)
    env = np.ones_like(wave)
    env[:fade_samples] = np.linspace(0, 1, fade_samples)
    env[-fade_samples:] = np.linspace(1, 0, fade_samples)
    return wave * env

st.title("🎹 R&B Master Sequencer")

# Struttura dati: {Nome_Strumento: [Lista di 4 note]}
strumenti = ["Basso", "Batteria", "Chitarra", "Archi"]
sequenza = {}

# Creazione griglia
for instr in strumenti:
    st.write(f"### {instr}")
    cols = st.columns(4)
    seq = []
    for i in range(4):
        seq.append(cols[i].selectbox(f"B{i+1}", list(NOTE_MAP.keys()), key=f"{instr}_{i}"))
    sequenza[instr] = seq

if st.button("Genera Loop 4/4"):
    # Generazione tracce
    tracce = []
    
    # Basso (Square)
    tracce.append(np.concatenate([generate_tone(NOTE_MAP[n]/2, DURATA_BATTUTA, "square") * 0.4 for n in sequenza["Basso"]]))
    # Rhodes/Chitarra
    tracce.append(np.concatenate([generate_tone(NOTE_MAP[n], DURATA_BATTUTA, "sine") * 0.3 for n in sequenza["Chitarra"]]))
    # Archi (Saw)
    tracce.append(np.concatenate([generate_tone(NOTE_MAP[n]*2, DURATA_BATTUTA, "saw") * 0.2 for n in sequenza["Archi"]]))
    
    # Mix finale
    mix = sum(tracce)
    mix = mix / np.max(np.abs(mix)) if np.max(np.abs(mix)) > 0 else mix
    
    # Esporta
    buffer = io.BytesIO()
    wavfile.write(buffer, SR, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")
