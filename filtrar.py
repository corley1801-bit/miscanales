import requests
from bs4 import BeautifulSoup
import re

PAGINA_MADRE = "https://spinoff.link/listas-iptv-actualizadas-2025/"

# REGLA: Usa palabras clave en minúsculas y sin agregados (el script buscará coincidencias de forma flexible)
MIS_CANALES_FAVORITOS = [
"De Pelicula",
"AE Mundo",
"AXN",
"Animal Planet",
"CNN",
"CNN Español",
"Canal Claro", 
"Cinecanal", 
"Cinemax",
"Cine Claro",
"Claro Deportes", 
"Discovery Channel",
"Discovery Turbo", 
"Disney Channel", 
"Disney Jr", 
"ESPN", 
"ESPN 2 HD", 
"ESPN 3",
"ESPN 4 HD", 
"ESPN 5 HD", 
"ESPN 6 HD", 
"ESPN 7HD", 
"ESPN HD", 
"ESPN PREMIUM HD", 
"Enlace", 
"Esne TV", 
"FOX NEWS CHANEL",
"FX",
"HBO", 
"HBO 2", 
"HBO Family", 
"HBO Plus", 
"HBO XTREME SD",
"History Channel",
"HomeandHealth",
"LA KALLE",
"DE POR VIDA",
"LIFETIME",
"MTV",
"National Geographic",
"HBO+",
"Nick Jr", 
"Nickelodeon", 
"STAR CHANNEL", 
"Sin Límites", 
"Sony",
"Espacio", 
"Space",
"Studio Universal",
"TCM", 
"TNT",
"TNT Sports Premium HD",
"Telemundo", 
"Tigo Sports HD", 
"USA",
"Universal", 
"Warner", 
"zz alquiler 8", 
"TV PREMIUM AZTECA 7",
"TV PREMIUM CANAL 5",
"Cartoon Network",
"DISTRITO COMEDIA", 
"FOX SPORT 2",
"TV PREMIUM LAS ESTRELLAS",
"TV PREMIUM LAS ESTRELLAS LEGAL",
"SKY SPORTS", 
"TELEMUNDO MIAMI",
"TL NOVELAS", 
"TUDN",
"Boomerang", 
"Discovery Kids", 
"Disney JR",
"Tooncast",
"Adult Swim", 
"Canal de conciertos",
"Exa TV", 
"Golf Channel HD", 
"Pasiones HD", 
"Univision HD", 
"AZ click HD", 
"Azcorazon", 
"Azmundo", 
"DISCOVERY THEATHER HD",
"Discovery Channel HD",
"Discovery ID HD", 
"Discovery World HD", 
"El Gourmet", 
"Historia 2",
"SONY HD", 
"SONY MOVIES HD", 
"STAR CHANNEL HD", 
"STAR LIFE", 
"Sun Channel",
"TNT 2",  
"TNT Novelas", 
"TNT Series HD", 
"UNIVERSAL CINEMA HD", 
"UNIVERSAL COMEDY HD", 
"UNIVERSAL CRIME HD",
"UNIVERSAL PREMIERE",
"UNIVERSAL PREMIERE O HD",
"UNIVERSAL REALITY HD",
"AMC HD", 
"TV PREMIUM AXN",
"Cine Latino", 
"TV PREMIUM CineMax", 
"DHE HD", 
"E! Entertainment HD", 
"Film & arts HD", 
"Golden", 
"Home & Health HD", 
"LIFETIME", 
"Multipremier", 
"Nat Geo HD", 
"SPACE HD", 
"TCM", 
"TLC",
"TV PREMIUM Universal",
"WARNER HD",
"Azteca UNO",
"Edge", 
"HBO POP HD",
"HBO Signature", 
"Playboy HD", 
"Venus", 
"GOLDEN PREMIER",
"IMAGEN",
"Az Cinema", 
"Az Corazón", 
"ADN 40"
]

def obtener_carpeta_actual():
    # Cabeceras completas imitando a Google Chrome desde una computadora
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
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
    except Exception as e:
        print(f"[ALERTA] Error al rastrear la web: {e}")
    print("[AVISO] Usando token de respaldo por defecto")
    return "wbh2" # Token de respaldo si la web está caída

def filtrar_lista():
    token_actual = obtener_carpeta_actual()
    
    # Tus 3 listas preferidas exclusivas
    ARCHIVOS_M3U = [
        "lista1.m3u",
        "android2.m3u",
        "android3.m3u"
    ]
    
    nueva_lista = ["#EXTM3U"] # Cabecera obligatoria
    enlaces_agregados = set()
    cabeceras_stream = {"User-Agent": "Mozilla/5.0"}
    
    for archivo in ARCHIVOS_M3U:
        url_m3u = f"https://tecnotv.club/{token_actual}/{archivo}"
        try:
            respuesta = requests.get(url_m3u, headers=cabeceras_stream, timeout=10)
            if respuesta.status_code != 200:
                continue
                
            lineas = respuesta.text.split("\n")
            print(f"Leyendo archivo: {archivo}")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    # Filtramos de forma flexible: si la palabra clave está en el nombre del canal, entra
                    if any(canal in lineas[i].lower() for canal in MIS_CANALES_FAVORITOS):
                        if i + 1 < len(lineas):
                            enlace_original = lineas[i + 1].strip()
                            
                            # Forzamos la actualización de la carpeta interna del enlace con el nuevo token
                            enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                            
                            if enlace_corregido not in enlaces_agregados:
                                nueva_lista.append(lineas[i].strip())
                                nueva_lista.append(enlace_corregido)
                                enlaces_agregados.add(enlace_corregido)
        except Exception:
            pass

    # Guardamos los resultados
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"[OK] Lista generada con {len(enlaces_agregados)} canales.")

if __name__ == "__main__":
    filtrar_lista()

