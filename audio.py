from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, Pulse
import simpleaudio as sa
import os

# Configuración de instrumentos
INSTRUMENTOS = {
    "piano": {
        "waveform": "sine",
        "attack": 50,
        "release": 200,
        "harmonics": [(1, 0), (2, -10), (3, -15)],  # (múltiplo, dB)
        "filtro": 3000
    },
    "guitarra": {
        "waveform": "square",
        "attack": 20,
        "release": 500,
        "harmonics": [(1, 0), (1.5, -8)],
        "filtro": 2000
    },
    "flauta": {
        "waveform": "sine",
        "attack": 10,
        "release": 300,
        "harmonics": [(1, 0)],
        "filtro": 5000
    }
}

def crear_directorios(instrumento):
    """Crea directorios específicos para cada instrumento."""
    os.makedirs(f"notes/{instrumento}", exist_ok=True)
    os.makedirs(f"chords/{instrumento}", exist_ok=True)

def generar_tono(freq, instrumento):
    """Genera un tono con el timbre del instrumento seleccionado."""
    config = INSTRUMENTOS[instrumento]
    tono_base = None
    
    # Generar armónicos
    for h, db in config["harmonics"]:
        if config["waveform"] == "sine":
            gen = Sine
        elif config["waveform"] == "square":
            gen = Square
        elif config["waveform"] == "sawtooth":
            gen = Sawtooth
        else:
            gen = Sine

        tono = gen(freq * h).to_audio_segment(duration=500)
        tono = tono.apply_gain(db)
        
        if tono_base:
            tono_base = tono_base.overlay(tono)
        else:
            tono_base = tono

    # Aplicar efectos
    return (tono_base.fade_in(config["attack"])
            .fade_out(config["release"])
            .low_pass_filter(config["filtro"]))

def generar_nota(freq, note_name, instrumento):
    """Genera y guarda una nota con el timbre del instrumento."""
    tono = generar_tono(freq, instrumento)
    filename = f"notes/{instrumento}/{note_name}.wav"
    tono.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def generar_acorde(chord_name, frecuencias, instrumento):
    """Genera un acorde con el timbre del instrumento seleccionado."""
    acorde = AudioSegment.silent(duration=500)
    
    for freq in frecuencias:
        tono = generar_tono(freq, instrumento)
        acorde = acorde.overlay(tono)
    
    filename = f"chords/{instrumento}/{chord_name}.wav"
    acorde.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def main():
    """Función principal para generar sonidos con diferentes instrumentos."""
    # Lista de instrumentos disponibles
    instrumentos = ["piano", "guitarra", "flauta"]
    
    # Frecuencias de la escala natural
    frecuencias = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    nombres_notas = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]

    # Acordes de la escala
    acordes = [
        ("Do mayor", [261.63, 329.63, 392.00]),
        ("Re menor", [293.66, 349.23, 440.00]),
        ("Mi menor", [329.63, 392.00, 493.88]),
        ("Fa mayor", [349.23, 440.00, 523.25]),
        ("Sol mayor", [392.00, 493.88, 587.33]),
        ("La menor", [440.00, 523.25, 659.25]),
        ("Si disminuido", [493.88, 587.33, 739.99])
    ]

    # Generar sonidos para cada instrumento
    for instrumento in instrumentos:
        crear_directorios(instrumento)
        
        # Generar notas
        for freq, nota in zip(frecuencias, nombres_notas):
            generar_nota(freq, nota, instrumento)
        
        # Generar acordes
        for nombre, frecs in acordes:
            generar_acorde(nombre, frecs, instrumento)

if __name__ == "__main__":
    main()