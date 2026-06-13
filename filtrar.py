import requests
from bs4 import BeautifulSoup
import re

# Página que publica las actualizaciones diarias
PAGINA_MADRE = "https://spinoff.link/listas-iptv-actualizadas-2025/"

# REGLA DE ORO: Escribe aquí tus canales (Usa las abreviaturas cortas que te funcionaban antes)
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
    """Entra a SpinOff y extrae el token/carpeta activa (ej: wbh2 o xm4p)"""
    cabeceras = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=15)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            for enlace in soup.find_all('a', href=True):
                href = enlace['href']
                # Buscamos patrones como /wbh2/ o /xm4p/ dentro de los links tecnotv
                if "tecnotv.club" in href and ".m3u" in href:
                    match = re.search(r"tecnotv\.club/([^/]+)/", href)
                    if match:
                        carpeta = match.group(1)
                        print(f"¡Carpeta y Token actual detectado con éxito!: {carpeta}")
                        return carpeta
    except Exception as e:
        print(f"Error al buscar la carpeta del servidor: {e}")
    return "wbh2" # Valor de respaldo si falla el escaneo

def filtrar_lista():
    # 1. Detectar dinámicamente si el token cambió (ej: wbh2)
    token_actual = obtener_carpeta_actual()
    
    # 2. Descargamos una lista limpia base (usamos una URL que siempre responde)
    # Reconstruimos la dirección web usando el token fresco del día
    url_m3u_fresca = f"https://tecnotv.club/{token_actual}/android3.m3u"
    
    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set() 
    cabeceras = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        respuesta = requests.get(url_m3u_fresca, headers=cabeceras, timeout=15)
        if respuesta.status_code != 200:
            print("El servidor de canales no respondió temporalmente.")
            return
            
        lineas = respuesta.text.split("\n")
        
        for i in range(len(lineas)):
            if lineas[i].startswith("#EXTINF"):
                # Filtro por palabra clave corta (ej: "ESPN")
                if any(canal.lower() in lineas[i].lower() for canal in MIS_CANALES_FAVORITOS):
                    if i + 1 < len(lineas):
                        enlace_original = lineas[i + 1].strip()
                        
                        # PARCHE INTELIGENTE: Si el enlace interno tiene una carpeta vieja,
                        # el script reescribe el token viejo por el nuevo (ej: cambia xm4p por wbh2)
                        enlace_corregido = re.sub(r"tecnotv\.club/[^/]+/", f"tecnotv.club/{token_actual}/", enlace_original)
                        
                        if enlace_corregido not in enlaces_agregados:
                            nueva_lista.append(lineas[i].strip())
                            nueva_lista.append(enlace_corregido)
                            enlaces_agregados.add(enlace_corregido)
    except Exception as e:
        print(f"Error al procesar canales: {e}")

    # Sobrescribir tu archivo final en GitHub
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print("¡Tu lista de canales ha sido reparada y actualizada con los nuevos tokens!")

if __name__ == "__main__":
    filtrar_lista()
