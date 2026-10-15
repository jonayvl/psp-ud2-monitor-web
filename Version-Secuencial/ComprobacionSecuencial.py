import time
import requests

urls = [
    "https://www.python.orgg/",
    "https://ppi.org/",
    "https://github.com/"
]

Online = 0
ErrorHttp = 0
tiempoExpirado = 0
ErrorConexion = 0


def comprobar_web(url):
    global Online , ErrorHttp , tiempoExpirado , ErrorConexion

    inicio = time.perf_counter()
    
    try:
        respuesta = requests.get(url, timeout=6)
        tiempo = time.perf_counter() - inicio
        codigo = respuesta.status_code
        if codigo >= 400:
            Errorhttp += 1
            print(f"URL: {url} - ERROR HTTP ({codigo}) - Tiempo: {tiempo:.2f}s")
        else:
            Online += 1
            print(f"URL: {url} - ONLINE ({codigo}) - Tiempo: {tiempo:.2f}s")
    except requests.Timeout:
        tiempo = time.perf_counter() - inicio    
        tiempoExpirado += 1
        print(f"URL: {url} - TIMEOUT - Tiempo: {tiempo:.2f}s")
    except requests.RequestException:
        tiempo = time.perf_counter() - inicio
        ErrorConexion += 1
        print(f"URL: {url} - ERROR DE CONEXIÓN - Tiempo: {tiempo:.2f}s")

inicio_total = time.perf_counter()
for url in urls:
    tiempo_secuencial = time.perf_counter() - inicio_total
    comprobar_web(url)

print("\n===============================")
print("       RESUMEN SECUENCIAL")
print("===============================")
print(f"WEB Online: {Online}")
print(f"ERROR http: {ErrorHttp}")
print(f"Tiempo Expirado: {tiempoExpirado}")
print(f"Error Conexion: {ErrorConexion}")
print(f"Tiempo total secuencial: {tiempo_secuencial:.2f} s")