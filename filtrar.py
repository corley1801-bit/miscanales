import requests
from bs4 import BeautifulSoup
import re

# La web de SpinOff (esta página no tiene bloqueos para el robot de GitHub)
PAGINA_MADRE = "https://spinoff.link"

# REGLA: Mantén tus palabras clave favoritas en minúsculas.
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

def obtener_datos_web():
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=15)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            
            # Buscaremos la URL del archivo de canales que SpinOff publica en su código HTML
            for enlace in soup.find_all('a', href=True):
                href = enlace['href']
                if "tecnotv.club" in href and ".m3u" in href:
                    # Extraemos el token/carpeta actual (ej: wbh2)
                    match_token = re.search(r"tecnotv\.club/([^/]+)/", href)
                    if match_token:
                        token = match_token.group(1)
                        print(f"[EXITO] Token dinámico de red detectado: {token}")
                        return token, href
    except Exception as e:
        print(f"Error al leer la web principal: {e}")
    return "wbh2", "https://tecnotv.club"

def filtrar_lista():
    # 1. El script lee la web de SpinOff y descarga el archivo usando el enlace puente permitido
    token_actual, url_lista_oficial = obtener_datos_web()
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set()
    cabeceras_descarga = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    
    try:
        respuesta = requests.get(url_lista_oficial, headers=cabeceras_descarga, timeout=15)
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    linea_tecnica_minusculas = lineas[i].lower()
                    
                    # Filtramos de forma segura usando tus palabras favoritas en minúsculas
                    if any(favorito in linea_tecnica_minusculas for favorito in MIS_CANALES_FAVORITOS):
                        if i + 1 < len(lineas):
                            enlace_original = lineas[i + 1].strip()
                            
                            if enlace_original.startswith("http"):
                                # Parcheamos cualquier rastro de token viejo por la carpeta activa de hoy
                                enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                                
                                # Aplicamos tu truco final multimedia para evitar errores de reproducción
                                if not enlace_corregido.endswith("&f=.m3u8"):
                                    enlace_corregido = enlace_corregido + "&f=.m3u8"
                                
                                if len(enlace_corregido) > 10 and enlace_corregido not in enlaces_agregados:
                                    nueva_lista.append(lineas[i].strip()) # Guarda el nombre original con mayúsculas
                                    nueva_lista.append(enlace_corregido)
                                    enlaces_agregados.add(enlace_corregido)
    except Exception as e:
        print(f"Error en el proceso de clonación: {e}")

    # Guardamos los resultados en tu repositorio público
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[OK] ¡Lista reparada de forma exitosa con {len(enlaces_agregados)} canales con extensión m3u8!")

if __name__ == "__main__":
    filtrar_lista()
