import pygame
import sys
import os
import random
import asyncio  # 🚀 IMPORTANTE: Librería para que funcione en la web
from jugador import Jugador
from nivel import Nivel
from particula import Particula

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Metroidvania Python - Campaña Completa 5 Niveles")
reloj = pygame.time.Clock()

ruta_assets = os.path.join(os.path.dirname(__file__), "assets")

def buscar_archivo(nombre_archivo, ruta_raiz):
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_raiz):
        if nombre_archivo in archivos:
            return os.path.join(carpeta_actual, nombre_archivo)
    return None

try:
    imagen_fondo = pygame.image.load(buscar_archivo("background.png", ruta_assets)).convert()
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

    spritesheet_bloques = pygame.image.load(buscar_archivo("tileset_32x32(new).png", ruta_assets)).convert_alpha()
    textura_suelo = spritesheet_bloques.subsurface(pygame.Rect(0, 0, 32, 32))
    
    img_corazon = pygame.image.load(buscar_archivo("hearts_hud.png", ruta_assets)).convert_alpha()
    img_corazon = pygame.transform.scale(img_corazon, (30, 30))

except Exception as e:
    print(f"❌ Error cargando recursos: {e}")
    pygame.quit()
    sys.exit()

# Declaramos las variables globales que usará la función asíncrona
heroe = None
puntuacion_monedas = 0
nivel_actual = 1
mapa = None
lista_particulas = []

def reiniciar_juego():
    global heroe, puntuacion_monedas, nivel_actual, mapa, lista_particulas
    heroe = Jugador(50, 400, ruta_assets)
    puntuacion_monedas = 0
    nivel_actual = 1
    mapa = Nivel(nivel_actual, textura_suelo, ruta_assets)
    lista_particulas = []

fuente_hud = pygame.font.SysFont("Arial", 24, bold=True)
fuente_pantalla = pygame.font.SysFont("Arial", 55, bold=True)
fuente_subtitulo = pygame.font.SysFont("Arial", 22, bold=False)

estado_juego = "menu"
reiniciar_juego()

# 🚀 DEFINIMOS LA FUNCIÓN ASÍNCRONA PRINCIPAL
async def main():
    global estado_juego, heroe, puntuacion_monedas, nivel_actual, mapa, lista_particulas
    
    while True:
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if estado_juego == "menu":
                    if evento.key == pygame.K_SPACE:
                        estado_juego = "jugando"
                        reiniciar_juego()
                elif estado_juego == "jugando":
                    if heroe.vida > 0:
                        if evento.key == pygame.K_k:
                            exito, pos_enemigo = heroe.atacar(mapa.enemigos)
                            if exito:
                                enemigo_x, enemigo_y = pos_enemigo
                                for _ in range(15):
                                    color_chispa = random.choice([(255, 140, 0), (255, 215, 0), (255, 69, 0)])
                                    lista_particulas.append(Particula(enemigo_x, enemigo_y, color_chispa))
                        if evento.key == pygame.K_l:
                            heroe.iniciar_dash()
                    else:
                        if evento.key == pygame.K_r:
                            reiniciar_juego()

        teclas = pygame.key.get_pressed()

        if estado_juego == "jugando":
            if heroe.vida > 0:
                if heroe.x >= ANCHO - 40:
                    jefes_vivos = len([e for e in mapa.enemigos if e.vivo and e.tipo in ["jefe1", "jefe2", "jefe_final"]])
                    if nivel_actual < 5 and jefes_vivos == 0:
                        nivel_actual += 1
                        mapa = Nivel(nivel_actual, textura_suelo, ruta_assets)
                        heroe.x = 40 
                    elif nivel_actual == 5 and jefes_vivos == 0:
                        nivel_actual = 6 

                heroe.actualizar(teclas, ALTO, mapa.plataformas)
                
                if heroe.en_dash:
                    for _ in range(2):
                        lista_particulas.append(Particula(heroe.x + heroe.ancho//2, heroe.y + heroe.alto//2 + random.randint(-10,10), (0, 238, 255)))
                
                for obj in mapa.objetos:
                    if obj.activo:
                        obj.actualizar()
                        rect_heroe = pygame.Rect(heroe.x, heroe.y, heroe.ancho, heroe.alto)
                        rect_obj = pygame.Rect(obj.x, obj.y, obj.ancho, obj.alto)
                        if rect_heroe.colliderect(rect_obj):
                            if obj.tipo == "moneda":
                                obj.activo = False
                                puntuacion_monedas += 1 
                            elif obj.tipo == "picos":
                                heroe.recibir_danio() 
                                
                for enemigo in mapa.enemigos:
                    if enemigo.vivo:
                        enemigo.actualizar(ALTO, mapa.plataformas, heroe.x, mapa.enemigos) 
                        rect_heroe = pygame.Rect(heroe.x, heroe.y, heroe.ancho, heroe.alto)
                        rect_enemigo = pygame.Rect(enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto)
                        if rect_heroe.colliderect(rect_enemigo):
                            heroe.recibir_danio()

            for p in lista_particulas[:]:
                p.actualizar()
                if p.radio <= 0:
                    lista_particulas.remove(p)

        pantalla.blit(imagen_fondo, (0, 0))
        
        if estado_juego == "menu":
            filtro_oscuro = pygame.Surface((ANCHO, ALTO))
            filtro_oscuro.fill((15, 10, 25))
            filtro_oscuro.set_alpha(180)
            pantalla.blit(filtro_oscuro, (0, 0))
            
            color_parp = (255, 255, 255) if (tiempo_actual // 500) % 2 == 0 else (160, 160, 180)
            titulo = fuente_pantalla.render("KNIGHT ADVENTURE", True, (0, 238, 255))
            sub_titulo = fuente_subtitulo.render("PRESIONA ESPACIO PARA EMPEZAR", True, color_parp)
            controles = fuente_subtitulo.render("Controles: A/D o Flechas (Mover) | W o Espacio (Saltar) | K (Atacar) | L (Dash)", True, (200, 200, 200))
            
            pantalla.blit(titulo, (ANCHO // 2 - 240, ALTO // 2 - 70))
            pantalla.blit(sub_titulo, (ANCHO // 2 - 170, ALTO // 2 + 20))
            pantalla.blit(controles, (ANCHO // 2 - 340, ALTO - 60))

        elif estado_juego == "jugando":
            for x in range(0, ANCHO, 40):
                pantalla.blit(pygame.transform.scale(textura_suelo, (40,40)), (x, ALTO - 90))
                pantalla.blit(pygame.transform.scale(textura_suelo, (40,40)), (x, ALTO - 50))
                
            for plat in mapa.plataformas:
                plat.dibujar(pantalla)
            for obj in mapa.objetos:
                obj.dibujar(pantalla)
            for enemigo in mapa.enemigos:
                enemigo.dibujar(pantalla)
            if heroe.vida > 0 and nivel_actual <= 5:
                heroe.dibujar(pantalla)
            for p in lista_particulas:
                p.dibujar(pantalla)
            
            if heroe.vida > 0 and nivel_actual <= 5:
                for i in range(heroe.vida):
                    pantalla.blit(img_corazon, (20 + (i * 35), 20))
                
            texto_monedas = fuente_hud.render(f"Monedas: {puntuacion_monedas}", True, (255, 215, 0))
            texto_nivel = fuente_hud.render(f"Nivel: {nivel_actual if nivel_actual <= 5 else 5}", True, (255, 255, 255))
            pantalla.blit(texto_monedas, (20, 60))
            pantalla.blit(texto_nivel, (ANCHO - 120, 20))

            if heroe.vida <= 0:
                texto_gameover = fuente_pantalla.render("GAME OVER", True, (255, 0, 0))
                texto_instruccion = fuente_subtitulo.render("Presiona 'R' para volver a intentarlo", True, (255, 255, 255))
                pantalla.blit(texto_gameover, (ANCHO // 2 - 130, ALTO // 2 - 40))
                pantalla.blit(texto_instruccion, (ANCHO // 2 - 145, ALTO // 2 + 20))
            elif nivel_actual == 6:
                texto_victoria = fuente_pantalla.render("¡CAMPEÓN DEFINITIVO!", True, (0, 255, 0))
                pantalla.blit(texto_victoria, (ANCHO // 2 - 250, ALTO // 2 - 25))

        pygame.display.flip()
        reloj.tick(60)
        
        # 🚀 SÚPER IMPORTANTE: Permite que el navegador respire y procese la pestaña web
        await asyncio.sleep(0)

# Lanzamos el bucle del juego asíncrono
asyncio.run(main())
