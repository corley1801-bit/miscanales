import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link/listas-iptv-actualizadas-2025/"

# REGLA: Deja solo las palabras principales en MINÚSCULAS. 
# El script jalará cualquier canal que contenga esta palabra en su línea técnica.
MIS_CANALES_FAVORITOS = [
    "de pelicula", "ae mundo", "axn", "animal planet", "cnn", "canal claro", 
    "cinecanal", "cinemax", "cine claro", "claro deportes", "discovery channel", 
    "discovery turbo", "disney channel", "disney jr", "espn", "enlace", "esne tv", 
    "fox news", "fx", "hbo", "history channel", "homeandhealth", "home & health", 
    "la kalle", "de por vida", "lifetime", "mtv", "national geographic", "nat geo", 
    "nick jr", "nickelodeon", "star channel", "sin límites", "sony", "espacio", 
    "space", "studio universal", "tcm", "tnt", "telemundo", "tigo sports", "usa", 
    "universal", "warner", "zz alquiler", "azteca 7", "canal 5", "cartoon network", 
    "distrito comedia", "las estrellas", "sky sports", "tl novelas", "tudn", 
    "boomerang", "discovery kids", "tooncast", "adult swim", "conciertos", "exa tv", 
    "golf channel", "pasiones", "univision", "az click", "azcorazon", "az corazón", 
    "azmundo", "discovery theather", "discovery id", "discovery world", "el gourmet", 
    "historia 2", "star life", "sun channel", "amc", "cine latino", "dhe", 
    "e! entertainment", "film & arts", "golden", "multipremier", "tlc", "edge", 
    "playboy", "venus", "imagen", "az cinema", "adn 40"
]

def obtener_carpeta_actual():
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
                        print(f"[EXITO] Token detectado: {token}")
                        return token
    except Exception:
        pass
    return "wbh2"

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
    cabeceras_stream = {"User-Agent": "Mozilla/5.0"}
    
    for archivo in ARCHIVOS_M3U:
        url_m3u = f"https://tecnotv.club/{token_actual}/{archivo}"
        try:
            respuesta = requests.get(url_m3u, headers=cabeceras_stream, timeout=10)
            if respuesta.status_code != 200:
                continue
                
            lineas = respuesta.text.split("\n")
            print(f"Buscando en: {archivo}")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    # Pasamos toda la línea técnica a minúsculas para romper problemas de formato
                    linea_tecnica_minusculas = lineas[i].lower()
                    
                    # Verificamos de forma directa si tu palabra favorita está dentro de la línea
                    if any(favorito in linea_tecnica_minusculas for favorito in MIS_CANALES_FAVORITOS):
                        if i + 1 < len(lineas):
                            enlace_original = lineas[i + 1].strip()
                            
                            if enlace_original.startswith("http"):
                                # Corregimos el token de la carpeta interna
                                enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                                
                                # Aplicamos tu gran truco del formato m3u8 al final
                                if not enlace_corregido.endswith("&f=.m3u8"):
                                    enlace_corregido = enlace_corregido + "&f=.m3u8"
                                
                                if enlace_corregido not in enlaces_agregados:
                                    nueva_lista.append(lineas[i].strip())
                                    nueva_lista.append(enlace_corregido)
                                    enlaces_agregados.add(enlace_corregido)
        except Exception as e:
            print(f"Error en {archivo}: {e}")

    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[OK] ¡Lista generada exitosamente con {len(enlaces_agregados)} canales!")

if __name__ == "__main__":
    filtrar_lista()
