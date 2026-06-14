import requests
from bs4 import BeautifulSoup
import re

# La página de SpinOff que usaremos SOLO para robar el token diario
PAGINA_MADRE = "https://spinoff.link"

# DICCIONARIO DIRECTO: El script creará estos canales basándose en los códigos de TecnoTV
# Si necesitas cambiar un nombre, hazlo aquí respetando las comillas
CANALES_A_GENERAR = {
    "De Pelicula": "a001",
    "Cinecanal": "a002",
    "Cinemax": "a003",
    "HBO HD": "a004",
    "HBO 2": "a005",
    "HBO Family": "a006",
    "HBO Plus": "a007",
    "HBO XTREME SD": "a008",
    "HBO POP HD": "a009",
    "HBO Signature": "a010",
    "HBO+": "a011",
    "ESPN HD": "a012",
    "ESPN 2 HD": "a013",
    "ESPN 3": "a014",
    "ESPN 4 HD": "a015",
    "ESPN 5 HD": "a016",
    "ESPN 6 HD": "a017",
    "ESPN 7HD": "a018",
    "ESPN PREMIUM HD": "a020",
    "Warner Channel": "a021",
    "WARNER HD": "a022",
    "Discovery Channel": "a023",
    "Discovery Turbo": "a025",
    "Discovery Kids": "a026",
    "Disney Channel": "a030",
    "Disney Jr": "a031",
    "AXN": "a033",
    "FX": "a035",
    "Space": "a036",
    "TNT": "a038",
    "TNT Series HD": "a040",
    "TNT Novelas": "a041",
    "TNT Sports Premium HD": "a042",
    "Universal": "a043",
    "STAR CHANNEL": "a051",
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
                        print(f"[ÉXITO] Token dinámico del día localizado: {token}")
                        return token
    except Exception:
        pass
    return "wbh2" # Token de respaldo si la web se satura

def filtrar_lista():
    # 1. El robot entra a SpinOff a robar el token activo del día (ej: wbh2)
    token_actual = obtener_carpeta_actual()
    
    nueva_lista = ["#EXTM3U"]
    
    # 2. Generación matemática directa sin descargar nada de TecnoTV (Evita bloqueos de red)
    for nombre, codigo in CANALES_A_GENERAR.items():
        # Creamos la etiqueta de la transmisión
        tag = f'#EXTINF:-1 tvg-name="{nombre}" group-title="Mis Canales", {nombre}'
        
        # Construimos el enlace inyectándole el token dinámico y tu truco final de m3u8
        enlace = f"https://tecnotv.club/{token_actual}/phpcode/android3.php?c={codigo}&token=tecnotokenplustv230516F&f=.m3u8"
        
        nueva_lista.append(tag)
        nueva_lista.append(enlace)
        
    # Guardamos el archivo final M3U
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
        
    print(f"[OK] ¡Lista indestructible generada con {len(CANALES_A_GENERAR)} canales!")

if __name__ == "__main__":
    filtrar_lista()
