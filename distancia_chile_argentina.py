import requests

API_KEY = "5ed51020-dbd1-4218-85cc-5a178cc31ac4"  

GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"


def geocodificar(ciudad, pais):
    """Convierte un nombre de ciudad + país en coordenadas lat/lng.
    Prioriza resultados etiquetados como ciudad/pueblo real para evitar
    puntos genéricos sin conexión vial."""
    params = {"q": f"{ciudad}, {pais}", "limit": 5, "key": API_KEY}
    resp = requests.get(GEOCODE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    hits = data.get("hits", [])
    if not hits:
        return None

    prioridad = ["city", "town", "village", "municipality"]
    mejor_hit = None

    
    for tipo in prioridad:
        for hit in hits:
            if hit.get("osm_value") == tipo and hit.get("country", "").lower() == pais.lower():
                mejor_hit = hit
                break
        if mejor_hit:
            break

    
    if not mejor_hit:
        for hit in hits:
            if hit.get("country", "").lower() == pais.lower():
                mejor_hit = hit
                break

    
    if not mejor_hit:
        mejor_hit = hits[0]

    return mejor_hit["point"]["lat"], mejor_hit["point"]["lng"], mejor_hit.get("name", ciudad)


def elegir_transporte():
    """Menú para elegir el medio de transporte del viaje."""
    opciones = {"1": "car", "2": "bike", "3": "foot"}
    print("\nSeleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. A pie")
    while True:
        opcion = input("Opción (1-3): ")
        if opcion in opciones:
            return opciones[opcion]
        print("Opción inválida, intente nuevamente.")


def consultar_ruta(origen, destino, vehiculo):
    """Consulta la ruta entre dos puntos usando la Routing API de GraphHopper."""
    params = {
        "point": [f"{origen[0]},{origen[1]}", f"{destino[0]},{destino[1]}"],
        "vehicle": vehiculo,
        "instructions": "true",
        "locale": "es",
        "key": API_KEY,
    }
    resp = requests.get(ROUTE_URL, params=params)
    if resp.status_code != 200:
        
        try:
            detalle = resp.json().get("message", resp.text)
        except ValueError:
            detalle = resp.text
        print(f">> GraphHopper respondió {resp.status_code}: {detalle}")
        resp.raise_for_status()
    return resp.json()


def main():
    print("=" * 55)
    print("CALCULADORA DE DISTANCIA CHILE - ARGENTINA (GraphHopper API)")
    print("=" * 55)

    while True:
        origen_ciudad = input("\nIngrese la Ciudad de Origen (Chile) [o 's' para salir]: ")
        if origen_ciudad.lower() == "s":
            print("Saliendo del programa...")
            break

        destino_ciudad = input("Ingrese la Ciudad de Destino (Argentina) [o 's' para salir]: ")
        if destino_ciudad.lower() == "s":
            print("Saliendo del programa...")
            break

        origen = geocodificar(origen_ciudad, "Chile")
        destino = geocodificar(destino_ciudad, "Argentina")

        if not origen or not destino:
            print(">> No se pudo encontrar una de las ciudades ingresadas. Intente nuevamente.")
            continue

        print(f"\nOrigen encontrado: {origen[2]} ({origen[0]:.4f}, {origen[1]:.4f})")
        print(f"Destino encontrado: {destino[2]} ({destino[0]:.4f}, {destino[1]:.4f})")

        vehiculo = elegir_transporte()

        try:
            ruta = consultar_ruta(origen, destino, vehiculo)
        except requests.exceptions.HTTPError as e:
            print(f">> Error al consultar la ruta: {e}")
            continue

        if "paths" not in ruta or len(ruta["paths"]) == 0:
            print(">> No se encontró una ruta disponible para este medio de transporte entre estas ciudades.")
            continue

        path = ruta["paths"][0]
        distancia_m = path["distance"]
        distancia_km = distancia_m / 1000
        distancia_millas = distancia_m / 1609.34
        tiempo_ms = path["time"]
        horas = tiempo_ms // (1000 * 60 * 60)
        minutos = (tiempo_ms // (1000 * 60)) % 60

        print("\n" + "=" * 55)
        print(f"RESULTADOS DEL VIAJE ({vehiculo.upper()})")
        print("=" * 55)
        print(f"Distancia: {distancia_km:.2f} km  |  {distancia_millas:.2f} millas")
        print(f"Duración estimada: {int(horas)}h {int(minutos)}min")

        print("\n--- NARRATIVA DEL VIAJE ---")
        for instr in path.get("instructions", []):
            print(f"- {instr['text']}")
        print()


if __name__ == "__main__":
    main()