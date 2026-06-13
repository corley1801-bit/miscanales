import requests
from bs4 import BeautifulSoup
import re

# La página web principal que contiene los botones dinámicos
PAGINA_MADRE = "https://spinoff.link/listas-iptv-actualizadas-2025/"

# Tus canales favoritos con nombres exactos (Modifícalos con comillas y comas)
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

def extraer_urls_dinamicas():
    urls_encontradas = []
    cabeceras = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        # Entrar a la página web de SpinOff para leer sus botones
        respuesta = requests.get(PAGINA_MADRE, headers=cabeceras, timeout=15)
        if respuesta.status_code != 200:
            print("Error: No se pudo acceder a la página web principal.")
            return urls_encontradas
            
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Buscar todos los enlaces de la página que apunten a un archivo .m3u
        for enlace in soup.find_all('a', href=True):
            href = enlace['href']
            if ".m3u" in href and href not in urls_encontradas:
                urls_encontradas.append(href)
                
        print(f"¡Éxito! Se detectaron {len(urls_encontradas)} URLs de listas M3U activas en la web.")
    except Exception as e:
        print(f"Fallo al rastrear la web: {e}")
        
    return urls_encontradas

def filtrar_lista():
    # 1. Obtener de forma automática las URLs vigentes de la página
    urls_origen = extraer_urls_dinamicas()
    
    if not urls_origen:
        print("No se encontraron enlaces M3U para procesar.")
        return

    nueva_lista = ["#EXTM3U"] 
    enlaces_agregados = set() 
    nombres_ya_guardados = set() 
    cabeceras = {"User-Agent": "Mozilla/5.0"}
    
    # 2. Recorrer las listas descargadas automáticamente
    for url in urls_origen:
        try:
            respuesta = requests.get(url, headers=cabeceras, timeout=10)
            if respuesta.status_code != 200:
                continue
                
            lineas = respuesta.text.split("\n")
            
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    match = re.search(r",([^,]+)$", lineas[i])
                    if match:
                        nombre_en_lista = match.group(1).strip().lower()
                        
                        if any(canal.strip().lower() == nombre_en_lista for canal in MIS_CANALES_FAVORITOS):
                            if i + 1 < len(lineas):
                                enlace = lineas[i + 1].strip()
                                
                                if enlace not in enlaces_agregados and nombre_en_lista not in nombres_ya_guardados:
                                    nueva_lista.append(lineas[i].strip())
                                    nueva_lista.append(enlace)
                                    enlaces_agregados.add(enlace)
                                    nombres_ya_guardados.add(nombre_en_lista)
        except Exception as e:
            pass

    # Sobrescribir tu archivo de lista personalizada en GitHub
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"¡Proceso terminado! Guardados {len(nombres_ya_guardados)} canales únicos sin repetidos.")

if __name__ == "__main__":
    filtrar_lista()
