from flask import Flask, request, jsonify  # Importamos Flask y utilidades para manejar peticiones HTTP y respuestas en JSON

app = Flask(__name__)  # Creamos una instancia de la aplicación Flask

frutas = {}  # Diccionario en memoria para almacenar las frutas con su ID
contador_id = 1  # Contador para generar IDs únicos

# Ruta para obtener todas las frutas, opcionalmente filtrando por nombre
@app.route("/frutas", methods=["GET"])
def obtener_frutas():
    nombre_filtro = request.args.get("nombre")  # Obtenemos el parámetro de búsqueda por nombre, si existe
    if nombre_filtro:
        # Filtramos las frutas que coincidan con el nombre (ignorando mayúsculas/minúsculas)
        resultado = [f for f in frutas.values() if f["nombre"].lower() == nombre_filtro.lower()]
        return jsonify(resultado), 200  # Retornamos la lista filtrada
    return jsonify(list(frutas.values())), 200  # Retornamos todas las frutas si no hay filtro

# Ruta para agregar una nueva fruta favorita
@app.route("/frutas", methods=["POST"])
def agregar_fruta():
    global contador_id  # Indicamos que vamos a modificar la variable global del contador
    datos = request.get_json()  # Obtenemos los datos enviados por el cliente en formato JSON
    nombre = datos.get("nombre")  # Extraemos el campo "nombre"

    if not nombre:
        # Validamos que se haya proporcionado un nombre
        return jsonify({"error": "Se requiere el nombre de la fruta"}), 400

    # Creamos un nuevo objeto de fruta con ID y nombre
    nueva_fruta = {"id": contador_id, "nombre": nombre}
    frutas[contador_id] = nueva_fruta  # Lo guardamos en el diccionario
    contador_id += 1  # Incrementamos el ID para la próxima fruta

    return jsonify(nueva_fruta), 201  # Devolvemos la nueva fruta con código 201 (creado)

# Ruta para actualizar el nombre de una fruta existente
@app.route("/frutas/<int:id_fruta>", methods=["PUT"])
def actualizar_fruta(id_fruta):
    datos = request.get_json()  # Obtenemos los datos enviados
    nuevo_nombre = datos.get("nombre")  # Extraemos el nuevo nombre

    if id_fruta not in frutas:
        # Verificamos que la fruta exista
        return jsonify({"error": "Fruta no encontrada"}), 404
    if not nuevo_nombre:
        # Validamos que se haya enviado un nuevo nombre
        return jsonify({"error": "Se requiere un nuevo nombre"}), 400

    frutas[id_fruta]["nombre"] = nuevo_nombre  # Actualizamos el nombre de la fruta
    return jsonify(frutas[id_fruta]), 200  # Devolvemos la fruta actualizada

# Ruta para eliminar una fruta por su ID
@app.route("/frutas/<int:id_fruta>", methods=["DELETE"])
def eliminar_fruta(id_fruta):
    if id_fruta not in frutas:
        # Verificamos que el ID exista
        return jsonify({"error": "Fruta no encontrada"}), 404

    fruta_eliminada = frutas.pop(id_fruta)  # Eliminamos la fruta del diccionario y la guardamos para mostrar
    return jsonify(fruta_eliminada), 200  # Respondemos con los datos de la fruta eliminada

# Ejecutamos la app en modo desarrollo si este archivo es el principal
if __name__ == "__main__":
    app.run(debug=True)  # Iniciamos el servidor Flask con modo depuración activado
