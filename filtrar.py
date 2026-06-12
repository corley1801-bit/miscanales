import requests

# 1. Agrega aquí tus 3 URLs de origen (puedes poner las que quieras)
URLS_ORIGEN = [
    "https://tecnotv.club",
    "https://tecnotv.club", # Reemplaza esta por tu segunda URL si la tienes
    "https://tecnotv.club"  # Reemplaza esta por tu tercera URL si la tienes
]

# 2. Escribe aquí tus canales favoritos (Modifícalos a tu gusto, respetando las comillas y comas)
MIS_CANALES_FAVORITOS = [
    "HBO", 
    "FOX Sports", 
    "Warner Channel", 
    "Discovery Channel"
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
