from modelos.entidades.bebida import Bebida

class BebidaSinAlcohol(Bebida):
    def __init__(self, nombre:str, costo:float, stock:int, mililitros:int, sabor: str, natural: bool):
        super().__init__(nombre, costo, stock, mililitros)
        if not isinstance(sabor, str) or not sabor.strip():
            raise ValueError("El sabor debe ser un string y no puede estar vacío")
        if not isinstance(natural, bool):
            raise ValueError("El atributo natural debe ser booleano")
        self.__sabor = sabor
        self.__natural = natural

    #agrego el metodo fromDiccionario para poder crear instancias de esta clase al recibir un diccionario con informacion
    @classmethod
    def fromDiccionario(cls, diccionario):
        if not isinstance(diccionario, dict):
            raise ValueError("El parámetro debe ser un diccionario")
        
        claves_requeridas = ['nombre', 'costo', 'stock', 'mililitros', 'sabor', 'natural']
        for clave in claves_requeridas:
            if clave not in diccionario:
                raise ValueError(f"Falta la clave {clave} en el diccionario")

        return cls(
            diccionario['nombre'],
            diccionario['costo'],
            diccionario['stock'],
            diccionario['mililitros'],
            diccionario['sabor'],
            diccionario['natural']
        )
    
    
    def obtenerSabor(self):
        return self.__sabor
    
    def obtenerNatural(self):
        return self.__natural
    
    def establecerSabor(self, sabor:str):
        if not isinstance(sabor, str) or sabor == "":
            raise ValueError("El sabor no puede ser vacío")
        self.__sabor = sabor
    
    def establecerNatural(self, natural:bool):
        if not isinstance(natural, bool):
            raise ValueError("El atributo natural debe ser booleano")
        self.__natural = natural

    def obtenerPrecio(self):
        return self._costo * 1.5
    
    def toDiccionario(self):
        return {
            "nombre": self.obtenerNombre(),
            "costo": self.obtenerCosto(),
            "stock": self.obtenerStock(),
            "mililitros": self.obtenerMililitros(),
            "sabor": self.obtenerSabor(),
            "natural": self.obtenerNatural(),
            "precio": self.obtenerPrecio()
        }
