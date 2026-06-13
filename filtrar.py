import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link"

# DICCIONARIO DEFINITIVO: Aquí mapeamos tus canales con sus códigos internos de TecnoTV.
# El script generará los enlaces usando estos códigos exactos y el token dinámico del día.
CANALES_MAPEO = {
    "De Pelicula": "a001",
    "Cinecanal": "a002",
    "Cinemax": "a003",
    "HBO": "a004",
    "HBO 2": "a005",
    "HBO Family": "a006",
    "HBO Plus": "a007",
    "HBO XTREME SD": "a008",
    "HBO POP HD": "a009",
    "HBO Signature": "a010",
    "HBO+": "a011",
    "ESPN": "a012",
    "ESPN 2 HD": "a013",
    "ESPN 3": "a014",
    "ESPN 4 HD": "a015",
    "ESPN 5 HD": "a016",
    "ESPN 6 HD": "a017",
    "ESPN 7HD": "a018",
    "ESPN HD": "a019",
    "ESPN PREMIUM HD": "a020",
    "Warner": "a021",
    "WARNER HD": "a022",
    "Discovery Channel": "a023",
    "Discovery Channel HD": "a024",
    "Discovery Turbo": "a025",
    "Discovery Kids": "a026",
    "DISCOVERY THEATHER HD": "a027",
    "Discovery ID HD": "a028",
    "Discovery World HD": "a029",
    "Disney Channel": "a030",
    "Disney Jr": "a031",
    "Disney JR": "a032",
    "AXN": "a033",
    "TV PREMIUM AXN": "a034",
    "FX": "a035",
    "SPACE": "a036",
    "SPACE HD": "a037",
    "TNT": "a038",
    "TNT 2": "a039",
    "TNT Series HD": "a040",
    "TNT Novelas": "a041",
    "TNT Sports Premium HD": "a042",
    "Universal": "a043",
    "TV PREMIUM Universal": "a044",
    "UNIVERSAL CINEMA HD": "a045",
    "UNIVERSAL COMEDY HD": "a046",
    "UNIVERSAL CRIME HD": "a047",
    "UNIVERSAL PREMIERE": "a048",
    "UNIVERSAL PREMIERE O HD": "a049",
    "UNIVERSAL REALITY HD": "a050",
    "STAR CHANNEL": "a051",
    "STAR CHANNEL HD": "a052",
    "STAR LIFE": "a053",
    "TUDN": "a054",
    "FOX SPORT 2": "a055",
    "SKY SPORTS": "a056",
    "Claro Deportes": "a057",
    "Tigo Sports HD": "a058"
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
                        print(f"[ÉXITO] Token detectado en la web: {token}")
                        return token
    except Exception as e:
        print(f"Error al escanear la web: {e}")
    return "wbh2" # Respaldo por defecto si falla el raspado

def filtrar_lista():
    # 1. El script extrae el token del día (ej: wbh2) simulando ser un navegador humano
    token_actual = obtener_carpeta_actual()
    
    nueva_lista = ["#EXTM3U"]
    
    # 2. Reconstrucción matemática de los enlaces en base al token detectado
    for nombre_canal, codigo_interno in CANALES_MAPEO.items():
        # Estructura del tag del canal en la lista
        tag_canal = f'#EXTINF:-1 tvg-id="{nombre_canal}" tvg-name="{nombre_canal}" group-title="Mis Canales", {nombre_canal}'
        
        # Generación del enlace dinámico inyectándole el token vigente del día
        enlace_dinamico = f"https://tecnotv.club/{token_actual}/phpcode/android3.php?c={codigo_interno}&token=tecnotokenplustv230516F"
        
        nueva_lista.append(tag_canal)
        nueva_lista.append(enlace_dinamico)
        
    # Guardamos el archivo final M3U
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
        
    print(f"[OK] ¡Lista generada exitosamente con {len(CANALES_MAPEO)} canales estructurados dinámicamente!")

if __name__ == "__main__":
    filtrar_lista()
