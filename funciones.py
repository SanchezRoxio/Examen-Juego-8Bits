import pygame, sys, csv, random, json, datetime, time

from clases import *
from consts import *

def jugar(screen:tuple[int,int], preguntas:str, vidas:int, puntaje_usuario:int) -> None:
    '''
    Establece la configuración principal del juego.

    Ingresa como parámetros las condiciones del juego.

    No retorna un valor. Maneja el flujo del juego y llama a otras funciones
    para tareas específicas (como manejar el menú principal o registrar puntajes).
    '''
    tiempo_inicial = time.time()
    respuestas_correctas = 0  #Contador de respuestas correctas
    respuestas_correctas_consecutivas = 0  #Contador de respuestas correctas consecutivas
    cant_puntaje = puntaje_usuario
    duracion_temporizador = 10
    tiempo_final = tiempo_inicial + duracion_temporizador
    comodin_pasar_disponible = True  #Variable para el comodin "Pasar"
    comodin_x2_disponible = True  # Variable para el comodin "X2"
    multiplicador_x2 = 1  #Multiplicador para el comodin X2

    while vidas >= 1 and len(preguntas) > 0:
        tiempo_restante = int(tiempo_final - time.time())

        if tiempo_restante <= 0: #Si se acaba el tiempo se resta una vida.
            vidas -= 1
            tiempo_inicial = time.time() #Se reinicia el tiempo inicial.
            tiempo_final = tiempo_inicial + duracion_temporizador
            pregunta = seleccionar_pregunta(preguntas)
            eliminar_pregunta(preguntas, pregunta[0])

        mouse_posicion_jugar = pygame.mouse.get_pos() #Me devuelve la posición o coordenadas del mouse en la pantalla.
        screen.blit(fondo_pantalla_preguntas, (0, 0)) #Se establece el fondo de pantalla.
        txt_vidas = obtener_letra(35).render(f"♥{vidas}", True, RED) #Renderiza un texto y lo transforma en una imagen.
        screen.blit(txt_vidas, (50, 700))

        pregunta = seleccionar_pregunta(preguntas)
        txt_pregunta = obtener_letra(40).render(pregunta[0], True, NEGRO)
        txt_width = txt_pregunta.get_size()
        txt_x = (SCREEN_RES[0] - txt_width[0]) // 2 #Centra la pregunta en la mitad de la pantalla. Toma los anchos de la pantalla y de la pregunta.
        if txt_width[0] > SCREEN_RES[0]:
            txt_x = 0
        screen.blit(txt_pregunta, (txt_x, 150)) #Posicionando la pregunta.

        letra_respuesta = None  #evitar errores
        # Botones de opciones
        btn_opcion_a = Boton(imagen=None, pos=(720, 300), text_input=pregunta[1], fuente=obtener_letra(35), color_base=NEGRO, color_hover=RED)
        btn_opcion_b = Boton(imagen=None, pos=(720, 400), text_input=pregunta[2], fuente=obtener_letra(35), color_base=NEGRO, color_hover=RED)
        btn_opcion_c = Boton(imagen=None, pos=(720, 500), text_input=pregunta[3], fuente=obtener_letra(35), color_base=NEGRO, color_hover=RED)
        btn_opcion_d = Boton(imagen=None, pos=(720, 600), text_input=pregunta[4], fuente=obtener_letra(35), color_base=NEGRO, color_hover=RED)
        btn_jugar_back = Boton(imagen=None, pos=(1400, 800), text_input="BACK", fuente=obtener_letra(30), color_base=NEGRO, color_hover=RED)

        # Botón "Pasar"
        if comodin_pasar_disponible:
            btn_pasar = Boton(imagen=None, pos=(1200, 800), text_input="PASAR", fuente=obtener_letra(30), color_base=NEGRO, color_hover=RED)
            btn_pasar.cambiar_color(mouse_posicion_jugar)
            btn_pasar.actualizar(screen)

        # Botón "X2"
        if comodin_x2_disponible:
            btn_x2 = Boton(imagen=None, pos=(1000, 800), text_input="X2", fuente=obtener_letra(30), color_base=NEGRO, color_hover=RED)
            btn_x2.cambiar_color(mouse_posicion_jugar)
            btn_x2.actualizar(screen)

        #Actualizar los botones.
        btn_opcion_a.cambiar_color(mouse_posicion_jugar)
        btn_opcion_a.actualizar(screen)
        btn_opcion_b.cambiar_color(mouse_posicion_jugar)
        btn_opcion_b.actualizar(screen)
        btn_opcion_c.cambiar_color(mouse_posicion_jugar)
        btn_opcion_c.actualizar(screen)
        btn_opcion_d.cambiar_color(mouse_posicion_jugar)
        btn_opcion_d.actualizar(screen)
        btn_jugar_back.cambiar_color(mouse_posicion_jugar)
        btn_jugar_back.actualizar(screen)

        #Verificar los clics
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: #Verifica qué respuesta se seleccionó, en dónde se clickeó.
                if btn_opcion_a.checkear_input(mouse_posicion_jugar):
                    letra_respuesta = "a"
                elif btn_opcion_b.checkear_input(mouse_posicion_jugar):
                    letra_respuesta = "b"
                elif btn_opcion_c.checkear_input(mouse_posicion_jugar):
                    letra_respuesta = "c"
                elif btn_opcion_d.checkear_input(mouse_posicion_jugar):
                    letra_respuesta = "d"
                elif comodin_pasar_disponible and btn_pasar.checkear_input(mouse_posicion_jugar):
                    #Boton PASAR
                    eliminar_pregunta(preguntas, pregunta[0])
                    tiempo_inicial = time.time()
                    tiempo_final = tiempo_inicial + duracion_temporizador
                    comodin_pasar_disponible = False  #Desactiva el comodín una vez usado.
                    break
                elif comodin_x2_disponible and btn_x2.checkear_input(mouse_posicion_jugar):
                    multiplicador_x2 = 2  #Duplicar los puntos
                    comodin_x2_disponible = False  #Desactiva el comodin
                    break
                elif btn_jugar_back.checkear_input(mouse_posicion_jugar):
                    # Botón BACK
                    print("Boton BACK presionado, regresando al menú principal.")
                    sonido_juego.stop()
                    sonido_ambiente.play()
                    main_menu(screen)
                    return
                else:# Si no se hizo clic en ningun lado, no hacer nada
                    continue
                #Procesar la respuesta
                if letra_respuesta:
                    if letra_respuesta == pregunta[5]:
                        puntos_obtenidos = 10 * multiplicador_x2  #Duplica los puntos si X2 esta encendido
                        cant_puntaje += puntos_obtenidos #Acumulador de los puntos.
                        respuestas_correctas += 1
                        respuestas_correctas_consecutivas += 1

                        if respuestas_correctas_consecutivas >= 5:
                            vidas += 1
                            respuestas_correctas_consecutivas = 0
                            respuestas_correctas = 0
                        tiempo_inicial = time.time()
                        tiempo_final = tiempo_inicial + duracion_temporizador

                        modificar_dato_pregunta(pregunta[0], 'cantidad_veces_preguntada')
                        modificar_dato_pregunta(pregunta[0], 'cantidad_aciertos')
                        calcular_y_modificar_porcentaje_aciertos(pregunta[0])
                    else:
                        vidas -= 1
                        cant_puntaje -= 10  # Restar 10 puntos al puntaje
                        if cant_puntaje < 0:  # Asegurarse de que no sea menor que 0
                            cant_puntaje = 0
                        sonido_error.play()
                        sonido_error.set_volume(0.5)
                        tiempo_inicial = time.time()
                        tiempo_final = tiempo_inicial + duracion_temporizador
                        respuestas_correctas_consecutivas = 0
                        modificar_dato_pregunta(pregunta[0], 'cantidad_veces_preguntada')
                        modificar_dato_pregunta(pregunta[0], 'cantidad_fallos')
                        calcular_y_modificar_porcentaje_aciertos(pregunta[0])

                    eliminar_pregunta(preguntas, pregunta[0])
                    if len(preguntas) == 0:
                        sonido_juego.stop()
                        pedir_nombre_jugador(screen, cant_puntaje)
                        return

        #Formato del temporizador
        tiempo_restante = int(tiempo_final - time.time())
        if tiempo_restante > 3:
            txt_temporizador = obtener_letra(30).render(f'Tiempo restante: {tiempo_restante}', True, NEGRO)
        else:
            txt_temporizador = obtener_letra(30).render(f'Tiempo restante: {tiempo_restante}', True, RED)
        rect_temporizador = txt_temporizador.get_rect(center=(300, 800))
        screen.blit(txt_temporizador, rect_temporizador)

        time.sleep(0.01)
        pygame.display.update() #Sirve para mostrar los cambios en la pantalla del juego.

    pedir_nombre_jugador(screen, cant_puntaje)

def seleccionar_pregunta(preguntas:list)->list: 
    '''
    Selecciona una de las preguntas del csv.\n
    Ingresa como parámetro ese archivo.\n
    Retorna la pregunta con sus respectivas respuestas.
    '''
    
    pregunta = preguntas[0]["pregunta"] 
    respuesta_a = preguntas[0]["respuesta_a"]  
    respuesta_b = preguntas[0]["respuesta_b"] 
    respuesta_c = preguntas[0]["respuesta_c"]
    respuesta_d = preguntas[0]["respuesta_d"]
    respuesta_correcta = preguntas[0]["respuesta_correcta"]
    return (pregunta, respuesta_a, respuesta_b, respuesta_c,respuesta_d, respuesta_correcta)

def opciones(screen:tuple[int,int])->None:
    '''
    Contiene la configuración de la pantalla de opciones del juego.\n
    Recibe como parámetro la dimensión de la pantalla.    
    '''
    
    while True:
        
        mouse_posicion_opciones = pygame.mouse.get_pos()
        
        screen.blit(fondo_pantalla_opciones,(0,0))
        
        txt_opciones = obtener_letra(45).render("OPTIONS", True, BLANCO)
        
        rect_opciones = txt_opciones.get_rect(center = (750, 120))
        
        screen.blit(txt_opciones, rect_opciones)

        btn_opciones_back = Boton(imagen = None, pos = (1380, 800), text_input = "BACK", fuente = obtener_letra(35), color_base = BLANCO, color_hover = RED)
        
        btn_opciones_activar_desactivar_sonido = Boton(imagen = None, pos = (380, 400), text_input= "TURN OFF/ON VOLUME", fuente = obtener_letra(35),color_base = BLANCO, color_hover = NEGRO)

        btn_opciones_subir_volumen = Boton(imagen = None, pos = (330,500), text_input = "INCREASE VOLUME", fuente = obtener_letra(35), color_base = BLANCO,color_hover = NEGRO)

        btn_opciones_bajar_volumen = Boton(imagen = None, pos = (330,600), text_input = "DECREASE VOLUME", fuente = obtener_letra(35),color_base = BLANCO, color_hover = NEGRO)
        
        lista_botones = [btn_opciones_activar_desactivar_sonido,btn_opciones_subir_volumen,btn_opciones_bajar_volumen,btn_opciones_back]
        
        for boton in lista_botones:
            
            boton.cambiar_color(mouse_posicion_opciones)
            
            boton.actualizar(screen)
            
        
        for event in pygame.event.get():

            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(btn_opciones_activar_desactivar_sonido.checkear_input(mouse_posicion_opciones)):
                    if(evaluar_sonido_json("partidas.json") == "0"):
                        sonido_ambiente.play()
                        print("TURN OFF/ON VOLUME")
                        volumen_actual = leer_json("partidas.json")
                        sonido_ambiente.set_volume(volumen_actual["sonido"][1]["nivel_volumen"])
                        escribir_json_sonido(False)

                    else:
                        sonido_ambiente.stop()
                        escribir_json_sonido(True)
                    
                if(btn_opciones_subir_volumen.checkear_input(mouse_posicion_opciones)):
                    
                    if(evaluar_sonido_json("partidas.json") == "1"):
                        
                        volumen_actual = leer_json("partidas.json")
                        
                        sonido_ambiente.set_volume(volumen_actual["sonido"][1]["nivel_volumen"])

                        if(volumen_actual["sonido"][1]["nivel_volumen"] < 1.0):

                            modificar_sonido(True)
                            
                        else:
                            print("NO SE PUEDE SEGUIR SUBIENDO EL VOLUMEN.")

                if(btn_opciones_bajar_volumen.checkear_input(mouse_posicion_opciones)):
                    
                    if(evaluar_sonido_json("partidas.json") == "1"):
                        
                        volumen_actual = leer_json("partidas.json")
                        
                        sonido_ambiente.set_volume(volumen_actual["sonido"][1]["nivel_volumen"])

                        if(volumen_actual["sonido"][1]["nivel_volumen"] > 0.1):

                            modificar_sonido(False)
                        else:

                            print("NO SE PUEDE SEGUIR BAJANDO EL VOLUMEN.")
                            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if btn_opciones_back.checkear_input(mouse_posicion_opciones):
                    
                    main_menu(screen)
    
        pygame.display.update()

def main_menu(screen:tuple[int,int])->None:
    '''
    Contiene la configuración de la pantalla principal.\n
    Recibe como parámetro la dimensión de la pantalla.\n
    Determina el tamaño y posición de los botones y lo que hace cada uno.
    '''

    pygame.display.set_caption("Menu")
    
    puntaje_usuario = Puntaje(0)
                    
    puntaje_usuario.set_puntaje(0)
    
    while main_menu:
        
        screen.blit(background,(0,0))
        
        posicion_mouse = pygame.mouse.get_pos()
        
        txt_menu = obtener_letra(70).render("MENU", True, NEGRO)
        rect_menu = txt_menu.get_rect(center=(750,150))

        #Configuro la parte visual de los votones y su posición.
        
        btn_jugar = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,250), text_input="PLAY", fuente = obtener_letra(50), color_base= LIGTH_GREEN, color_hover= BLANCO)
        btn_top_10 = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,350), text_input="TOP 10", fuente = obtener_letra(50), color_base= LIGTH_GREEN, color_hover= BLANCO)
        btn_opciones = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,450), text_input="OPTIONS", fuente = obtener_letra(50), color_base= LIGTH_GREEN, color_hover= BLANCO)
        btn_agregar_preguntas = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,550), text_input="ADD QUESTION", fuente = obtener_letra(46), color_base= LIGTH_GREEN, color_hover= BLANCO)
        btn_salir = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,650), text_input="EXIT", fuente = obtener_letra(50), color_base= LIGTH_GREEN, color_hover= BLANCO)
        
        lista_botones = [btn_jugar, btn_opciones, btn_salir, btn_top_10, btn_agregar_preguntas]
        
        screen.blit(txt_menu, rect_menu)
        
        for boton in lista_botones:
            
            boton.cambiar_color(posicion_mouse)
            
            boton.actualizar(screen)
        
        #Determino la acción que realiza al clickear cada botón.
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if btn_jugar.checkear_input(posicion_mouse):
                    sonido_ambiente.stop()
                    sonido_juego.play(-1)
                    sonido_juego.set_volume(0.1)
                    csv_leido = leer_csv("preguntas.csv")
                    random.shuffle(csv_leido)
                    jugar(screen,csv_leido, 3, 0)

                if btn_opciones.checkear_input(posicion_mouse):
                    opciones(screen)
                
                if btn_top_10.checkear_input(posicion_mouse):
                    top_10_jugadores(screen)

                if btn_agregar_preguntas.checkear_input(posicion_mouse):
                    pantalla_agregar_pregunta(screen)

                if btn_salir.checkear_input(posicion_mouse):   
                    pygame.quit()  
                    sys.exit()
        
        pygame.display.update()
    
    main_menu(screen)   

def top_10_jugadores(screen:tuple[int,int])->None:
    '''
    Contiene la información de la pantalla "TOP 10 JUGADORES".\n
    Recibe como parámetro la dimensión de la pantalla.
    '''
    
    x, y = 50 , 150
    
    altura_linea = 20 + 30
    
    contador = 0
    
    json_ordenado = ordenar_json('partidas.json', 'jugador', 'puntaje') 
    
    top_10_json_ordenado = json_ordenado[:10]
    
    while True:
        
        screen.blit(background_top_10, (0,0))
        
        btn_volver = Boton(imagen=None, pos=(1380,800), text_input="BACK", fuente = obtener_letra(35), color_base = BLANCO, color_hover= LIGTH_RED)

        posicion_mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if btn_volver.checkear_input(posicion_mouse):
                    
                    main_menu(screen)
        
        txt_title = obtener_letra(50).render("TOP 10", True, NEGRO)
        rect_txt = txt_title.get_rect(center=(750,100))
        screen.blit(txt_title, rect_txt)

        y_actual = y
        
        for i in top_10_json_ordenado:
            
            txt_jugador = obtener_letra(20).render(f" Top:{(top_10_json_ordenado.index(i) + 1)} Nombre: {i['nombre']} - Puntaje: {i['puntaje']} - Fecha: {i['fecha']}", True, NEGRO)
            
            screen.blit(txt_jugador, (x,y_actual))
            
            y_actual += altura_linea

        btn_volver.cambiar_color(posicion_mouse)
        btn_volver.actualizar(screen)
        pygame.display.update()

def leer_csv(ruta_archivo:str)->dict:
    '''
    Abre el archivo csv en modo lectura y extrae como una lista y los pasa a un diccionario.\n
    Recibe como parámetro la ruta del archivo especificado.\n
    Retorna un diccionario.
    '''
    datos = []
    
    with open(ruta_archivo, mode='r', newline='', encoding ='UTF-8') as archivo_csv:
        
        lector_csv = csv.DictReader(archivo_csv)
        
        for fila in lector_csv:
            
            datos.append(dict(fila))

    return datos

def pedir_nombre_jugador(screen:tuple[int,int], puntaje:int)->None:
    '''
    Contiene la configuración de la pantalla donde el usuario pone su nombre.\n
    Recibe como parámetro la dimensión de la pantalla y el puntaje del usuario.
    '''

    sonido_juego.stop()
    datos = leer_json('partidas.json')
    
    if (datos['sonido'][0]['estado_reproduccion'] == "1"):
        sonido_ambiente.play()
    
    fecha_actual = datetime.datetime.today()
    fecha_actual = fecha_actual.strftime("%d/%m/%Y") 
    letra = ""
    txt_letra = obtener_letra(75).render(letra, True, BLANCO)
    x = 140
    rect_letra = txt_letra.get_rect(center=(x,250))
    
    while True:
        
        posicion_mouse = pygame.mouse.get_pos()
        screen.blit(difuminado,(0,0))
        
        txt_input = obtener_letra(70).render("INGRESE SU NOMBRE", True, BLANCO)
        rect_txt = txt_input.get_rect(center=(750,100))
        
        txt_aviso = obtener_letra(20).render("HASTA 12 CARACTERES", True, BLANCO)
        rect_aviso = txt_aviso.get_rect(center=(750,160))

        screen.blit(txt_aviso, rect_aviso)
        screen.blit(txt_input, rect_txt)

        btn_guardar = Boton(imagen=pygame.image.load("Assets/rect_difuminado.png"), pos=(750,750), text_input="SAVE", fuente = obtener_letra(55), color_base = BLANCO, color_hover= LIGTH_RED)

        btn_guardar.cambiar_color(posicion_mouse)
        btn_guardar.actualizar(screen)
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                
                print(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                    
                if btn_guardar.checkear_input(posicion_mouse):
                    
                    escribir_json(letra, puntaje, fecha_actual)
                    
                    main_menu(screen)
                
            if event.type == pygame.KEYDOWN:
                
                if len(letra) <12:
                    
                    letra += event.unicode
                        
                    txt_letra = obtener_letra(75).render(letra, True, BLANCO)
                        
                    rect_letra = txt_letra.get_rect(center=(750,250))
                    
                if event.key ==pygame.K_BACKSPACE:
                    
                    letra = letra[:-1]
            
            if event.type == pygame.KEYDOWN and event.key == 8:
                
                letra = letra[:-1]

                txt_letra = obtener_letra(75).render(letra, True, BLANCO)
                        
                rect_letra = txt_letra.get_rect(center=(750,250))
            
            if event.type == pygame.KEYDOWN and event.key == 32:
                
                letra += " "
                
                txt_letra = obtener_letra(75).render(letra, True, BLANCO)
                        
                rect_letra = txt_letra.get_rect(center=(750,250))

            if event.type == pygame.QUIT:
                
                pygame.quit()
                
                sys.exit()
                
            
        screen.blit(txt_letra, rect_letra)
        pygame.display.update()

def leer_json(ruta_json:str)->dict:
    '''
    Abre y lee los datos del archivo json.
    Recibe como parámetro la ruta del archivo.
    Retorna un diccionario con los datos.
    '''
    archivo_json = open(ruta_json, 'r')
    datos = json.load(archivo_json) 
    archivo_json.close()
    return datos

def escribir_json(letra:str, puntaje:int, fecha_actual:str)->None:
    '''
    Abre e ingresa los datos especificados en el archivo json.\n
    Recibe como parámetro el nombre (puesto como letra), el puntaje y la fecha actual.\n
    No retorna nada.
    '''
    datos = leer_json('partidas.json')
    
    ultimos_datos = {'nombre': letra, 'puntaje': puntaje, 'fecha':fecha_actual}
    
    datos["jugador"].append(ultimos_datos)
                    
    with open("partidas.json", "w") as file:
                        
        json.dump(datos, file, indent=4)
    
    file.close()

def ordenar_json(ruta_json:str, clave_json:str, clave_orden:str)->dict:
    '''
    Ordena de mayor a menor a los jugadores.\n
    Recibe como parámetro la ruta del json, la clave a tomar en consideración y la clave para ordenar.\n
    Retorna una diccionario ordenado de los elementos del archivo JSON en orden descendente según la clave de orden especificada.
    '''
    
    archivo_json = leer_json(ruta_json)
    
    jugadores_ordenados = sorted(archivo_json[clave_json], key=lambda x: x[clave_orden], reverse=True)
                
    return jugadores_ordenados

def cargar_csv_lista(ruta:str)->list:
    '''
    Abre el archivo csv e ingresa los datos en una lista.\n
    Toma como parámetro la ruta especificada.\n
    Retorna una lista con la información.
    '''
    with open(ruta, mode='r', newline='', encoding='utf8') as archivo:
        
        lector = csv.DictReader(archivo)
        
        return list(lector)

def modificar_dato_pregunta(pregunta:str, clave:str)->None:
    '''
    Modifica dentro del archivo csv el dato especificado de la pregunta especificada.\n
    Ingresa como parámetro la pregunta y su clave.\n
    '''
    lista_archivo = cargar_csv_lista('preguntas.csv')
    
    for i in lista_archivo:
        if i['pregunta'] == pregunta:
            #verifica si el valor actual de 'clave' es un número válido
            if i[clave].isdigit():
                i[clave] = int(i[clave]) + 1
            else:
                #si éste no es un número, inicializa con 1
                i[clave] = 1
            #cadena para guardar en el CSV
            i[clave] = str(i[clave])
    #guardar en el archivo CSV
    with open('preguntas.csv', mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=lista_archivo[0].keys())
        escritor.writeheader()
        escritor.writerows(lista_archivo)

def calcular_y_modificar_porcentaje_aciertos(pregunta:str)-> int:
    '''
    Modifica el porcentaje de aciertos en el CSV.\n
    Ingresa como parámetro la pregunta.\n
    Retorna el porcentaje actualizado de aciertos.
    '''
    
    lista_archivo = cargar_csv_lista('preguntas.csv')

    for i in lista_archivo:
        
        if i ['pregunta'] == pregunta:
            
            cantidad_aciertos = int(i['cantidad_aciertos'])
        
            cantidad_veces_preguntadas = int(i['cantidad_veces_preguntada'])

            cantidad_fallos = int(i['cantidad_fallos'])
            
            porcentaje_fallos = int((cantidad_fallos/ cantidad_veces_preguntadas) * 100)
            
            if cantidad_veces_preguntadas >= 2:
                
                i['porcentaje_aciertos'] = int((cantidad_aciertos / cantidad_veces_preguntadas) * 100)
            
            elif  int((cantidad_aciertos / cantidad_veces_preguntadas) * 100) != 0:
            
                i['porcentaje_aciertos'] =  int((cantidad_aciertos / cantidad_veces_preguntadas) * 100)  - porcentaje_fallos

    with open('preguntas.csv', mode='w', newline='', encoding='utf-8') as archivo:
        
        escritor = csv.DictWriter(archivo, fieldnames=lista_archivo[0].keys())
        escritor.writeheader()
        escritor.writerows(lista_archivo)

def reproducir_musica_fondo()->None:
    '''
    Hace que comience la reproducción de la música de fondo.
    '''
    escribir_json_sonido(False)
    sonido_ambiente.play()
    volumen_actual = leer_json("partidas.json")
    sonido_ambiente.set_volume(volumen_actual["sonido"][1]["nivel_volumen"])

def evaluar_sonido_json(ruta_json:str)->int:
    '''
    Lee el archivo json y extrae la información necesaria.\n
    Ingresa como parámetro la ruta del archivo.\n
    Retorna el estado del sonido.
    '''

    datos = leer_json(ruta_json)

    estado_sonido = datos["sonido"][0]["estado_reproduccion"]

    return estado_sonido

def modificar_sonido(valor:bool)->None:
    '''
    Lee los datos del archivo json y aumenta o disminuye el sonido.
    '''
    datos = leer_json("partidas.json")

    if(valor == True):
        datos["sonido"][1]["nivel_volumen"] += 0.1

    elif(valor == False and datos["sonido"][1]["nivel_volumen"] != 0.10000000000000003):

        datos["sonido"][1]["nivel_volumen"] -= 0.1

    with open("partidas.json","w+") as archivo:

        json.dump(datos,archivo,indent=4)

def obtener_letra(tamaño:int)->None:
    '''
    Tiene como parámetro el tamaño de la letra deseada.\n
    Retorna la función para cambiar el tipo de letra.
    '''
    return pygame.font.Font("Assets/font.ttf", tamaño)

def escribir_json_sonido(valor_antiguo:bool)->None:
    '''
    Lee los datos del json, extrae la información del sonido y la modifica en base al parámetro ingresado.\n
    Ingresa por parámetro el estado del sonido anterior (si está encendido o apagado).
    '''

    datos = leer_json('partidas.json')

    if(valor_antiguo == True):
        datos["sonido"][0]["estado_reproduccion"] = "0"
    else:
        datos["sonido"][0]["estado_reproduccion"] = "1"

    with open("partidas.json", "w") as file:

        json.dump(datos, file, indent=4)

    file.close()

def agregar_pregunta(pregunta:str, respuesta_a:str, respuesta_b:str, respuesta_c:str, respuesta_d:str, respuesta_correcta:str)->None:
    '''
    Abre el archivo csv y permite agregar una nueva pregunta al mismo.\n
    Recibe como parámetro la pregunta y sus respectivas respuestas.
    '''
    with open('preguntas.csv', mode='a', newline='', encoding='utf-8') as file:  # Asegúrate de incluir encoding
        writer = csv.writer(file)
        writer.writerow([pregunta, respuesta_a, respuesta_b, respuesta_c, respuesta_d, respuesta_correcta, 0, 0, 0, 0])

def pantalla_agregar_pregunta(screen:tuple[int,int])->None:
    '''
    Contiene toda la configuración de la pantalla de "Agregar pregunta".\n
    Recibe como parámetro la dimensión de la pantalla.
    '''
    # Variables para las entradas de texto
    campos = ["pregunta", "respuesta_a", "respuesta_b", "respuesta_c", "respuesta_d", "respuesta_correcta"]
    valores = {campo: "" for campo in campos}  # Almacena los valores de cada campo
    campo_activo = 0  # Indica qué campo está actualmente activo para escribir

    while True:
        # Limpia y redibuja el fondo en cada iteración
        screen.blit(fondo_pantalla_agregar_preguntas, (0, 0))

        txt_titulo = obtener_letra(50).render("ADD QUESTIONS", True, NEGRO)
        rect_txt = txt_titulo.get_rect(center=(750, 100))
        screen.blit(txt_titulo, rect_txt)

        # Botones
        btn_volver = Boton(imagen=None, pos=(1380, 800), text_input="BACK", fuente=obtener_letra(35), color_base=BLANCO, color_hover=LIGTH_RED)
        btn_agregar_pregunta = Boton(imagen=None, pos=(750, 700), text_input="ADD", fuente=obtener_letra(35), color_base=LIGTH_GREEN, color_hover=RED)
        posicion_mouse = pygame.mouse.get_pos()

        # Actualizar botones
        btn_volver.cambiar_color(posicion_mouse)
        btn_agregar_pregunta.cambiar_color(posicion_mouse)
        btn_volver.actualizar(screen)
        btn_agregar_pregunta.actualizar(screen)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Manejar clics en los botones
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.checkear_input(posicion_mouse):
                    main_menu(screen)  # Regresar al menú principal

                if btn_agregar_pregunta.checkear_input(posicion_mouse):
                    agregar_pregunta(
                        valores["pregunta"],
                        valores["respuesta_a"],
                        valores["respuesta_b"],
                        valores["respuesta_c"],
                        valores["respuesta_d"],
                        valores["respuesta_correcta"],
                    )
                    # Limpiar los valores después de agregar
                    valores = {campo: "" for campo in campos}
                    campo_activo = 0

            #tecla TAB
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    campo_activo = (campo_activo + 1) % len(campos)

                #campo activo
                elif evento.key == pygame.K_BACKSPACE:
                    valores[campos[campo_activo]] = valores[campos[campo_activo]][:-1]
                elif len(valores[campos[campo_activo]]) < 50:  # Limitar longitud
                    valores[campos[campo_activo]] += evento.unicode
        # Mostrar los campos y los textos ingresados
        y_offset = 200
        for i, campo in enumerate(campos):
            color = NEGRO if i == campo_activo else BLANCO
            texto_campo = obtener_letra(30).render(f"{campo.replace('_', ' ').upper()}: {valores[campo]}", True, color)
            rect_campo = texto_campo.get_rect(topleft=(100, y_offset))
            screen.blit(texto_campo, rect_campo)
            y_offset += 80  # Incremento para cada línea

        # Actualizar la pantalla
        pygame.display.update()

def eliminar_pregunta(preguntas:list, pregunta)->None:

    '''
    Elimina la pregunta que tocó dentro de la lista de preguntas (por partida)
    '''
    for i in range(len(preguntas)):
        
        if preguntas[i]["pregunta"] == pregunta:
            
            preguntas.pop(i)
            
            break