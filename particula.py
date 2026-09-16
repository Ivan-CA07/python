import pygame
import random

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        # Dirección aleatoria para que salgan disparadas en todas direcciones
        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-5, 2)
        # Tamaño inicial aleatorio
        self.radio = random.randint(4, 7)
        self.color = color
        self.vida = 255 # Opacidad inicial (va bajando)

    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        # Gravedad ligera para que las chispas caigan
        self.vel_y += 0.1 
        # Reducir el tamaño poco a poco
        self.radio -= 0.15
        if self.radio < 0: self.radio = 0

    def dibujar(self, superficie):
        if self.radio > 0:
            # Dibujamos un círculo brillante con el color elegido
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), int(self.radio))
