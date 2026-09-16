import pygame
from plataforma import Plataforma
from enemigo import Enemigo
from objeto import Objeto

class Nivel:
    def __init__(self, numero, textura_suelo, ruta_assets):
        self.numero = numero
        self.plataformas = []
        self.enemigos = []
        self.objetos = []
        
        if numero == 1:
            self.plataformas = [Plataforma(220, 360, 200, 35, textura_suelo), Plataforma(500, 240, 200, 35, textura_suelo)]
            self.enemigos = [Enemigo(250, 300, "slime", ruta_assets), Enemigo(550, 180, "hongo", ruta_assets), Enemigo(350, 465, "slime", ruta_assets)]
            self.objetos = [Objeto(320, 310, "moneda", ruta_assets), Objeto(590, 190, "moneda", ruta_assets), Objeto(450, 480, "picos", ruta_assets)]
            
        elif numero == 2:
            self.plataformas = [Plataforma(100, 400, 140, 35, textura_suelo), Plataforma(300, 290, 140, 35, textura_suelo), Plataforma(500, 180, 140, 35, textura_suelo)]
            self.enemigos = [Enemigo(120, 340, "hongo", ruta_assets), Enemigo(320, 230, "slime", ruta_assets), Enemigo(520, 120, "hongo", ruta_assets), Enemigo(220, 465, "slime", ruta_assets)]
            self.objetos = [Objeto(150, 350, "moneda", ruta_assets), Objeto(260, 340, "moneda", ruta_assets), Objeto(450, 230, "moneda", ruta_assets), Objeto(350, 240, "moneda", ruta_assets), Objeto(440, 480, "picos", ruta_assets), Objeto(480, 480, "picos", ruta_assets)]
            
        elif numero == 3: # Sala con plataformas, enemigos comunes y el Jefe 1 al final
            self.plataformas = [
                Plataforma(100, 320, 160, 35, textura_suelo), 
                Plataforma(320, 220, 160, 35, textura_suelo),
                Plataforma(540, 320, 160, 35, textura_suelo)
            ]
            self.enemigos = [
                Enemigo(120, 260, "slime", ruta_assets), 
                Enemigo(350, 160, "hongo", ruta_assets),
                Enemigo(650, 390, "jefe1", ruta_assets) # El jefe te espera al fondo
            ]
            self.objetos = [
                Objeto(150, 270, "moneda", ruta_assets),
                Objeto(370, 170, "moneda", ruta_assets),
                Objeto(350, 480, "picos", ruta_assets),
                Objeto(390, 480, "picos", ruta_assets)
            ]
            
        elif numero == 4: # Sala con obstáculos y el Jefe 2 (Gusano) custodiando el suelo
            self.plataformas = [
                Plataforma(150, 380, 140, 35, textura_suelo),
                Plataforma(350, 280, 140, 35, textura_suelo),
                Plataforma(550, 380, 140, 35, textura_suelo)
            ]
            self.enemigos = [
                Enemigo(170, 320, "hongo", ruta_assets),
                Enemigo(570, 320, "slime", ruta_assets),
                Enemigo(600, 440, "jefe2", ruta_assets) # El jefe gusano al final del suelo
            ]
            self.objetos = [
                Objeto(380, 230, "moneda", ruta_assets),
                Objeto(400, 230, "moneda", ruta_assets),
                Objeto(320, 480, "picos", ruta_assets),
                Objeto(480, 480, "picos", ruta_assets)
            ]

        elif numero == 5: # La fortaleza antes del Jefe Final
            self.plataformas = [
                Plataforma(100, 400, 120, 35, textura_suelo),
                Plataforma(260, 300, 120, 35, textura_suelo),
                Plataforma(420, 200, 120, 35, textura_suelo),
                Plataforma(580, 320, 140, 35, textura_suelo)
            ]
            self.enemigos = [
                Enemigo(120, 340, "slime", ruta_assets),
                Enemigo(280, 240, "hongo", ruta_assets),
                Enemigo(440, 140, "slime", ruta_assets),
                Enemigo(650, 390, "jefe_final", ruta_assets) # El bombardero gigante protegiendo la salida
            ]
            self.objetos = [
                Objeto(140, 350, "moneda", ruta_assets),
                Objeto(440, 150, "moneda", ruta_assets),
                Objeto(220, 480, "picos", ruta_assets),
                Objeto(540, 480, "picos", ruta_assets)
            ]
