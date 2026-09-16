import pygame
import os

class Jugador:
    def __init__(self, x, y, ruta_assets):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.vel_x = 5
        self.vel_y = 0
        self.gravedad = 0.65       
        self.fuerza_salto = -14.5  
        self.en_el_suelo = False
        self.mirando_derecha = True
        
        self.vida_max = 3
        self.vida = 3
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.duracion_invulnerable = 1500 
        
        self.puede_dash = True
        self.en_dash = False
        self.tiempo_dash = 0
        self.duracion_dash = 200 
        self.vel_dash = 15
        self.direccion_dash = 1
        
        self.estado = "quieto"
        self.indice_anim = 0.0
        self.velocidad_anim = 0.15
        
        self.cargar_graficos(ruta_assets)
        self.imagen_actual = self.anim_idle

    def buscar_archivo(self, nombre_archivo, ruta_raiz):
        for carpeta_actual, subcarpetas, archivos in os.walk(ruta_raiz):
            if nombre_archivo in archivos:
                return os.path.join(carpeta_actual, nombre_archivo)
        return None

    def recortar_animacion_individual(self, imagen_strip, cantidad_cuadros, multiplicador=3.2):
        cuadros = []
        ancho_cuadro = imagen_strip.get_width() // cantidad_cuadros
        alto_cuadro = imagen_strip.get_height()
        for i in range(cantidad_cuadros):
            cuadro = imagen_strip.subsurface(pygame.Rect(i * ancho_cuadro, 0, ancho_cuadro, alto_cuadro))
            cuadros.append(pygame.transform.scale(cuadro, (int(ancho_cuadro * multiplicador), int(alto_cuadro * multiplicador))))
        return cuadros, int(ancho_cuadro * multiplicador), int(alto_cuadro * multiplicador)

    def cargar_graficos(self, ruta_assets):
        strip_idle = pygame.image.load(self.buscar_archivo("herochar_idle_anim_strip_4.png", ruta_assets)).convert_alpha()
        self.anim_idle, self.ancho, self.alto = self.recortar_animacion_individual(strip_idle, 4)
        strip_run = pygame.image.load(self.buscar_archivo("herochar_run_anim_strip_6.png", ruta_assets)).convert_alpha()
        self.anim_run, _, _ = self.recortar_animacion_individual(strip_run, 6)
        strip_attack = pygame.image.load(self.buscar_archivo("herochar_sword_attack_anim_strip_4.png", ruta_assets)).convert_alpha()
        self.anim_attack, _, _ = self.recortar_animacion_individual(strip_attack, 4)
        strip_efecto = pygame.image.load(self.buscar_archivo("sword_effect_strip_4(new).png", ruta_assets)).convert_alpha()
        self.anim_efecto_espada, _, _ = self.recortar_animacion_individual(strip_efecto, 4, multiplicador=4.0)

    def atacar(self, lista_enemigos):
        golpe_exitoso = False
        enemigo_golpeado_pos = (0,0)
        if self.estado != "atacando" and not self.en_dash:
            self.estado = "atacando"
            self.indice_anim = 0.0
            rango_ataque = 95 
            alto_hitbox = self.alto + 30 
            if self.mirando_derecha:
                hitbox_ataque = pygame.Rect(self.x + self.ancho - 10, self.y - 15, rango_ataque, alto_hitbox)
            else:
                hitbox_ataque = pygame.Rect(self.x - rango_ataque + 10, self.y - 15, rango_ataque, alto_hitbox)
                
            for enemigo in lista_enemigos:
                if enemigo.vivo:
                    rect_enemigo = pygame.Rect(enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto)
                    if hitbox_ataque.colliderect(rect_enemigo):
                        enemigo.recibir_golpe()
                        golpe_exitoso = True
                        enemigo_golpeado_pos = (enemigo.x + enemigo.ancho//2, enemigo.y + enemigo.alto//2)
        return golpe_exitoso, enemigo_golpeado_pos

    def recibir_danio(self):
        if not self.invulnerable and not self.en_dash:
            self.vida -= 1
            if self.vida < 0: self.vida = 0
            self.invulnerable = True
            self.tiempo_invulnerable = pygame.time.get_ticks()
            self.vel_y = -7
            if self.mirando_derecha: self.x -= 50
            else: self.x += 50

    def iniciar_dash(self):
        if self.puede_dash and not self.en_dash and self.estado != "atacando":
            self.en_dash = True
            self.puede_dash = False
            self.tiempo_dash = pygame.time.get_ticks()
            self.direccion_dash = 1 if self.mirando_derecha else -1
            self.vel_y = 0 

    def actualizar(self, teclas, alto_pantalla, lista_plataformas):
        tiempo_actual = pygame.time.get_ticks()
        if self.invulnerable:
            if tiempo_actual - self.tiempo_invulnerable > self.duracion_invulnerable: self.invulnerable = False

        if self.en_dash:
            if tiempo_actual - self.tiempo_dash > self.duracion_dash:
                self.en_dash = False
                self.vel_y = 0
            else:
                self.x += self.vel_dash * self.direccion_dash
                if self.x < 0: self.x = 0
                if self.x > 800 - self.ancho: self.x = 800 - self.ancho
        else:
            self.indice_anim += self.velocidad_anim
            if self.en_el_suelo: self.puede_dash = True
            if self.estado == "atacando":
                if int(self.indice_anim) >= len(self.anim_attack):
                    self.estado = "quieto"
                    self.indice_anim = 0.0
                    self.imagen_actual = self.anim_idle
                else: self.imagen_actual = self.anim_attack[int(self.indice_anim)]
            if self.estado != "atacando":
                moviendose = False
                if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                    self.x -= self.vel_x
                    self.mirando_derecha = False
                    moviendose = True
                if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                    self.x += self.vel_x
                    self.mirando_derecha = True
                    moviendose = True
                if moviendose:
                    self.estado = "corriendo"
                    if self.indice_anim >= len(self.anim_run): self.indice_anim = 0.0
                    self.imagen_actual = self.anim_run[int(self.indice_anim)]
                else:
                    self.estado = "quieto"
                    if self.indice_anim >= len(self.anim_idle): self.indice_anim = 0.0
                    self.imagen_actual = self.anim_idle[int(self.indice_anim)]
            self.vel_y += self.gravedad
            self.y += self.vel_y
            
        self.en_el_suelo = False
        if self.y >= alto_pantalla - 90 - self.alto:
            self.y = alto_pantalla - 90 - self.alto
            self.vel_y = 0
            self.en_el_suelo = True
            
        rect_jugador = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        for plat in lista_plataformas:
            if rect_jugador.colliderect(plat.rect):
                if self.vel_y > 0 and (self.y + self.alto - self.vel_y) <= plat.rect.top + 6:
                    self.y = plat.rect.top - self.alto
                    self.vel_y = 0
                    self.en_el_suelo = True
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w]) and self.en_el_suelo and self.estado != "atacando" and not self.en_dash:
            self.vel_y = self.fuerza_salto

    def dibujar(self, superficie):
        if self.invulnerable and (pygame.time.get_ticks() // 80) % 2 == 0: return
        if self.mirando_derecha:
            superficie.blit(self.imagen_actual, (self.x, self.y))
            if self.estado == "atacando": superficie.blit(self.anim_efecto_espada[int(self.indice_anim)], (self.x + 30, self.y - 10))
        else:
            imagen_volteada = pygame.transform.flip(self.imagen_actual, True, False)
            superficie.blit(imagen_volteada, (self.x, self.y))
            if self.estado == "atacando":
                img_efecto = pygame.transform.flip(self.anim_efecto_espada[int(self.indice_anim)], True, False)
                superficie.blit(img_efecto, (self.x - 45, self.y - 10))
