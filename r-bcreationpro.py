import streamlit as st
import numpy as np
import io
import scipy.io.wavfile as wavfile
from pydub import AudioSegment

# Configurazione
NOTE_MAP = {"-": 0, "Do": 261.63, "Re": 293.66, "Mi": 329.63, "Fa": 349.23, "Sol": 392.00, "La": 440.00, "Si": 493.88}
SR = 44100
DURATA_BATTUTA = 0.8 

# Generatore Toni
def generate_tone(freq, duration, type="sine"):
    if freq == 0: return np.zeros(int(SR * duration))
    t = np.linspace(0, duration, int(SR * duration), False)
    if type == "square": wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif type == "saw": wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    else: wave = np.sin(2 * np.pi * freq * t)
    return wave * 0.5

st.title("🎹 R&B Sequencer Pro - BPM Control")


# Gestione Stato per il Reset
if 'reset' not in st.session_state: st.session_state.reset = False

def reset_grid():
    st.session_state.reset = True
    st.rerun()

# Controllo BPM
bpm = st.slider("BPM (Velocità)", min_value=60, max_value=140, value=90)
durata_battuta = 60 / bpm # Calcolo dinamico della durata in secondi

def generate_tone(freq, duration, type="sine"):
    if freq == 0: return np.zeros(int(SR * duration))
    t = np.linspace(0, duration, int(SR * duration), False)
    if type == "square": wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif type == "saw": wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    else: wave = np.sin(2 * np.pi * freq * t)
    return wave * 0.3

# Griglia
strumenti = ["Basso", "Batteria", "Chitarra", "Archi"]
sequenza = {}

for instr in strumenti:
    st.write(f"### {instr}")
    cols = st.columns(4)
    seq = []
    for i in range(4):
        # Usiamo il session_state per gestire il valore del selectbox
        val = cols[i].selectbox(f"B{i+1}", list(NOTE_MAP.keys()), key=f"{instr}_{i}")
        seq.append(val)
    sequenza[instr] = seq

if st.button("Reset Griglia"):
    reset_grid()

if st.button("Genera Loop"):
    # Generazione tracce basata sul BPM attuale
    basso_loop = np.concatenate([generate_tone(NOTE_MAP[n]/2, durata_battuta, "square") for n in sequenza["Basso"]])
    chitarra_loop = np.concatenate([generate_tone(NOTE_MAP[n], durata_battuta, "sine") for n in sequenza["Chitarra"]])
    archi_loop = np.concatenate([generate_tone(NOTE_MAP[n]*2, durata_battuta, "saw") for n in sequenza["Archi"]])
    
    # Mix e Normalizzazione
    mix = (basso_loop + chitarra_loop + archi_loop)
    mix = mix / np.max(np.abs(mix)) if np.max(np.abs(mix)) > 0 else mix
    
    buffer = io.BytesIO()
    wavfile.write(buffer, SR, (mix * 32767).astype(np.int16))
    st.audio(buffer, format="audio/wav")

