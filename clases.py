class Boton:
    def __init__(self, imagen, pos, text_input, fuente, color_base, color_hover):
        self.imagen = imagen
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.fuente = fuente
        self.color_base = color_base
        self.color_hover = color_hover
        self.text = self.fuente.render(self.text_input, True, self.color_base)   
        # Si no hay imagen, se utiliza el texto como botón
        if self.imagen is None:
            self.imagen = self.text
        # Rectángulo del botón
        self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def actualizar(self, screen):
        """Dibuja el boton en la pantalla."""
        if self.imagen is not None:
            screen.blit(self.imagen, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkear_input(self, position):
        """Devuelve True si el mouse está sobre el boton."""
        return self.rect.collidepoint(position)

    def cambiar_color(self, position):
        """Cambia el color del texto si el mouse está sobre el boton."""
        if self.checkear_input(position):  # Usa directamente collidepoint
            self.text = self.fuente.render(self.text_input, True, self.color_hover)
        else:
            self.text = self.fuente.render(self.text_input, True, self.color_base)
			

class Vidas(): 
    def __init__(self, cantidad):
        self.cantidad = int(cantidad)
    def set_vidas(self, respuesta):
        if respuesta == False:   
            self.cantidad -= 1
        return self.cantidad
    def get_vidas(self): 
        return self.cantidad

class Puntaje():
    def __init__(self, puntaje):
        self.puntaje =int(puntaje)
    def set_puntaje(self, valor):  
        self.puntaje += valor
        return self.puntaje
    def get_puntaje(self):
        return self.puntaje
