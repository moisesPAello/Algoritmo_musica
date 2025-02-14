from pydub import AudioSegment
from pydub.generators import Sine
import simpleaudio as sa
import os

def crear_directorios():
    """Crea los directorios necesarios para guardar las notas y los acordes."""
    os.makedirs('notes', exist_ok=True)
    os.makedirs('chords', exist_ok=True)

def generar_nota(freq, note_name):
    """
    Genera una nota musical con una frecuencia específica y la guarda en un archivo .wav.
    
    Args:
        freq (float): Frecuencia de la nota (en Hz).
        note_name (str): Nombre de la nota (Ej: "Do", "Re").
    """
    # Crear un tono de la frecuencia dada con una duración de 0.5 segundos
    tone = Sine(freq).to_audio_segment(duration=500)
    # Aplicar efectos de ataque y liberación, y suavizar los agudos
    tone = tone.fade_in(50).fade_out(200).low_pass_filter(3000)
    # Guardar la nota en un archivo .wav
    filename = f"notes/{note_name}.wav"
    tone.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def generar_acorde(chord_name, chord_freqs):
    """
    Genera un acorde a partir de una lista de frecuencias y lo guarda en un archivo .wav.
    
    Args:
        chord_name (str): Nombre del acorde (Ej: "Do mayor").
        chord_freqs (list): Lista de frecuencias que forman el acorde.
    """
    # Crear un segmento de audio vacío para el acorde
    chord = AudioSegment.silent(duration=500)  # Duración de 0.5 segundos

    # Superponer cada frecuencia del acorde
    for freq in chord_freqs:
        tone = Sine(freq).to_audio_segment(duration=500)
        tone = tone.fade_in(50).fade_out(200).low_pass_filter(3000)
        chord = chord.overlay(tone)

    # Exportar el acorde a un archivo .wav
    filename = f"chords/{chord_name}.wav"
    chord.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def generar_escala(frequencies):
    """
    Genera una escala musical a partir de una lista de frecuencias y la guarda en un archivo .wav.
    
    Args:
        frequencies (list): Lista de frecuencias para la escala.
    """
    # Crear un segmento de audio vacío para la escala
    scale = AudioSegment.silent(duration=0)
    
    # Generar cada nota de la escala y agregarla al segmento de audio
    for freq in frequencies:
        tone = Sine(freq).to_audio_segment(duration=500)
        tone = tone.fade_in(50).fade_out(200).low_pass_filter(3000)
        scale += tone

    # Exportar la escala completa a un archivo .wav
    scale_filename = "scale.wav"
    scale.export(scale_filename, format="wav")
    print(f"Archivo guardado: {scale_filename}")
    
    # Reproducir la escala generada
    reproducir_audio(scale_filename)

def reproducir_audio(filepath):
    """
    Reproduce un archivo de audio .wav dado.
    
    Args:
        filepath (str): Ruta al archivo de audio .wav.
    """
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def main():
    """Función principal que organiza la creación de notas, acordes y escalas."""
    # Crear los directorios para guardar los archivos de notas y acordes
    crear_directorios()

    # Lista de frecuencias para la escala natural (Do, Re, Mi, Fa, Sol, La, Si)
    frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    note_names = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]

    # Generar y guardar cada nota en un archivo de audio separado con efectos
    for freq, note in zip(frequencies, note_names):
        generar_nota(freq, note)

    # Definir los acordes de la escala natural
    chords = [
        ("Do mayor", [261.63, 329.63, 392.00]),  # Do mayor
        ("Re menor", [293.66, 349.23, 440.00]),  # Re menor
        ("Mi menor", [329.63, 392.00, 493.88]),  # Mi menor
        ("Fa mayor", [349.23, 440.00, 523.25]),  # Fa mayor
        ("Sol mayor", [392.00, 493.88, 587.33]),  # Sol mayor
        ("La menor", [440.00, 523.25, 659.25]),  # La menor
        ("Si disminuido", [493.88, 587.33, 739.99])  # Si disminuido
    ]

    # Generar y guardar cada acorde
    for chord_name, chord_freqs in chords:
        generar_acorde(chord_name, chord_freqs)

    # Crear y guardar la escala completa
    generar_escala(frequencies)

if __name__ == "__main__":
    main()
