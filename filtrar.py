import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link"

def obtener_carpeta_actual():
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=12)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            for enlace in soup.find_all('a', href=True):
                href = enlace['href']
                if "tecnotv.club" in href:
                    match = re.search(r"tecnotv\.club/([^/]+)/", href)
                    if match:
                        token = match.group(1)
                        print(f"[ÉXITO] Token del servidor localizado: {token}")
                        return token
    except Exception:
        pass
    return "wbh2" # Token de respaldo

def filtrar_lista():
    token_actual = obtener_carpeta_actual()
    
    # Las 3 fuentes completas que se unificarán
    ARCHIVOS_M3U = [
        "lista1.m3u",
        "android2.m3u",
        "android3.m3u"
    ]
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set()
    
    # Usamos el servidor puente para descargar las listas sin bloqueos de red
    for archivo in ARCHIVOS_M3U:
        url_original = f"https://tecnotv.club{token_actual}/{archivo}"
        url_puente = f"https://allorigins.win{url_original}"
        
        try:
            respuesta = requests.get(url_puente, timeout=15)
            if respuesta.status_code != 200:
                # Conexión directa de respaldo si el puente está saturado
                respuesta = requests.get(url_original, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if respuesta.status_code != 200:
                    continue
                
            lineas = respuesta.text.split("\n")
            print(f"[OK] Clonando lista completa: {archivo}")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    if i + 1 < len(lineas):
                        enlace_original = lineas[i + 1].strip()
                        
                        if enlace_original.startswith("http"):
                            # Reparamos el token de la carpeta interna por el del día
                            enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                            
                            # Candado anti-repetidos para no duplicar canales entre archivos
                            if enlace_corregido not in enlaces_agregados:
                                nueva_lista.append(lineas[i].strip())
                                nueva_lista.append(enlace_corregido)
                                enlaces_agregados.add(enlace_corregido)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    # Guardamos absolutamente todos los canales unificados
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[FIN] ¡Fusión completa! Se guardaron {len(enlaces_agregados)} canales totales actualizados.")

if __name__ == "__main__":
    filtrar_lista()
