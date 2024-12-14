import pygame
import sys

# Init
pygame.init()

# Farben
HINTERGRUND = (0, 255, 255)
VORDERGRUND = (255, 255, 255)

# Konstanten
FENSTERHOEHE = 600
FENSTERBREITE = 800
FENSTERMITTEY = FENSTERHOEHE / 2
FENSTERMITTEX = FENSTERBREITE / 2

SCHLAEGERABSTAND = 20
SCHLAEGERBREITE = 16
SCHLAEGERHOEHE = 90
RECHTERSCHLAEGERX = FENSTERBREITE - SCHLAEGERABSTAND - SCHLAEGERBREITE
SCHLAEGERGESCHWINDIGKEIT = 0.5

BALLGROESSE = 10
BALLGESCHWINDIGKEIT = 0.1

# Fenster
bildschirm = pygame.display.set_mode((FENSTERBREITE, FENSTERHOEHE))
pygame.display.set_caption("Pong")

# Schlaegerposition
linkerSchlaegerY = 50
rechterSchlaegerY = 50

# Ballposition
ballX = FENSTERMITTEX
ballY = FENSTERMITTEY

ballbewegungX = BALLGESCHWINDIGKEIT
ballbewegungY = BALLGESCHWINDIGKEIT

a = 0
b = 0
# schriftart = pygame.font.SysFont("tuffy", 50, italic=True, bold=False)
schriftart = pygame.font.Font("Ac437_Amstrad_PC.ttf", 50)

texta = schriftart.render(str(a), True, pygame.Color(VORDERGRUND))
textb = schriftart.render(str(b), True, pygame.Color(VORDERGRUND))

clock = pygame.time.Clock()

# Mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Tastenaktionen
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_UP]:
        rechterSchlaegerY -= SCHLAEGERGESCHWINDIGKEIT
    if tasten[pygame.K_DOWN]:
        rechterSchlaegerY += SCHLAEGERGESCHWINDIGKEIT

    if tasten[pygame.K_w]:
        linkerSchlaegerY -= SCHLAEGERGESCHWINDIGKEIT
    if tasten[pygame.K_s]:
        linkerSchlaegerY += SCHLAEGERGESCHWINDIGKEIT

    # Schlaegergrenzen
    if rechterSchlaegerY <= 0:
        rechterSchlaegerY = 0
    if rechterSchlaegerY >= FENSTERHOEHE - SCHLAEGERHOEHE:
        rechterSchlaegerY = FENSTERHOEHE - SCHLAEGERHOEHE

    if linkerSchlaegerY <= 0:
        linkerSchlaegerY = 0
    if linkerSchlaegerY >= FENSTERHOEHE - SCHLAEGERHOEHE:
        linkerSchlaegerY = FENSTERHOEHE - SCHLAEGERHOEHE

    # Schl�ger definieren
    linkerSchlaeger = pygame.Rect(
        SCHLAEGERABSTAND, linkerSchlaegerY, SCHLAEGERBREITE, SCHLAEGERHOEHE
    )
    rechterSchlaeger = pygame.Rect(
        RECHTERSCHLAEGERX, rechterSchlaegerY, SCHLAEGERBREITE, SCHLAEGERHOEHE
    )

    # Ballbewegungen
    ballX += ballbewegungX
    ballY += ballbewegungY

    # Kollision oben und unten
    if ballY < BALLGROESSE:
        ballbewegungY = BALLGESCHWINDIGKEIT

    if ballY > FENSTERHOEHE - BALLGROESSE:
        ballbewegungY *= -1

    # Kollision links und rechts
    if ballX <= BALLGROESSE:
        ballX = FENSTERMITTEX
        ballY = FENSTERMITTEY
        ballbewegungX = BALLGESCHWINDIGKEIT
        ballbewegungY = BALLGESCHWINDIGKEIT
        a = a + 1
        texta = schriftart.render(
            str(a), True, pygame.Color(VORDERGRUND), pygame.Color(HINTERGRUND)
        )

    if ballX >= FENSTERBREITE - BALLGROESSE:
        ballX = FENSTERMITTEX
        ballY = FENSTERMITTEY
        ballbewegungX *= -1
        ballbewegungY = BALLGESCHWINDIGKEIT
        b = b + 1
        textb = schriftart.render(
            str(b), True, pygame.Color(VORDERGRUND), pygame.Color(HINTERGRUND)
        )

    # Kollision Schlaeger
    ballRechteck = pygame.Rect(
        ballX - BALLGROESSE, ballY - BALLGROESSE, 2 * BALLGROESSE, 2 * BALLGROESSE
    )

    if linkerSchlaeger.colliderect(ballRechteck):
        ballX = linkerSchlaeger.right + BALLGROESSE
        ballbewegungX *= -1

    if rechterSchlaeger.colliderect(ballRechteck):
        ballX = rechterSchlaeger.left - BALLGROESSE
        ballbewegungX *= -1

    # Elemente zeichnen
    bildschirm.fill(HINTERGRUND)

    pygame.draw.rect(bildschirm, VORDERGRUND, rechterSchlaeger)
    pygame.draw.circle(bildschirm, VORDERGRUND, (ballX, ballY), BALLGROESSE)
    pygame.draw.rect(bildschirm, VORDERGRUND, linkerSchlaeger)

    bildschirm.blit(texta, (40, 20))
    bildschirm.blit(textb, (FENSTERBREITE - 120, 20))
    pygame.display.flip()
    clock.tick(30)
