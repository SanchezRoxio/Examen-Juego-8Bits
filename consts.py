import pygame
import sys

pygame.init()

SCREEN_RES = (1500,920)

NEGRO = (0,0,0)
BLANCO = (255,255,255)
RED = (255,0,0)
LIGTH_RED = (227, 66, 51)
GREEN = (0,255,0)
LIGTH_GREEN = (215,252,212)
CELESTE = (215,215,252)

pygame.mixer.init()

sonido_error = pygame.mixer.Sound("Assets\error.mp3")
sonido_ambiente = pygame.mixer.Sound("Assets\sonido_ambiente.mp3")
sonido_juego = pygame.mixer.Sound("Assets\sonido_juego.mp3")

#me traigo todas las imagenes :)

background = pygame.image.load("Assets\BackGround.png")
background = pygame.transform.scale(background, (1500,920))
background_rect = background.get_rect()

background_top_10 = pygame.image.load("Assets\BackGroundTop10.jpg")
background_top_10 = pygame.transform.scale(background_top_10, (1500,920))
background_saves_rect = background_top_10.get_rect()

fondo_pantalla_opciones = pygame.image.load("Assets\pantalla_opciones.png")
fondo_pantalla_opciones = pygame.transform.scale(fondo_pantalla_opciones, (1500,920))
fondo_pantalla_opciones_rect = fondo_pantalla_opciones.get_rect()

fondo_pantalla_preguntas =pygame.image.load("Assets\pantalla_preguntas.jpg")
fondo_pantalla_preguntas = pygame.transform.scale(fondo_pantalla_preguntas,(1500,920))
fondo_pantalla_preguntas_rect = fondo_pantalla_preguntas.get_rect()

fondo_pantalla_modficiar_vidas = pygame.image.load("Assets\pantalla_modificar_vidas.jpg")
fondo_pantalla_modificar_vidas = pygame.transform.scale(fondo_pantalla_modficiar_vidas,(1500,920))
fondo_pantalla_modificar_vidas_rect = fondo_pantalla_modficiar_vidas.get_rect()

fondo_pantalla_agregar_preguntas = pygame.image.load("Assets\pantalla_agregar_pregunta.jpg")
fondo_pantalla_agregar_preguntas = pygame.transform.scale(fondo_pantalla_agregar_preguntas,(1500,920))
fondo_pantalla_agregar_preguntas_rect = fondo_pantalla_agregar_preguntas.get_rect()

difuminado = pygame.image.load("Assets\save.jpg")
difuminado = pygame.transform.scale(difuminado, (1500,920))
difuminado_rect = difuminado.get_rect()