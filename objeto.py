import pygame
import os

class Objeto:
    def __init__(self, x, y, tipo, ruta_assets):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.activo = True
        self.indice_anim = 0.0
        
        if tipo == "moneda":
            self.ancho, self.alto = 25, 25
            self.cargar_moneda(ruta_assets)
        elif tipo == "picos":
            self.ancho, self.alto = 40, 30
            self.cargar_picos(ruta_assets)

    def buscar_archivo(self, nombre_archivo, ruta_raiz):
        for carpeta_actual, subcarpetas, archivos in os.walk(ruta_raiz):
            if nombre_archivo in archivos: return os.path.join(carpeta_actual, nombre_archivo)
        return None

    def cargar_moneda(self, ruta_assets):
        ruta_img = self.buscar_archivo("coin_anim_strip_6.png", ruta_assets)
        strip = pygame.image.load(ruta_img).convert_alpha()
        self.anim = []
        ancho_cuadro = strip.get_width() // 6
        for i in range(6):
            cuadro = strip.subsurface(pygame.Rect(i * ancho_cuadro, 0, ancho_cuadro, strip.get_height()))
            self.anim.append(pygame.transform.scale(cuadro, (self.ancho, self.alto)))

    def cargar_picos(self, ruta_assets):
        ruta_img = self.buscar_archivo("spikes.png", ruta_assets)
        img = pygame.image.load(ruta_img).convert_alpha()
        img_escalada = pygame.transform.scale(img, (self.ancho, self.alto))
        self.imagen = pygame.transform.flip(img_escalada, False, True)

    def actualizar(self):
        if self.tipo == "moneda":
            self.indice_anim += 0.15
            if self.indice_anim >= len(self.anim): self.indice_anim = 0.0

    def dibujar(self, superficie):
        if not self.activo: return
        if self.tipo == "moneda": superficie.blit(self.anim[int(self.indice_anim)], (self.x, self.y))
        elif self.tipo == "picos": superficie.blit(self.imagen, (self.x, self.y))
