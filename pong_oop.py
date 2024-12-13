import random
import pygame
import sys

# Farben
HINTERGRUND = (0, 125, 255)
VORDERGRUND = (255, 255, 255)

# Konstanten
FENSTERHOEHE = 600
FENSTERBREITE = 800
SCHLAEGERABSTAND = 20
SCHLAEGERBREITE = 16
SCHLAEGERHOEHE = 90
BALLGROESSE = 10
SCHLAEGERGESCHWINDIGKEIT = 0.5
BALLGESCHWINDIGKEIT = 0.2

# Initialisierung
pygame.init()
bildschirm = pygame.display.set_mode((FENSTERBREITE, FENSTERHOEHE))
pygame.display.set_caption("Pong")
schriftart = pygame.font.Font("Ac437_Amstrad_PC.ttf", 50)


class Schlaeger:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, SCHLAEGERBREITE, SCHLAEGERHOEHE)
        self.y = y

    def bewege(self, hoch, runter):
        keys = pygame.key.get_pressed()
        if keys[hoch]:
            self.y -= SCHLAEGERGESCHWINDIGKEIT
        if keys[runter]:
            self.y += SCHLAEGERGESCHWINDIGKEIT

        self.y = max(0, min(self.y, FENSTERHOEHE - SCHLAEGERHOEHE))
        self.rect.y = round(self.y)


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bewegung_x = BALLGESCHWINDIGKEIT
        self.bewegung_y = BALLGESCHWINDIGKEIT

    def bewege(self):
        self.x += self.bewegung_x
        self.y += self.bewegung_y

        # Kollision oben/unten
        if self.y < BALLGROESSE or self.y > FENSTERHOEHE - BALLGROESSE:
            self.bewegung_y *= -1

    def reset(self):
        self.x = FENSTERBREITE / 2
        self.y = FENSTERHOEHE / 2

        ## Zufällige Geschwindigkeit und Richtung
        self.bewegung_x = BALLGESCHWINDIGKEIT * random.choice([-1, 1])
        self.bewegung_y = BALLGESCHWINDIGKEIT * random.choice([-1, 1])

        ## Zufälligen Winkel in Radiant berechnen (0 bis 2*pi)
        # winkel = random.uniform(0, 2 * math.pi)

        ## Geschwindigkeit basierend auf dem Winkel berechnen
        # self.bewegung_x = math.cos(winkel) * BALLGESCHWINDIGKEIT
        # self.bewegung_y = math.sin(winkel) * BALLGESCHWINDIGKEIT


class Spiel:
    def __init__(self):
        self.linker_schlaeger = Schlaeger(
            SCHLAEGERABSTAND, FENSTERHOEHE / 2 - SCHLAEGERHOEHE / 2
        )
        self.rechter_schlaeger = Schlaeger(
            FENSTERBREITE - SCHLAEGERABSTAND - SCHLAEGERBREITE,
            FENSTERHOEHE / 2 - SCHLAEGERHOEHE / 2,
        )
        self.ball = Ball(FENSTERBREITE / 2, FENSTERHOEHE / 2)
        self.punkte_links = 0
        self.punkte_rechts = 0

    def aktualisiere_punkte(self):
        if self.ball.x < BALLGROESSE:
            self.punkte_rechts += 1
            self.ball.reset()
        if self.ball.x > FENSTERBREITE - BALLGROESSE:
            self.punkte_links += 1
            self.ball.reset()

    def kollisionen_pruefen(self):
        ball_rect = pygame.Rect(
            self.ball.x - BALLGROESSE,
            self.ball.y - BALLGROESSE,
            2 * BALLGROESSE,
            2 * BALLGROESSE,
        )
        if ball_rect.colliderect(self.linker_schlaeger.rect):
            self.ball.x = self.linker_schlaeger.rect.right + BALLGROESSE
            self.ball.bewegung_x *= -1
        if ball_rect.colliderect(self.rechter_schlaeger.rect):
            self.ball.x = self.rechter_schlaeger.rect.left - BALLGROESSE
            self.ball.bewegung_x *= -1

    def zeichnen(self):
        bildschirm.fill(HINTERGRUND)
        pygame.draw.rect(bildschirm, VORDERGRUND, self.linker_schlaeger.rect)
        pygame.draw.rect(bildschirm, VORDERGRUND, self.rechter_schlaeger.rect)
        pygame.draw.circle(
            bildschirm, VORDERGRUND, (int(self.ball.x), int(self.ball.y)), BALLGROESSE
        )

        text_links = schriftart.render(str(self.punkte_links), True, VORDERGRUND)
        text_rechts = schriftart.render(str(self.punkte_rechts), True, VORDERGRUND)
        bildschirm.blit(text_links, (40, 20))
        bildschirm.blit(text_rechts, (FENSTERBREITE - 120, 20))

        pygame.display.flip()


def main():
    spiel = Spiel()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Beenden mit Tastendruck
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        spiel.linker_schlaeger.bewege(pygame.K_w, pygame.K_s)
        spiel.rechter_schlaeger.bewege(pygame.K_UP, pygame.K_DOWN)

        spiel.ball.bewege()
        spiel.kollisionen_pruefen()
        spiel.aktualisiere_punkte()
        spiel.zeichnen()


if __name__ == "__main__":
    main()
