from modelos.entidades.bebida import Bebida

class BebidaConAlcohol(Bebida):
    def __init__(self, nombre:str, costo:float, stock:int, mililitros:int, graduacionAlcoholica: float):
        super().__init__(nombre, costo, stock, mililitros)
        if not isinstance(graduacionAlcoholica, (int, float)) or graduacionAlcoholica < 0 or graduacionAlcoholica > 100:
            raise ValueError("La graduación alcohólica debe ser un número positivo")
        self.__graduacionAlcoholica = graduacionAlcoholica


    #agrego el metodo fromDiccionario para poder crear instancias de esta clase al recibir un diccionario con informacion
    @classmethod
    def fromDiccionario(cls, diccionario):
        if not isinstance(diccionario, dict):
            raise ValueError("El parametro debe ser un diccionario")
        
        claves_requeridas = ['nombre', 'costo', 'stock', 'mililitros', 'graduacionAlcoholica']
        for clave in claves_requeridas:
            if clave not in diccionario:
                raise ValueError(f"Falta la clave {clave} en el diccionario")

        return cls(
            diccionario['nombre'],
            diccionario['costo'],
            diccionario['stock'],
            diccionario['mililitros'],
            diccionario['graduacionAlcoholica']
        )

    def obtenerPrecio(self):
        return self._costo * 1.6
    
    def obtenerGraduacionAlcoholica(self):
        return self.__graduacionAlcoholica
    
    def establecerGraduacionAlcoholica(self, graduacionAlcoholica:float):
        if not isinstance(graduacionAlcoholica, (int, float)) or graduacionAlcoholica < 0 or graduacionAlcoholica > 100:
            raise ValueError("La graduación alcohólica debe ser un número positivo")
        self.__graduacionAlcoholica = graduacionAlcoholica

    # Eliminamos los campos 'sabor' y 'natural' del diccionario en esta clase 
    # porque no son atributos de BebidaConAlcohol. Estos campos solo existen 
    # en la clase BebidaSinAlcohol, tambien agregamos self.obtenerGraduacionAlcoholica(), que no estaba
    def toDiccionario(self):
        return {
            "nombre": self._nombre,  
            "costo": self._costo,
            "stock": self._stock,
            "mililitros": self._mililitros,
            "graduacionAlcoholica": self.obtenerGraduacionAlcoholica(),
            "precio": self.obtenerPrecio()  
        }