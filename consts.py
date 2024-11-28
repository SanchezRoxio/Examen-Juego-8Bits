import pygame
import sys

pygame.init()

SCREEN_RES = (1500,920) #Es la resolución de la pantalla.

#Establecemos los colores.

NEGRO = (0,0,0)
BLANCO = (255,255,255)
RED = (255,0,0)
LIGTH_RED = (227, 66, 51)
GREEN = (0,255,0)
LIGTH_GREEN = (215,252,212)
CELESTE = (215,215,252)

# Se establecen los sonidos.

pygame.mixer.init()

sonido_error = pygame.mixer.Sound("Assets\error.mp3")
sonido_ambiente = pygame.mixer.Sound("Assets\sonido_ambiente.mp3")
sonido_juego = pygame.mixer.Sound("Assets\sonido_juego.mp3")

#Establezco las imágenes de fondo.

background = pygame.image.load("Assets\BackGround.png")
background = pygame.transform.scale(background, SCREEN_RES)
background_rect = background.get_rect()

background_top_10 = pygame.image.load("Assets\BackGroundTop10.jpg")
background_top_10 = pygame.transform.scale(background_top_10, SCREEN_RES)
background_saves_rect = background_top_10.get_rect()

fondo_pantalla_opciones = pygame.image.load("Assets\pantalla_opciones.png")
fondo_pantalla_opciones = pygame.transform.scale(fondo_pantalla_opciones, SCREEN_RES)
fondo_pantalla_opciones_rect = fondo_pantalla_opciones.get_rect()

fondo_pantalla_preguntas =pygame.image.load("Assets\pantalla_preguntas.jpg")
fondo_pantalla_preguntas = pygame.transform.scale(fondo_pantalla_preguntas,SCREEN_RES)
fondo_pantalla_preguntas_rect = fondo_pantalla_preguntas.get_rect()

fondo_pantalla_modficiar_vidas = pygame.image.load("Assets\pantalla_modificar_vidas.jpg")
fondo_pantalla_modificar_vidas = pygame.transform.scale(fondo_pantalla_modficiar_vidas,SCREEN_RES)
fondo_pantalla_modificar_vidas_rect = fondo_pantalla_modficiar_vidas.get_rect()

fondo_pantalla_agregar_preguntas = pygame.image.load("Assets\pantalla_agregar_pregunta.jpg")
fondo_pantalla_agregar_preguntas = pygame.transform.scale(fondo_pantalla_agregar_preguntas,SCREEN_RES)
fondo_pantalla_agregar_preguntas_rect = fondo_pantalla_agregar_preguntas.get_rect()

difuminado = pygame.image.load("Assets\save.jpg")
difuminado = pygame.transform.scale(difuminado, SCREEN_RES)
difuminado_rect = difuminado.get_rect()