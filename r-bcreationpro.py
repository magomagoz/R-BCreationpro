import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile

# Configurazione Frequenze (Ottava centrale)
NOTE_MAP = {"-": 0, "Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
SR = 44100


st.image("banner.png")

st.title("🎹 R&B Sequencer Pro (No Dependency Issues)")

# Parametri
bpm = st.slider("BPM", 60, 140, 90)
durata_battuta = 60 / bpm

def generate_wave(freq, duration, wave_type="sine"):
    if freq == 0: return np.zeros(int(SR * duration))
    t = np.linspace(0, duration, int(SR * duration), False)
    # Generazione forme d'onda
    if wave_type == "square": wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "saw": wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    else: wave = np.sin(2 * np.pi * freq * t)
    
    # Inviluppo per eliminare click
    fade = 0.02
    fade_samples = int(fade * SR)
    env = np.ones_like(wave)
    env[:fade_samples] = np.linspace(0, 1, fade_samples)
    env[-fade_samples:] = np.linspace(1, 0, fade_samples)
    return wave * env

# Interfaccia Sequencer
strumenti = {"Basso": "square", "Chitarra": "sine", "Archi": "saw"}
sequenza = {}

for instr, w_type in strumenti.items():
    st.write(f"### {instr}")
    cols = st.columns(4)
    sequenza[instr] = [cols[i].selectbox(f"B{i+1}", list(NOTE_MAP.keys()), key=f"{instr}_{i}") for i in range(4)]

if st.button("Genera Loop"):
    # Costruzione traccia
    tracce = []
    for instr, w_type in strumenti.items():
        # Moltiplicatore ottava: 0.5 per Basso, 2.0 per Archi
        octave = 0.5 if instr == "Basso" else (2.0 if instr == "Archi" else 1.0)
        tracce.append(np.concatenate([generate_wave(NOTE_MAP[n]*octave, durata_battuta, w_type) for n in sequenza[instr]]))
    
    # Mix e Normalizzazione
    mix = sum(tracce)
    mix = mix / np.max(np.abs(mix)) if np.max(np.abs(mix)) > 0 else mix
    
    # Esporta
    buffer = io.BytesIO()
    wavfile.write(buffer, SR, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")

# Gestione Stato per il Reset
if 'reset' not in st.session_state: st.session_state.reset = False

def reset_grid():
    st.session_state.reset = True
    st.rerun()

st.divider()
if st.button("Reset Griglia"):
    reset_grid()
    
