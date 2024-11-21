from flask import Blueprint, jsonify, request
from modelos.repositorios.repositorios import obtenerRepoBebidas
from modelos.entidades.bebida import Bebida
from modelos.entidades.bebidaConAlcohol import BebidaConAlcohol 
from modelos.entidades.bebidaSinAlcohol import BebidaSinAlcohol

repo_bebidas = obtenerRepoBebidas()

bp_bebidas = Blueprint("bp_bebidas", __name__)

@bp_bebidas.route("/bebidas", methods = ["GET"])
def listar_bebidas():
    return jsonify([bebida.toDiccionario() for bebida in repo_bebidas.obtenerBebidas()])

@bp_bebidas.route("/bebidas/<string:nombre>", methods = ["GET"])
def obtener_bebida(nombre):
    bebida = repo_bebidas.obtenerBebidaPorNombre(nombre)
    if bebida == None:
        return jsonify({"error": "Bebida no encontrada"}), 404
    return jsonify(bebida.toDiccionario()), 200 #el codigo retornado estaba mal, debe ser 200

#faltaba el parametro que nos manda el usuario para saber que bebida eliminar (<string:nombre>)    
@bp_bebidas.route("/bebidas/<string:nombre>", methods = ["DELETE"])
def eliminar_bebida(nombre):
    if repo_bebidas.eliminarBebida(nombre):
        return jsonify({"Mensaje":f"Bebida eliminada con éxito."}), 200
    return jsonify({"error": "No se encontró la bebida a eliminar"}), 404


@bp_bebidas.route("/bebidas/<string:nombre>/precio", methods=["GET"])
def obtener_precio_bebida(nombre):
    print(f"Nombre de bebida recibido: {nombre}")  # Imprime el nombre recibido
    bebida = repo_bebidas.obtenerBebidaPorNombre(nombre)
    if bebida is None:
        return jsonify({"error": "Bebida no encontrada"}), 404
    return jsonify({"nombre": bebida.obtenerNombre(), "precio": bebida.obtenerPrecio()}), 200 #el codigo retornado estaba mal, debe ser 



# Agregamos funcion CREATE
@bp_bebidas.route("/bebidas", methods=["POST"])
def agregar_bebida():
    if request.is_json:
        # Recibir los datos del JSON enviado por el cliente
        data=request.get_json()
        try:
            # Recibir los datos JSON del cliente
            data = request.get_json()

            # Crear la bebida a partir del diccionario recibido
            if "graduacionAlcoholica" in data:
                bebida = BebidaConAlcohol.fromDiccionario(data)
            else:
                bebida = BebidaSinAlcohol.fromDiccionario(data)

            # Agrega y guarda la bebida al repositorio
            repo_bebidas.agregarBebida(bebida)

            # Retornar la bebida agregada con el código 201
            return jsonify(bebida.toDiccionario()), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400  # Error 400 si los datos no son validos
        except Exception as e:
            return jsonify({'error': f"Error al agregar bebida: {str(e)}"}), 500  # Manejar cualquier otro error
    else:
        return jsonify({'error': 'El contenido debe ser Json'}), 400

# Agregamos funcion UPDATE
@bp_bebidas.route("/bebidas/<string:nombre>", methods=["PUT"])
def modificar_bebida(nombre):
    if request.is_json:
        datos = request.get_json()

        # Verificamos que los datos necesarios estén presentes en la solicitud
        if "costo" in datos and "mililitros" in datos and "precio" in datos and "stock" in datos:
            costo = datos["costo"]
            mililitros = datos["mililitros"]
            precio = datos["precio"]
            stock = datos["stock"]
            
            # Verificamos si la bebida es con alcohol
            if "graduacionAlcoholica" in datos:
                graduacion_alcoholica = datos["graduacionAlcoholica"]
                bebida = BebidaConAlcohol(nombre, costo, stock, mililitros, graduacion_alcoholica)
            else:
                # Es bebida sin alcohol, por lo que el campo "sabor" y "natural" son necesarios
                if "sabor" not in datos or "natural" not in datos:
                    return jsonify({'error': 'Faltan datos: "sabor" o "natural"'}), 400

                sabor = datos["sabor"]
                natural = datos["natural"]
                bebida = BebidaSinAlcohol(nombre, costo, stock, mililitros, sabor, natural)

            # Intentamos modificar la bebida en el repositorio
            if repo_bebidas.modificarBebida(nombre, bebida):
                return jsonify({'mensaje': 'Bebida modificada exitosamente'}), 200
            else:
                return jsonify({'error': 'No se encontró la bebida'}), 404
        else:
            return jsonify({'error': 'Faltan datos'}), 400
    else:
        return jsonify({'error': 'El contenido debe ser Json'}), 400
