import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link"

# DICCIONARIO CON LOS CÓDIGOS INTERNOS REALES DE TECNOTV
# El script generará los enlaces de tus canales usando estos parámetros
CANALES_A_GENERAR = {
    "De Pelicula": "de_pelicula",
    "Cinecanal": "cinecanal",
    "Cinemax": "cinemax",
    "HBO HD": "hbo_hd",
    "HBO 2": "hbo_2",
    "HBO Family": "hbo_family",
    "HBO Plus": "hbo_plus",
    "HBO XTREME SD": "hbo_xtreme",
    "HBO POP HD": "hbo_pop",
    "HBO Signature": "hbo_signature",
    "ESPN HD": "espn_hd",
    "ESPN 2 HD": "espn_2_hd",
    "ESPN 3": "espn_3",
    "ESPN 4 HD": "espn_4_hd",
    "ESPN 5 HD": "espn_5_hd",
    "ESPN 6 HD": "espn_6_hd",
    "ESPN 7HD": "espn_7_hd",
    "ESPN PREMIUM HD": "espn_premium",
    "Warner Channel": "warner",
    "Discovery Channel": "discovery_channel",
    "Discovery Turbo": "discovery_turbo",
    "Discovery Kids": "discovery_kids",
    "Disney Channel": "disney_channel",
    "Disney Jr": "disney_jr",
    "AXN": "axn",
    "FX": "fx",
    "Space": "space",
    "TNT": "tnt",
    "TNT Series HD": "tnt_series",
    "TNT Novelas": "tnt_novelas",
    "TNT Sports Premium HD": "tnt_sports",
    "Universal": "universal_tv",
    "STAR CHANNEL": "star_channel",
    "TUDN": "tudn",
    "FOX SPORT 2": "fox_sports_2",
    "SKY SPORTS": "sky_sports",
    "Claro Deportes": "claro_deportes",
    "Tigo Sports HD": "tigo_sports"
}

def obtener_carpeta_actual():
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=10)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            for enlace in soup.find_all('a', href=True):
                href = enlace['href']
                if "tecnotv.club" in href:
                    match = re.search(r"tecnotv\.club/([^/]+)/", href)
                    if match:
                        token = match.group(1)
                        print(f"[ÉXITO] Token localizado: {token}")
                        return token
    except Exception:
        pass
    return "wbh2" # Respaldo

def filtrar_lista():
    # 1. Obtenemos el token dinámico sin tocar el servidor de TecnoTV
    token_actual = obtener_carpeta_actual()
    
    nueva_lista = ["#EXTM3U"]
    
    # 2. Construcción matemática de la lista con la extensión requerida por tu reproductor
    for nombre, codigo in CANALES_A_GENERAR.items():
        tag = f'#EXTINF:-1 tvg-name="{nombre}" group-title="Mis Canales", {nombre}'
        
        # Enlace dinámico con parche de token automático y tu truco multimedia al final
        enlace = f"https://tecnotv.club/{token_actual}/phpcode/android3.php?c={codigo}&token=tecnotokenplustv230516F&f=.m3u8"
        
        nueva_lista.append(tag)
        nueva_lista.append(enlace)
        
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
        
    print(f"[OK] ¡Lista unificada generada de forma local con {len(CANALES_A_GENERAR)} canales!")

if __name__ == "__main__":
    filtrar_lista()
