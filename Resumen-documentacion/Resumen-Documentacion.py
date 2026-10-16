
import threading
import time
import requests

SERVICIOS = {
    "Python": "https://www.python.org/",
    "PyPI": "https://pypi.org/",
    "GitHub": "https://github.com/",
    "Google": "https://www.google.com/",
    "HTTPBin": "https://httpbin.org/status/200",
    "Web de prueba": "https://httpbin.org/status/500"
}

TIMEOUT = 6


def comprobar_web(nombre, url):
    """Comprueba una web y devuelve True si responde correctamente."""
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)

        if respuesta.status_code < 400:
            print(f"[{nombre}] Disponible - HTTP {respuesta.status_code}")
            return True

        print(f"[{nombre}] Error HTTP - {respuesta.status_code}")
        return False

    except requests.Timeout:
        print(f"[{nombre}] Error: tiempo de espera agotado")
        return False

    except requests.RequestException as error:
        print(f"[{nombre}] Error de conexión: {error}")
        return False


def version_secuencial():
    """Comprueba los servicios uno después de otro."""
    print("\n--- VERSIÓN SECUENCIAL ---")
    inicio = time.perf_counter()
    disponibles = 0

    for nombre, url in SERVICIOS.items():
        if comprobar_web(nombre, url):
            disponibles += 1

    tiempo_total = time.perf_counter() - inicio
    return disponibles, tiempo_total


def version_concurrente():
    """Comprueba los servicios mediante hilos."""
    print("\n--- VERSIÓN CONCURRENTE ---")
    inicio = time.perf_counter()
    resultados = {}
    hilos = []

    def tarea(nombre, url):
        resultados[nombre] = comprobar_web(nombre, url)

    for nombre, url in SERVICIOS.items():
        hilo = threading.Thread(
            target=tarea,
            args=(nombre, url),
            name=f"web-{nombre}"
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    tiempo_total = time.perf_counter() - inicio
    disponibles = sum(resultados.values())

    return disponibles, tiempo_total


def mostrar_resumen(disponibles_seq, tiempo_seq,
                    disponibles_conc, tiempo_conc):
    """Muestra el resumen final de las dos versiones."""
    total = len(SERVICIOS)
    errores_seq = total - disponibles_seq
    errores_conc = total - disponibles_conc

    print("\n===============================")
    print("RESUMEN DEL MONITOR")
    print("===============================")
    print(f"Servicios comprobados: {total}")
    print(f"Disponibles (secuencial): {disponibles_seq}")
    print(f"Con error (secuencial): {errores_seq}")
    print(f"Disponibles (concurrente): {disponibles_conc}")
    print(f"Con error (concurrente): {errores_conc}")
    print(f"Tiempo secuencial: {tiempo_seq:.2f} s")
    print(f"Tiempo concurrente: {tiempo_conc:.2f} s")

    if tiempo_conc > 0:
        mejora = tiempo_seq / tiempo_conc
        print(f"Relación de velocidad: {mejora:.2f}x")

    if tiempo_conc < tiempo_seq:
        print("Conclusión: la versión concurrente ha tardado menos.")
    elif tiempo_conc > tiempo_seq:
        print("Conclusión: la versión secuencial ha tardado menos.")
    else:
        print("Conclusión: ambas versiones han tardado lo mismo.")


def main():
    disponibles_seq, tiempo_seq = version_secuencial()
    disponibles_conc, tiempo_conc = version_concurrente()

    mostrar_resumen(
        disponibles_seq,
        tiempo_seq,
        disponibles_conc,
        tiempo_conc
    )


if __name__ == "__main__":
    main()
