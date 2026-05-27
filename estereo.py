import struct

def leer_cabecera_wave(archivo):
    """
    Lee y valida la cabecera de un archivo WAVE.
    Soporta la lectura secuencial de sub-chunks ignorando los no deseados.
    Retorna un diccionario con las propiedades del formato de audio.
    """
    riff_hdr = archivo.read(12)
    if len(riff_hdr) < 12:
        raise ValueError("Cabecera del archivo incompleta o corrupta.")
        
    id_riff, tamano_riff, id_wave = struct.unpack('<4sI4s', riff_hdr)
    if id_riff != b'RIFF' or id_wave != b'WAVE':
        raise ValueError("El archivo no posee una firma válida de RIFF/WAVE.")
        
    formato_encontrado = None
    datos_encontrados = None
    
    while True:
        cabecera_chunk = archivo.read(8)
        if len(cabecera_chunk) < 8:
            break
            
        id_chunk, tamano_chunk = struct.unpack('<4sI', cabecera_chunk)
        
        if id_chunk == b'fmt ':
            datos_fmt = archivo.read(tamano_chunk)
            if len(datos_fmt) < 16:
                raise ValueError("Sección de formato 'fmt ' truncada.")
            formato_encontrado = struct.unpack('<HHIIHH', datos_fmt[:16])
        elif id_chunk == b'data':
            datos_encontrados = tamano_chunk
            break
        else:
            # Saltamos bloques adicionales (ej. metadatos, JUNK o etiquetas)
            archivo.seek(tamano_chunk, 1)
            
    if not formato_encontrado:
        raise ValueError("No se encontró el bloque de formato 'fmt '.")
    if datos_encontrados is None:
        raise ValueError("No se encontró el bloque de muestras 'data '.")
        
    formato_audio, canales, fs, tasa_bytes, alineacion, bits_muestra = formato_encontrado
    
    return {
        'formato': formato_audio,
        'canales': canales,
        'frecuencia': fs,
        'bits_muestra': bits_muestra,
        'tamano_datos': datos_encontrados
    }


def escribir_cabecera_wave(archivo, canales, frecuencia, bits_muestra, tamano_datos):
    """
    Genera y escribe una cabecera RIFF-WAVE estándar para codificación PCM lineal.
    """
    bytes_muestra = bits_muestra // 8
    alineacion = canales * bytes_muestra
    tasa_bytes = frecuencia * alineacion
    tamano_fmt = 16
    tamano_riff = 36 + tamano_datos
    
    archivo.write(struct.pack('<4sI4s', b'RIFF', tamano_riff, b'WAVE'))
    archivo.write(struct.pack('<4sI', b'fmt ', tamano_fmt))
    archivo.write(struct.pack('<HHIIHH', 1, canales, frecuencia, tasa_bytes, alineacion, bits_muestra))
    archivo.write(struct.pack('<4sI', b'data', tamano_datos))


def estereo2mono(ficEste, ficMono, canal=2):
    """
    Lee un fichero de audio estéreo (16 bits) y genera un fichero monofónico.
    
    Parámetros de canal:
        0: Canal izquierdo (L)
        1: Canal derecho (R)
        2: Semisuma (L + R) // 2
        3: Semidiferencia (L - R) // 2
    """
    if canal not in (0, 1, 2, 3):
        raise ValueError("El parámetro 'canal' debe ser un entero entre 0 y 3.")
        
    with open(ficEste, 'rb') as f_entrada:
        meta = leer_cabecera_wave(f_entrada)
        
        if meta['canales'] != 2:
            raise ValueError("El fichero de origen debe ser estéreo (2 canales).")
        if meta['bits_muestra'] != 16:
            raise ValueError("Solo se admiten ficheros estéreo con resolución de 16 bits.")
        if meta['formato'] != 1:
            raise ValueError("El formato de codificación debe ser PCM lineal.")
            
        datos_crudos = f_entrada.read(meta['tamano_datos'])
        
    total_muestras_estereo = len(datos_crudos) // 2
    muestras = struct.unpack(f'<{total_muestras_estereo}h', datos_crudos)
    
    izq = muestras[0::2]
    der = muestras[1::2]
    
    if canal == 0:
        muestras_mono = izq
    elif canal == 1:
        muestras_mono = der
    elif canal == 2:
        muestras_mono = [(l + r) // 2 for l, r in zip(izq, der)]
    else:  # canal == 3
        muestras_mono = [(l - r) // 2 for l, r in zip(izq, der)]
        
    num_muestras_final = len(muestras_mono)
    datos_salida = struct.pack(f'<{num_muestras_final}h', *muestras_mono)
    
    with open(ficMono, 'wb') as f_salida:
        escribir_cabecera_wave(f_salida, 1, meta['frecuencia'], 16, len(datos_salida))
        f_salida.write(datos_salida)


def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Fusiona dos ficheros monofónicos de 16 bits en un único fichero estéreo de 16 bits.
    """
    with open(ficIzq, 'rb') as f_izq:
        meta_i = leer_cabecera_wave(f_izq)
        if meta_i['canales'] != 1 or meta_i['bits_muestra'] != 16 or meta_i['formato'] != 1:
            raise ValueError("El archivo izquierdo debe ser mono, PCM, de 16 bits.")
        datos_izq = f_izq.read(meta_i['tamano_datos'])
        
    with open(ficDer, 'rb') as f_der:
        meta_d = leer_cabecera_wave(f_der)
        if meta_d['canales'] != 1 or meta_d['bits_muestra'] != 16 or meta_d['formato'] != 1:
            raise ValueError("El archivo derecho debe ser mono, PCM, de 16 bits.")
        datos_der = f_der.read(meta_d['tamano_datos'])
        
    if meta_i['frecuencia'] != meta_d['frecuencia']:
        raise ValueError("Las frecuencias de muestreo de ambos archivos no coinciden.")
        
    muestras_izq = struct.unpack(f'<{len(datos_izq) // 2}h', datos_izq)
    muestras_der = struct.unpack(f'<{len(datos_der) // 2}h', datos_der)
    
    min_muestras = min(len(muestras_izq), len(muestras_der))
    
    # Intercalación mediante comprensión plana unidimensional
    intercaladas = [
        muestra
        for i in range(min_muestras)
        for muestra in (muestras_izq[i], muestras_der[i])
    ]
    
    datos_salida = struct.pack(f'<{min_muestras * 2}h', *intercaladas)
    
    with open(ficEste, 'wb') as f_salida:
        escribir_cabecera_wave(f_salida, 2, meta_i['frecuencia'], 16, len(datos_salida))
        f_salida.write(datos_salida)


def codEstereo(ficEste, ficCod):
    """
    Codifica un fichero estéreo de 16 bits en un fichero de 32 bits (monofónico).
    Almacena la semisuma en la parte alta (MSB) y la semidiferencia en la baja (LSB).
    """
    with open(ficEste, 'rb') as f_entrada:
        meta = leer_cabecera_wave(f_entrada)
        if meta['canales'] != 2 or meta['bits_muestra'] != 16 or meta['formato'] != 1:
            raise ValueError("El archivo de entrada debe ser estéreo PCM de 16 bits.")
        datos_crudos = f_entrada.read(meta['tamano_datos'])
        
    muestras = struct.unpack(f'<{len(datos_crudos) // 2}h', datos_crudos)
    izq = muestras[0::2]
    der = muestras[1::2]
    
    datos_32 = [
        (((l + r) // 2) << 16) | (((l - r) // 2) & 0xFFFF)
        for l, r in zip(izq, der)
    ]
    
    datos_salida = struct.pack(f'<{len(datos_32)}i', *datos_32)
    
    with open(ficCod, 'wb') as f_salida:
        escribir_cabecera_wave(f_salida, 1, meta['frecuencia'], 32, len(datos_salida))
        f_salida.write(datos_salida)


def decEstereo(ficCod, ficEste):
    """
    Decodifica una señal de 32 bits para extraer y restaurar los dos canales de 16 bits.
    """
    with open(ficCod, 'rb') as f_entrada:
        meta = leer_cabecera_wave(f_entrada)
        if meta['canales'] != 1 or meta['bits_muestra'] != 32:
            raise ValueError("El archivo codificado debe ser monofónico de 32 bits.")
        datos_crudos = f_entrada.read(meta['tamano_datos'])
        
    num_muestras = len(datos_crudos) // 4
    muestras_32 = struct.unpack(f'<{num_muestras}i', datos_crudos)
    
    semisuma = [v >> 16 for v in muestras_32]
    semidif = [((v & 0xFFFF) ^ 0x8000) - 0x8000 for v in muestras_32]
    
    limitar = lambda x: max(-32768, min(32767, x))
    
    # Comprensión anidada para reconstruir, limitar e intercalar en un único paso
    intercalado = [
        limitar(val)
        for s, d in zip(semisuma, semidif)
        for val in (s + d, s - d)
    ]
    
    datos_salida = struct.pack(f'<{num_muestras * 2}h', *intercalado)
    
    with open(ficEste, 'wb') as f_salida:
        escribir_cabecera_wave(f_salida, 2, meta['frecuencia'], 16, len(datos_salida))
        f_salida.write(datos_salida)