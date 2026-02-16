import random
import numpy as np  # Per array facili, opzionale

# Scala pentatonica minore A (simile a tonalità R&B: A C D E G)
pentatonica_minore = [0, 3, 5, 7, 10]  # Semitoni da A

# Durate in battiti (4/4, BPM ~80-90 R&B lento/mid)
durata_note = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]  # Ottavi, quarti, ecc.

def genera_melodia(lunghezza=16, tonalita_base=0):
    """
    Genera una melodia casuale R&B-style.
    - lunghezza: numero di note
    - tonalita_base: trasposizione (es. 0=A, 3=C)
    """
    melodia = []
    altezza_precedente = 0  # Parte bassa per vibe intima
    
    for _ in range(lunghezza):
        # Logica R&B: preferisci note vicine (step piccoli), occasionali salti (melismi Braxton/Carey)
        step = random.choice([-2, -1, 0, 1, 2])  # Movimento melodico fluido
        salto_occasionale = random.random() < 0.2  # 20% chance salto emotivo
        if salto_occasionale:
            step += random.choice([-3, 3, 5])  # Salto tipo Braxton
        
        altezza = (altezza_precedente + step) % 12
        altezza = max(0, min(11, altezza))  # Limita ottava
        altezza += tonalita_base
        
        # Scegli dalla scala, arrotonda all'altezza più vicina
        nota_scala = min(pentatonica_minore, key=lambda x: abs(x - altezza))
        durata = random.choice(durata_note)
        
        melodia.append({
            'nota': nota_scala + tonalita_base,
            'durata': durata,
            'semitono': nota_scala  # Per debug
        })
        altezza_precedente = nota_scala
    
    return melodia

# Esempio di generazione
random.seed(42)  # Riproducibile
melodia = genera_melodia(16, tonalita_base=9)  # A minor-ish

print("Melodia generata (16 note, stile R&B Braxton/Carey):")
print("Nota (semitono rel.) | Durata (battiti) | Nome appross. (da A)")
for i, nota in enumerate(melodia):
    nome_nota = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'][nota['nota'] % 12]
    print(f"{i+1:2d}: {nota['semitono']:2d} ({nome_nota}) | {nota['durata']:4.2f}")
