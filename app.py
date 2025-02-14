from pydub import AudioSegment
from pydub.generators import Sine
import simpleaudio as sa
import os

def crear_directorios():
    os.makedirs('notes', exist_ok=True)
    os.makedirs('chords', exist_ok=True)

def generar_nota(freq, note):
    tone = Sine(freq).to_audio_segment(duration=500)  # Cada nota dura 0.5 segundos
    tone = tone.fade_in(50).fade_out(200)  # Simular ataque y liberación del piano
    tone = tone.low_pass_filter(3000)  # Suavizar el sonido eliminando agudos artificiales
    filename = f"notes/{note}.wav"
    tone.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def generar_acorde(chord_name, chord_freqs):
    # Crear un segmento de audio vacío para el acorde
    chord = AudioSegment.silent(duration=500)  # Duración de 0.5 segundos

    # Superponer cada frecuencia en el acorde
    for freq in chord_freqs:
        tone = Sine(freq).to_audio_segment(duration=500)
        tone = tone.fade_in(50).fade_out(200).low_pass_filter(3000)
        chord = chord.overlay(tone)

    # Exportar el acorde a un archivo .wav
    filename = f"chords/{chord_name}.wav"
    chord.export(filename, format="wav")
    print(f"Archivo guardado: {filename}")

def generar_escala(frequencies):
    scale = AudioSegment.silent(duration=0)
    for freq in frequencies:
        tone = Sine(freq).to_audio_segment(duration=500)
        tone = tone.fade_in(50).fade_out(200).low_pass_filter(3000)
        scale += tone
    scale_filename = "scale.wav"
    scale.export(scale_filename, format="wav")
    print(f"Archivo guardado: {scale_filename}")
    reproducir_audio(scale_filename)

def reproducir_audio(filepath):
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def main():
    crear_directorios()

    # Lista de frecuencias de la escala natural (Do, Re, Mi, Fa, Sol, La, Si)
    frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    note_names = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]

    # Generar y guardar cada nota en un archivo de audio separado con efecto de piano
    for freq, note in zip(frequencies, note_names):
        generar_nota(freq, note)

    # Generar y guardar los acordes de la escala natural
    chords = [
        ("Do", [261.63, 329.63, 392.00]),  # Do mayor
        ("Re", [293.66, 349.23, 440.00]),  # Re menor
        ("Mi", [329.63, 392.00, 493.88]),  # Mi menor
        ("Fa", [349.23, 440.00, 523.25]),  # Fa mayor
        ("Sol", [392.00, 493.88, 587.33]),  # Sol mayor
        ("La", [440.00, 523.25, 659.25]),  # La menor
        ("Si", [493.88, 587.33, 739.99])   # Si disminuido
    ]

    for chord_name, chord_freqs in chords:
        generar_acorde(chord_name, chord_freqs)

    # Crear y guardar la escala completa
    generar_escala(frequencies)

if __name__ == "__main__":
    main()
