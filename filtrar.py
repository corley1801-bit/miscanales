import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link"

# REGLA: Todas tus palabras clave en MINÚSCULAS. El script jalará el canal donde sea que se mueva hoy.
MIS_CANALES_FAVORITOS = [
    "de pelicula", "ae mundo", "axn", "animal planet", "cnn", "cnn español", 
    "canal claro", "cinecanal", "cinemax", "cine claro", "claro deportes", 
    "discovery channel", "discovery turbo", "disney channel", "disney jr", 
    "espn", "espn 2 hd", "espn 3", "espn 4 hd", "espn 5 hd", "espn 6 hd", 
    "espn 7hd", "espn hd", "espn premium hd", "enlace", "esne tv", "fox news chanel", 
    "fx", "hbo", "hbo 2", "hbo family", "hbo plus", "hbo xtreme sd", "history channel", 
    "homeandhealth", "la kalle", "de por vida", "lifetime", "mtv", "national geographic", 
    "hbo+", "nick jr", "nickelodeon", "star channel", "sin límites", "sony", "espacio", 
    "space", "studio universal", "tcm", "tnt", "tnt sports premium hd", "telemundo", 
    "tigo sports hd", "usa", "universal", "warner", "zz alquiler 8", "tv premium azteca 7", 
    "tv premium canal 5", "cartoon network", "distrito comedia", "fox sport 2", 
    "tv premium las estrellas", "tv premium las estrellas legal", "sky sports", 
    "telemundo miami", "tl novelas", "tudn", "boomerang", "discovery kids", "tooncast", 
    "adult swim", "canal de conciertos", "exa tv", "golf channel hd", "pasiones hd", 
    "univision hd", "az click hd", "azcorazon", "az corazón", "azmundo", "discovery theather hd", 
    "discovery channel hd", "discovery id hd", "discovery world hd", "el gourmet", 
    "historia 2", "sony hd", "sony movies hd", "star channel hd", "star life", "sun channel", 
    "tnt 2", "tnt novelas", "tnt series hd", "universal cinema hd", "universal comedy hd", 
    "universal crime hd", "universal premiere", "universal premiere o hd", "universal reality hd", 
    "amc hd", "tv premium axn", "cine latino", "tv premium cinemax", "dhe hd", 
    "e! entertainment hd", "film & arts hd", "golden", "home & health hd", "multipremier", 
    "nat geo hd", "space hd", "tlc", "tv premium universal", "warner hd", "azteca uno", 
    "edge", "hbo pop hd", "hbo signature", "playboy hd", "venus", "golden premier", 
    "imagen", "az cinema", "az corazón", "adn 40"
]

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
                        print(f"[ÉXITO] Servidor activo localizado en la ruta: {token}")
                        return token
    except Exception:
        pass
    return "wbh2"

def filtrar_lista():
    token_actual = obtener_carpeta_actual()
    
    # El robot buscará simultáneamente en las 3 listas oficiales de TecnoTV
    ARCHIVOS_M3U = [
        "lista1.m3u",
        "android2.m3u",
        "android3.m3u"
    ]
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set()
    
    # Cabeceras de simulación de dispositivo móvil para saltar cualquier bloqueo directo de Cloudflare
    cabeceras_tv = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Chromecast) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36"
    }
    
    for archivo in ARCHIVOS_M3U:
        url_m3u = f"https://tecnotv.club/{token_actual}/{archivo}"
        try:
            respuesta = requests.get(url_m3u, headers=cabeceras_tv, timeout=12)
            if respuesta.status_code != 200:
                continue
                
            lineas = respuesta.text.split("\n")
            print(f"[INFO] Escaneando canales en la ruta del archivo: {archivo}")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    linea_tecnica_minusculas = lineas[i].lower()
                    
                    # Comprobación de texto flexible en minúsculas
                    if any(favorito in linea_tecnica_minusculas for favorito in MIS_CANALES_FAVORITOS):
                        if i + 1 < len(lineas):
                            enlace_original = lineas[i + 1].strip()
                            
                            if enlace_original.startswith("http"):
                                # El script extrae el enlace completo real con su token largo original vigente
                                enlace_corregido = enlace_original
                                
                                # Aplicamos tu modificación para forzar la reproducción multimedia en tu app
                                if not enlace_corregido.endswith("&f=.m3u8"):
                                    enlace_corregido = enlace_corregido + "&f=.m3u8"
                                
                                if enlace_corregido not in enlaces_agregados:
                                    nueva_lista.append(lineas[i].strip())
                                    nueva_lista.append(enlace_corregido)
                                    enlaces_agregados.add(enlace_corregido)
        except Exception:
            pass

    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[FIN] ¡Proceso concluido! Tu lista ha guardado {len(enlaces_agregados)} canales reales actualizados.")

if __name__ == "__main__":
    filtrar_lista()
