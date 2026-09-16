import pygame
import os

class Enemigo:
    def __init__(self, x, y, tipo, ruta_assets):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vivo = True
        self.indice_anim = 0.0
        self.velocidad_anim = 0.15
        self.vel_y = 0
        self.gravedad = 0.6
        
        if tipo == "slime":
            self.ancho, self.alto = 45, 35
            self.vel_x = 2
            self.vida_max = 1
            archivo_img = "slime_walk_anim_strip_15.png"
            self.total_cuadros = 15
        elif tipo == "hongo":
            self.ancho, self.alto = 40, 45
            self.vel_x = 3
            self.vida_max = 1
            archivo_img = "mushroom_walk_anim_strip_8.png"
            self.total_cuadros = 8
        elif tipo == "jefe1":
            self.ancho, self.alto = 90, 95
            self.vel_x = 2
            self.vida_max = 5
            archivo_img = "goblin_run_anim_strip_6.png"
            self.total_cuadros = 6
        elif tipo == "jefe2":
            self.ancho, self.alto = 110, 45
            self.vel_x = 4.5
            self.vida_max = 7
            archivo_img = "worm_spritesheet.png"
            self.total_cuadros = 3  
            self.velocidad_anim = 0.1 
        elif tipo == "jefe_final":
            self.ancho, self.alto = 120, 120
            self.vel_x = 5
            self.vida_max = 10
            archivo_img = "goblin_bomber_spritesheet.png"
            self.total_cuadros = 4

        self.vida = self.vida_max
        self.direccion = 1
        self.ultimo_ataque = pygame.time.get_ticks()
        self.cargar_graficos(ruta_assets, archivo_img)

    def buscar_archivo(self, nombre_archivo, ruta_raiz):
        for carpeta_actual, subcarpetas, archivos in os.walk(ruta_raiz):
            if nombre_archivo in archivos: return os.path.join(carpeta_actual, nombre_archivo)
        return None

    def cargar_graficos(self, ruta_assets, archivo_img):
        ruta_img = self.buscar_archivo(archivo_img, ruta_assets)
        if not ruta_img: raise FileNotFoundError(f"No se encontró {archivo_img}")
        strip = pygame.image.load(ruta_img).convert_alpha()
        self.anim_caminar = []
        ancho_cuadro = strip.get_width() // self.total_cuadros
        for i in range(self.total_cuadros):
            cuadro = strip.subsurface(pygame.Rect(i * ancho_cuadro, 0, ancho_cuadro, strip.get_height()))
            self.anim_caminar.append(pygame.transform.scale(cuadro, (self.ancho, self.alto)))

    def recibir_golpe(self):
        self.vida -= 1
        if self.vida <= 0: self.vivo = False

    def actualizar(self, alto_pantalla, lista_plataformas, heroe_x, lista_enemigos=None):
        if not self.vivo: return
        tiempo_actual = pygame.time.get_ticks()

        if self.tipo == "jefe1":
            self.direccion = 1 if heroe_x > self.x else -1
            if tiempo_actual - self.ultimo_ataque > 2500 and abs(self.x - heroe_x) < 200:
                if self.y >= alto_pantalla - 90 - self.alto:
                    self.vel_y = -12
                    self.ultimo_ataque = tiempo_actual
        elif self.tipo == "jefe2":
            self.direccion = 1 if heroe_x > (self.x + self.ancho // 2) else -1
        elif self.tipo == "jefe_final":
            self.direccion = 1 if heroe_x > self.x else -1
            if self.vida <= 5:
                self.vel_x = 6.5
                self.velocidad_anim = 0.25 

        self.x += self.vel_x * self.direccion
        self.vel_y += 0.6
        self.y += self.vel_y
        if self.y >= alto_pantalla - 90 - self.alto:
            self.y = alto_pantalla - 90 - self.alto
            self.vel_y = 0

        rect_enemigo = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        if lista_enemigos:
            for otro in lista_enemigos:
                if otro != self and otro.vivo:
                    rect_otro = pygame.Rect(otro.x, otro.y, otro.ancho, otro.alto)
                    if rect_enemigo.colliderect(rect_otro):
                        self.direccion *= -1
                        otro.direccion *= -1
                        self.x += self.vel_x * self.direccion
                        rect_enemigo.x = self.x 
                        break

        sobre_plataforma = False
        plat_actual = None
        for plat in lista_plataformas:
            if rect_enemigo.colliderect(plat.rect):
                if self.vel_y >= 0 and (self.y + self.alto - self.vel_y) <= plat.rect.top + 6:
                    self.y = plat.rect.top - self.alto
                    self.vel_y = 0
                    sobre_plataforma = True
                    plat_actual = plat.rect

        if sobre_plataforma and self.tipo in ["slime", "hongo"]:
            futuro_pie_x = self.x + (self.vel_x * self.direccion) + (self.ancho if self.direccion == 1 else 0)
            if futuro_pie_x > plat_actual.right or futuro_pie_x < plat_actual.left: self.direccion *= -1

        self.indice_anim += self.velocidad_anim
        if self.indice_anim >= len(self.anim_caminar): self.indice_anim = 0.0

    def dibujar(self, superficie):
        if not self.vivo: return
        imagen_actual = self.anim_caminar[int(self.indice_anim)]
        if self.direccion == -1: imagen_actual = pygame.transform.flip(imagen_actual, True, False)
        superficie.blit(imagen_actual, (self.x, self.y))

        if self.tipo in ["jefe1", "jefe2", "jefe_final"]:
            ancho_barra = self.ancho + 10
            pygame.draw.rect(superficie, (80, 20, 20), (self.x - 5, self.y - 15, ancho_barra, 6))
            color_barra = (240, 200, 20) if (self.tipo == "jefe_final" and self.vida <= 5) else (50, 220, 90)
            pygame.draw.rect(superficie, color_barra, (self.x - 5, self.y - 15, int(ancho_barra * (self.vida / self.vida_max)), 6))
