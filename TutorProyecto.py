import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (0, 0, 0)
RED = (255, 255, 255)

# Cargar imágenes
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")

# Tamaño del jugador y enemigo
player_size = 75
enemy_size = 50

# Lista para almacenar enemigos
enemies = []

# Posición inicial del jugador
player_x = 375
player_y = 1000

# Puntuación
score = 0

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Función para crear un nuevo enemigo
def crear_enemigo():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT // 2)
    enemies.append([enemy_x, enemy_y])

# Función principal del juego
def jugar(screen, font):
    global player_x, player_y, enemies, score
    clock = pygame.time.Clock()

    # Velocidad y dirección del jugador
    player_speed = 5
    player_direction = 0

    # Velocidad y dirección de los enemigos
    enemy_speed = 3

    # Tiempo entre creación de enemigos
    enemy_spawn_time = 1000  # en milisegundos
    pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_time)

    # Variable para controlar la visualización del mensaje de seguir jugando
    mostrar_seguir_jugando = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrar_resultado_pantalla(screen, font, f"¡Hasta luego! Gracias por jugar. Puntuación: {score}")
                guardar_puntuacion(score)

                screen.fill(WHITE)
                pygame.display.flip()

                mostrar_seguir_jugando = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_direction = -1
                elif event.key == pygame.K_RIGHT:
                    player_direction = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_direction = 0
            elif event.type == pygame.USEREVENT + 1:
                crear_enemigo()

        # Mover al jugador
        player_x += player_speed * player_direction

        # Limitar al jugador dentro de la pantalla
        player_x = max(0, min(WIDTH - player_size, player_x))

        # Mover a los enemigos hacia abajo
        for enemy in enemies:
            enemy[1] += enemy_speed

            # Verificar colisión con el jugador
            if (
                player_x < enemy[0] + enemy_size
                and player_x + player_size > enemy[0]
                and player_y < enemy[1] + enemy_size
                and player_y + player_size > enemy[1]
            ):
                mostrar_resultado_pantalla(screen, font, f"¡Has perdido! Puntuación: {score}")
                guardar_puntuacion(score)

                screen.fill(WHITE)
                pygame.display.flip()

                mostrar_seguir_jugando = True

        # Si se muestra el mensaje de seguir jugando, esperar la respuesta del jugador
        if mostrar_seguir_jugando:
            seguir_jugando = preguntar_seguir_jugando(screen, font)
            if seguir_jugando:
                reiniciar_juego()
                mostrar_seguir_jugando = False
            else:
                return  # Volver al menú principal

        # Incrementar la puntuación por cada enemigo que sale de la pantalla
        for enemy in enemies:
            if enemy[1] + enemy_size >= HEIGHT:
                # El enemigo ha salido de la pantalla
                score += 1

        # Eliminar todos los enemigos que han salido de la pantalla
        enemies = [enemy for enemy in enemies if enemy[1] + enemy_size < HEIGHT]

        screen.fill(WHITE)

        # Dibujar al jugador
        screen.blit(player_image, (player_x, player_y))

        # Dibujar a los enemigos
        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0], enemy[1]))

        # Mostrar la puntuación
        score_text = font.render(f"Puntuación: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del bucle
        clock.tick(60)

# Función para mostrar el menú
def mostrar_menu(screen, font):
    screen.fill(WHITE)
    opcion1 = font.render("1. Jugar", True, RED)
    opcion2 = font.render("2. Ver mejores puntuaciones", True, RED)
    opcion3 = font.render("3. Eliminar puntuaciones", True, RED)
    opcion4 = font.render("4. Instrucciones", True, RED)
    opcion5 = font.render("5. Salir", True, RED)

    screen.blit(opcion1, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(opcion2, (WIDTH // 2 - 150, HEIGHT // 2))
    screen.blit(opcion3, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    screen.blit(opcion4, (WIDTH // 2 - 125, HEIGHT // 2 + 100))
    screen.blit(opcion5, (WIDTH // 2 - 75, HEIGHT // 2 + 150))
    pygame.display.flip()

# Función para mostrar las mejores puntuaciones
def ver_mejores_puntuaciones(screen, font):
    try:
        with open("puntuaciones.txt", "r") as file:
            mejores_puntuaciones = file.readlines()
        if mejores_puntuaciones:
            mejores_puntuaciones = [int(puntuacion.strip()) for puntuacion in mejores_puntuaciones]
            mejores_puntuaciones.sort(reverse=True)
            screen.fill(WHITE)
            titulo_text = font.render("Mejores Puntuaciones:", True, RED)
            screen.blit(titulo_text, (WIDTH // 2 - 150, 50))
            for i, puntaje in enumerate(mejores_puntuaciones, 1):
                puntaje_text = font.render(f"{i}. {puntaje}", True, RED)
                screen.blit(puntaje_text, (WIDTH // 2 - 50, 50 + i * 30))
            pygame.display.flip()
            pygame.time.delay(1500)  
        else:
            screen.fill(WHITE)
            pygame.display.flip()
            mensaje_text = font.render("Lo sentimos,no hay puntuaciones registradas.", True, RED)
            screen.blit(mensaje_text, (WIDTH // 2 - 200, HEIGHT // 2 - 25))
            pygame.display.flip()
            pygame.time.delay(1000)  # Mostrar durante 5 segundos antes de volver al menú
    except FileNotFoundError:
        mensaje_text = font.render("Lo sentimos, no hay puntuaciones registradas.", True, RED)
        screen.blit(mensaje_text, (WIDTH // 2 - 200, HEIGHT // 2 - 25))
        pygame.display.flip()
        pygame.time.delay(1000)  # Mostrar durante 5 segundos antes de volver al menú

# Función para guardar la puntuación en el archivo
def guardar_puntuacion(puntuacion):
    try:
        with open("puntuaciones.txt", "a") as file:
            file.write(str(puntuacion) + "\n")
    except Exception as e:
        print(f"Error al guardar la puntuación: {e}")

# Función para preguntar al jugador si desea seguir jugando
def preguntar_seguir_jugando(screen, font):
    mensaje = font.render("¿Deseas seguir jugando? (Sí: 1, No: 2)", True, RED)
    screen.blit(mensaje, (WIDTH // 2 - 200, HEIGHT // 2 - 25))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                elif event.key == pygame.K_2:
                    return False

# Función para reiniciar el juego
def reiniciar_juego():
    global player_x, player_y, enemies, score
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    enemies = []
    score = 0

# Función para mostrar el resultado en la pantalla
def mostrar_resultado_pantalla(screen, font, mensaje):
    screen.fill(WHITE)
    resultado_text = font.render(mensaje, True, RED)
    screen.blit(resultado_text, (WIDTH // 1 - 800, HEIGHT // 1 - 25))
    pygame.display.flip()
    pygame.time.delay(2000)  # Mostrar durante 2 segundos antes de preguntar seguir jugando

# Función para eliminar las puntuaciones registradas
def eliminar_puntuaciones():
    try:
        open("puntuaciones.txt", "w").close()
        print("Puntuaciones eliminadas.")
    except Exception as e:
        print(f"Error al eliminar puntuaciones: {e}")

# Función para mostrar las instrucciones
def mostrar_instrucciones(screen, font):
    instrucciones_text = [
        "Instrucciones:",
        "1. Usa las teclas izquierda y derecha para mover a Panchi.",
        "2. Evita que las pelotas toquen a nuestro perrito.",
        "3. Cada pelota que sale de la pantalla suma un punto.",
        "4. ¡Diviértete ayudando a panchi y obtén la mayor puntuación posible!",
        "",
        "Presiona cualquier tecla para volver al menú."
    ]

    screen.fill(WHITE)
    for i, line in enumerate(instrucciones_text):
        instruccion_text = font.render(line, True, RED)
        screen.blit(instruccion_text, (WIDTH // 1 - 900, 50 + i * 30))
    pygame.display.flip()

    # Esperar a que el jugador regrese al menú
    esperar_tecla = True
    while esperar_tecla:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                esperar_tecla = False

# Función principal
def main():
    global WIDTH, HEIGHT, player_x, player_y, enemies, score
    WIDTH, HEIGHT = 900, 600
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    enemies = []
    score = 0

    # Inicializar la ventana de Pygame antes de mostrar el menú
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PanchiGol")

    font_menu = pygame.font.Font(None, 36)
    font_resultado = pygame.font.Font(None, 24)

    # Saludo de bienvenida
    bienvenida_text = [
        "¡Bienvenido!",
        "¡Diviértete y obten la mayor puntuación que puedas!"
    ]

    screen.fill(WHITE)
    for i, line in enumerate(bienvenida_text):
        bienvenida_line = font_menu.render(line, True, RED)
        screen.blit(bienvenida_line, (WIDTH // 2 - 300, 50 + i * 30))
    pygame.display.flip()
    pygame.time.delay(3000)  # Mostrar el saludo durante 3 segundos

    while True:
        mostrar_menu(screen, font_menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jugar(screen, font_resultado)
                elif event.key == pygame.K_2:
                    ver_mejores_puntuaciones(screen, font_resultado)
                elif event.key == pygame.K_3:
                    eliminar_puntuaciones()
                elif event.key == pygame.K_4:
                    mostrar_instrucciones(screen, font_menu)
                elif event.key == pygame.K_5:
                    mostrar_resultado_pantalla(screen, font_resultado, "¡Hasta luego! Gracias por jugar.")
                    pygame.time.delay(1000)  # Mostrar durante 2 segundos antes de cerrar
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()