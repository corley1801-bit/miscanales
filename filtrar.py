import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link/listas-iptv-actualizadas-2025/"

def obtener_carpeta_actual():
    # Fingimos ser un navegador para extraer el token activo del día en SpinOff
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
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
                        print(f"[EXITO] Token detectado en la web: {token}")
                        return token
    except Exception:
        pass
    return "wbh2" # Respaldo por defecto

def filtrar_lista():
    token_actual = obtener_carpeta_actual()
    
    # Tus 3 listas preferidas exclusivas
    ARCHIVOS_M3U = [
        "lista1.m3u",
        "android2.m3u",
        "android3.m3u"
    ]
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set()
    
    # User-Agent de televisión para saltar cualquier restricción del servidor de canales
    cabeceras_tv = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36 IPTV-Player"
    }
    
    for archivo in ARCHIVOS_M3U:
        url_m3u = f"https://tecnotv.club{token_actual}/{archivo}"
        try:
            respuesta = requests.get(url_m3u, headers=cabeceras_tv, timeout=12)
            if respuesta.status_code != 200:
                continue
                
            lineas = respuesta.text.split("\n")
            print(f"Clonando y reparando archivo: {archivo}")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    if i + 1 < len(lineas):
                        enlace_original = lineas[i + 1].strip()
                        
                        if enlace_original.startswith("http"):
                            # Parcheamos el enlace interno con el token del segundo exacto
                            enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                            
                            # Tu truco indispensable para que el reproductor no de error
                            if not enlace_corregido.endswith("&f=.m3u8"):
                                enlace_corregido = enlace_corregido + "&f=.m3u8"
                            
                            if enlace_corregido not in enlaces_agregados:
                                nueva_lista.append(lineas[i].strip())
                                nueva_lista.append(enlace_corregido)
                                enlaces_agregados.add(enlace_corregido)
        except Exception:
            pass

    # Guardamos todos los canales sin filtros restrictivos
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[FIN] ¡Lista unificada y reparada con {len(enlaces_agregados)} canales totales!")

if __name__ == "__main__":
    filtrar_lista()
