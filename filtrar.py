import requests

# 1. Agrega aquí tus 3 URLs de origen (puedes poner las que quieras)
URLS_ORIGEN = [
    "https://tecnotv.club/xm4p/android2.m3u",
    "https://tecnotv.club/xm4p/android3.m3u",
]

# 2. Escribe aquí tus canales favoritos (Modifícalos a tu gusto, respetando las comillas y comas)
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
"ADN 40",
]

def filtrar_lista():
    nueva_lista = ["#EXTM3U"] # Cabecera obligatoria
    canales_agregados = set() # Evita canales repetidos si están en más de una lista
    
    # Revisar cada una de las URLs
    for url in URLS_ORIGEN:
        try:
            respuesta = requests.get(url, timeout=10)
            if respuesta.status_code != 200:
                print(f"Error al descargar la lista: {url}")
                continue
                
            lineas = respuesta.text.split("\n")
            
            # Recorrer el archivo buscando tus canales
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    # Comprobar si coincide con tus favoritos
                    if any(canal.lower() in lineas[i].lower() for canal in MIS_CANALES_FAVORITOS):
                        # Extraer el enlace del canal (la línea siguiente)
                        if i + 1 < len(lineas):
                            enlace = lineas[i + 1].strip()
                            # Si el enlace no lo hemos guardado antes, lo añade
                            if enlace not in canales_agregados:
                                nueva_lista.append(lineas[i].strip())
                                nueva_lista.append(enlace)
                                canales_agregados.add(enlace)
        except Exception as e:
            print(f"Fallo en la conexión con {url}: {e}")

    # Guardar el archivo final unificado
    with open("mi_lista_personalizada.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))
    print(f"¡Lista actualizada con {len(canales_agregados)} canales con tokens nuevos!")

if __name__ == "__main__":
    filtrar_lista()
