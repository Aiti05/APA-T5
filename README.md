# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Aitana Ortega Sánchez

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.
<img width="548" height="606" alt="image" src="https://github.com/user-attachments/assets/549e46d0-47c5-4814-a1d3-18f49f4015d5" />
<img width="206" height="191" alt="image" src="https://github.com/user-attachments/assets/08cabcc5-7332-4934-b3ef-e2344d29a5de" />


#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`
```
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
```
##### Código de `mono2estereo()`
```
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
```
##### Código de `codEstereo()`
```
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
```
##### Código de `decEstereo()`
```
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
```
#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
