import os
import pygame

# Mapeo de teclas a notas (usa las teclas: Z, X, C, V, B, N, M)
NOTE_MAPPING = {
    pygame.K_z: "Do",
    pygame.K_x: "Re",
    pygame.K_c: "Mi",
    pygame.K_v: "Fa",
    pygame.K_b: "Sol",
    pygame.K_n: "La",
    pygame.K_m: "Si"
}

# Instrumento que usaremos (asegúrate de haber generado previamente las notas en notes/piano)
INSTRUMENT = "piano"
NOTES_DIR = os.path.join("notes", INSTRUMENT)

# Inicializar pygame y pygame.mixer
pygame.init()
pygame.mixer.init()  # Inicializa el mezclador

# Precarga los sonidos usando pygame.mixer.Sound
SOUNDS = {}
for note in ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]:
    path = os.path.join(NOTES_DIR, f"{note}.wav")
    if os.path.exists(path):
        try:
            sound = pygame.mixer.Sound(path)
            SOUNDS[note] = sound
        except Exception as e:
            print(f"Error al cargar {path}: {e}")
    else:
        print(f"Archivo {path} no encontrado.")

# Configurar la ventana Pygame
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pianito Interactivo")
font = pygame.font.SysFont("Arial", 24)

def draw_piano_keys():
    """Dibuja las teclas del piano en la ventana."""
    key_width = WIDTH // 7
    for i, note in enumerate(["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]):
        rect = pygame.Rect(i * key_width, 0, key_width, HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Dibujar el contorno
        # Escribir el nombre de la nota en la parte inferior
        text = font.render(note, True, (0, 0, 0))
        text_rect = text.get_rect(center=(i * key_width + key_width // 2, HEIGHT - 30))
        screen.blit(text, text_rect)

def main():
    """Bucle principal del pianito interactivo.
    Se mantiene en ciclo y reproduce notas sin detener el flujo al presionar una tecla.
    """
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((200, 200, 200))
        draw_piano_keys()
        
        for event in pygame.event.get():
            print("Evento recibido:", event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in NOTE_MAPPING:
                    note_name = NOTE_MAPPING[event.key]
                    print(f"Reproduciendo nota: {note_name}")
                    if note_name in SOUNDS:
                        try:
                            SOUNDS[note_name].play()
                        except Exception as e:
                            print(f"Error al reproducir {note_name}: {e}")
        
        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()
