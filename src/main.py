"""Screen, Draws and controls"""
import sys
import pygame
from config import *
from physics import Game
from bot import SimpleBot
from ui import FuentePixel, cargar_imagen, teñir

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AZUL = (90, 200, 255)
ROJO = (255, 90, 90)

def draw_text(screen, font, text, center):
    img = font.render(text)
    screen.blit(img, img.get_rect(center=center))


def draw_menu(screen, big, small):
    draw_text(screen, big, "PONG", (WIDTH // 2, 270))
    draw_text(screen, small, "PLAY!", (WIDTH // 2, 435))
    pygame.draw.line(screen, WHITE, (378, 482), (657, 482), 1)
    draw_text(screen, small, "ENTER", (WIDTH // 2, 540))


def draw_game(screen, game, big, small, sprites):
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, 0, 5, HEIGHT))
    screen.blit(sprites["paleta_izq"], game.left.rect)
    screen.blit(sprites["paleta_der"], game.right.rect)
    screen.blit(sprites["pelota"], game.ball.rect)
    draw_text(screen, big, str(game.score["left"]), (250, 45))
    draw_text(screen, big, str(game.score["right"]), (775, 45))
    draw_text(screen, small, "AI", (975, 38))


def draw_gameover(screen, game, big, small):
    msg = "YOU WIN" if game.winner == "left" else "AI WINS"
    draw_text(screen, big, msg, (WIDTH // 2, 300))
    draw_text(screen, small, "ENTER", (WIDTH // 2, 450))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    big = FuentePixel("PONGfont.png", escala=5)     # letras de 80 px
    small = FuentePixel("PONGfont.png", escala=3)   # letras de 48 px

    paleta = cargar_imagen("Paleta.png", (PADDLE_W, PADDLE_H))
    sprites = {
        "paleta_izq": teñir(paleta, AZUL),
        "paleta_der": teñir(paleta, ROJO),
        "pelota": cargar_imagen("Pelota.png", (BALL_SIZE, BALL_SIZE)),
    }

    game, bot = Game(), SimpleBot()
    scene = "menu"  # menu | game | gameover

    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                if scene in ("menu", "gameover"):
                    game.reset()
                    scene = "game"

        screen.fill(BLACK)
        if scene == "menu":
            draw_menu(screen, big, small)
        elif scene == "game":
            keys = pygame.key.get_pressed()
            p_dir = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
            game.update(dt, p_dir, bot.decide(game))
            draw_game(screen, game, big, small, sprites)
            if game.state == "gameover":
                scene = "gameover"
        else:
            draw_game(screen, game, big, small, sprites)
            draw_gameover(screen, game, big, small)
        pygame.display.flip()


if __name__ == "__main__":
    main()
