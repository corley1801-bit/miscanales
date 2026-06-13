import requests
from bs4 import BeautifulSoup
import re

# Página que publica las actualizaciones diarias de TecnoTV
PAGINA_MADRE = "https://spinoff.link"

# Escribe aquí tus canales favoritos usando abreviaturas cortas
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
    """Escanea la página web para ver si el token cambió hoy"""
    cabeceras = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=10)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            for enlace in soup.find_all('a', href=True):
                href = enlace['href']
                if "tecnotv.club" in href and ".m3u" in href:
                    match = re.search(r"tecnotv\.club/([^/]+)/", href)
                    if match:
                        return match.group(1)
    except Exception:
        pass
    return "wbh2" # Si falla el escaneo, usa wbh2 por defecto

def filtrar_lista():
    token_actual = obtener_carpeta_actual()
    print(f"Token dinámico del día: {token_actual}")
    
    # TUS 3 FUENTES EXCLUSIVAS SELECCIONADAS
    # El script cambiará 'wbh2' automáticamente por el nuevo token cuando sea necesario
    ARCHIVOS_M3U = [
        "lista1.m3u",
        "android2.m3u",
        "android3.m3u"
    ]
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set() 
    cabeceras = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    
    for archivo in ARCHIVOS_M3U:
        url_m3u = f"https://tecnotv.club/{token_actual}/{archivo}"
        try:
            respuesta = requests.get(url_m3u, headers=cabeceras, timeout=8)
            if respuesta.status_code != 200:
                print(f"No se pudo leer el archivo: {archivo}")
                continue
                
            lineas = respuesta.text.split("\n")
            print(f"Buscando canales en: {archivo}...")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    if any(canal.lower() in lineas[i].lower() for canal in MIS_CANALES_FAVORITOS):
                        if i + 1 < len(lineas):
                            enlace_original = lineas[i + 1].strip()
                            
                            # Corrección de token en tiempo real
                            enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                            
                            if enlace_corregido not in enlaces_agregados:
                                nueva_lista.append(lineas[i].strip())
                                nueva_lista.append(enlace_corregido)
                                enlaces_agregados.add(enlace_corregido)
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")

    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"¡Éxito total! Lista generada con {len(enlaces_agregados)} canales de tus 3 fuentes.")

if __name__ == "__main__":
    filtrar_lista()
