class Jugador:
    def __init__(self, personaje_db):
        self.x = personaje_db.x
        self.y = personaje_db.y
        self.velocidad = personaje_db.velocidad
        
        
    def movimiento_personaje(self, key, ancho=100, alto=100, W=1000, H=500):
        x = self.x
        y = self.y
        
        if key == "d":
            x = x + self.velocidad
        elif key == "a":
            x = x - self.velocidad
        elif key == "w":
            y = y - self.velocidad
        elif key == "s":
            y = y + self.velocidad
            
        self.x = x
        self.y = y

        # Límite real del plano: el borde del personaje no puede salir de la imagen
        x = max(0, min(x, W - ancho))
        y = max(0, min(y, H - alto))
        self.x = x
        self.y = y

        return x, y

    def hay_colision(self, xA, yA, anchoA, altoA, xB, yB, anchoB, altoB):
        solapan_en_x = (xA < xB + anchoB) and (xB < xA + anchoA)
        solapan_en_y = (yA < yB + altoB) and (yB < yA + altoA)
        return solapan_en_x and solapan_en_y