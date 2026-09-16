import pygame

class Plataforma:
    def __init__(self, x, y, ancho, alto, textura):
        self.rect = pygame.Rect(x, y, ancho, alto)
        # Escalamos la textura de piedra para que rellene la plataforma
        self.textura = pygame.transform.scale(textura, (ancho, alto))

    def dibujar(self, superficie):
        superficie.blit(self.textura, (self.rect.x, self.rect.y))
