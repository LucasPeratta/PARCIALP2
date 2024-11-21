from modelos.entidades.bebidaConAlcohol import BebidaConAlcohol
from modelos.entidades.bebidaSinAlcohol import BebidaSinAlcohol
from modelos.entidades.bebida import Bebida
import json

class RepositorioBebidas:
    ruta_archivo = "datos/bebidas.json"

    def __init__(self):
        self.__bebidas = []
        self.__cargarBebidas()

    def __cargarBebidas(self):
        try:
            with open(RepositorioBebidas.ruta_archivo, "r") as archivo:
                lista_dicc_bebidas = json.load(archivo)
                for bebida in lista_dicc_bebidas:
                    if "graduacionAlcoholica" in bebida:
                        self.__bebidas.append(BebidaConAlcohol.fromDiccionario(bebida))
                    else:
                        self.__bebidas.append(BebidaSinAlcohol.fromDiccionario(bebida))
        except FileNotFoundError:
            print("No se encontró el archivo de bebidas")
        except Exception as e:
            print("Error cargando las bebidas del archivo.\n" + str(e))

    def __guardarBebidas(self):
        try:
            with open(RepositorioBebidas.ruta_archivo, "w") as archivo:
                lista_dicc_bebidas = [bebida.toDiccionario() for bebida in self.__bebidas]
                json.dump(lista_dicc_bebidas, archivo, indent=4)
        except Exception as e:
            print("Error guardando las bebidas en el archivo.\n" + str(e))
    
    def obtenerBebidas(self):
        """Retorna una lista con todas las bebidas"""
        return self.__bebidas
    
    def obtenerBebidaPorNombre(self, nombre:str):
        """Retorna la bebida con el nombre indicado, None si no existe"""
        for bebida in self.__bebidas:
            if bebida.obtenerNombre() == nombre:
                return bebida
        return None
    
    def existeBebida(self, nombre:str):
        """Retorna True si existe una bebida con el nombre indicado, False en caso contrario"""
        return self.obtenerBebidaPorNombre(nombre) != None
    

    #agregamos el metodo eliminarBebida para poder hacer el delete en "rutas_bebidas.py"
    def eliminarBebida(self, nombre: str):
        bebida = self.obtenerBebidaPorNombre(nombre)
        if bebida:
            self.__bebidas.remove(bebida)  # Elimina la bebida de la lista
            self.__guardarBebidas()         # Guarda los cambios en el archivo
            return True
        return False
    


    # AGREGAMOS funcion para el POST en "rutas_bebidas.py"
    def agregarBebida(self, bebida):
        # Verificamos si el objeto bebida es de la clase correcta
        if not isinstance(bebida, (BebidaConAlcohol, BebidaSinAlcohol)):
            raise ValueError('El parametro debe ser una instancia de BebidaConAlcohol o BebidaSinAlcohol')
        
        # Verificamos si ya existe una bebida con el mismo nombre
        if self.existeBebida(bebida.obtenerNombre()):
            raise ValueError('Ya existe una bebida con el mismo nombre')

        # Agregamos la bebida a la lista interna
        self.__bebidas.append(bebida)

        # Guardamos los cambios en el archivo
        self.__guardarBebidas()

    
    # AGREGAMOS funcion para el PUT en "rutas_bebidas.py"
    def modificarBebida(self, nombre: str, nueva_bebida):
        bebida_existente = self.obtenerBebidaPorNombre(nombre)
        
        if bebida_existente:
            # Encontramos la bebida y la reemplazamos por la nueva bebida
            indice = self.__bebidas.index(bebida_existente)
            self.__bebidas[indice] = nueva_bebida  # Reemplazamos la bebida existente por la nueva

            # Guardamos los cambios en el archivo
            self.__guardarBebidas()
            return True
        return False
