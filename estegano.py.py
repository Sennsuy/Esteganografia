# Utilizaremos el modulo Pillow, que no es mas que un fork del modulo PIL, es por ello que importamos PIL,
# pero a la hora de instalar el modulo tenemos que hacer pip install Pillow que es la version mas reciente de PIL
# Aparte, importamos el modulo math ya que vamos a tener que realizar un redondeo a la baja en una de las funciones.

from PIL import Image
import math

# Utilizamos una variable de nombre imagen que contiene la ruta y el nombre de nuestra imagen a utilizar
# la ruta en la que tiene que estar es la misma carpeta sobre la que nos encontramos

rutaImagenOriginal = "proyimag1T.png"
archivoSalida = "proyimod1T.png"

# Definimos un caracter de terminacion, de 8 bits, esto nos sirve en caso de que la imagen sea mucho mas grande
# que el mensaje que queremos introducir o extraer en una imagen. A la hora de extraer el mensaje, si a la hora de colocar
# el mensaje oculto dentro de la imagen, si el mensaje a introducir es corto, y queremose evitar tener que rellenar todo el docuemtno
# tenemos que dejar la imagen tal y como esta, es decir, no queremos recorrer el resto de pixeles ni rellenarlos con 0 o modificar su
# contenido actual, es por ello que tras introducir el mensaje, añadiremos el caracter de terminacion.
# El caracter de terminacion es un byte con todos sus bits a 1.

caracterTerminacion = [1, 1, 1, 1, 1, 1, 1, 1]

# Lo que tenemos que hacer ahora es, una funcion que pasa cada caracter de la imagen a codigo ascii, luego dicho codigo ascii
# lo queremos pasar a binario, para poder luego extraer / introducir el mensaje, segun proceda.
# La funcion ord de python devuelve la representacion unicode del caracter

def obtener_representacion_ascii(caracter):
	return ord(caracter)

# Ahora queremos una funcion que, dado un numero como parametro de entrada, obtenga su representacion en binario.
# Como queremos obtenerlo en formato de un bit entero, utilizamos la funcion bin para pasar dicho numero a binario, y luego
# utilizamos la funcion zfill[x] para rellenar hasta x caracteres con 0's, en nuestro caso zfill[8] rellena el numero con tantos 0's
# como sea necesario para llegar a 8 caracteres.

def obtener_representacion_binaria(numero):
	return bin(numero)[2:].zfill(8)

# Necesitamos ahora una nueva funcion que, dado un byte entero y un bit nuevo, nos cambie el ultimo bit de dicho byte.

def cambiar_ultimo_bit(byte, nuevo_bit):
	return byte[:-1] + str(nuevo_bit)

# Hacemos ahora una funcion que, dado un numero binario, haga lo contrario a lo que hicimos con obtener representacion binaria.
# Es decir, queremos que dicho numero binario se pase a notacion decimal.

def binario_a_decimal(binario):
	return int(binario, 2)

# Dado un color original, y un bit, lo que queremos hacer es cambiar el color original que aparece en la imagen,
# para ello lo que tener que hacer es pasar el color a binario y luego modificarlo con el valor que tenemos tambien en el bit
# y devolvemos el valor decimal del color modificado

def modificar_color(color_original, bit):
	color_binario = obtener_representacion_binaria(color_original)
	color_modificado = cambiar_ultimo_bit(color_binario, bit)
	return binario_a_decimal(color_modificado)

# Ahora creamos una funcion que, dado un texto, que obtendremos de la imagen, crea una lista vacia, y luego obtenemos la representacion en ascii y en binario
# de dicho caracter. Al final de la funcion, lo que vamos a hacer es añadir a la lista todos los caracteres del texto en formato binario.

def obtener_lista_de_bits(texto):
	lista = []
	for letra in texto:
		representacion_ascii = obtener_representacion_ascii(letra)
		representacion_binaria = obtener_representacion_binaria(representacion_ascii)
		for bit in representacion_binaria:
			lista.append(bit)
	for bit in caracter_terminacion:
		lista.append(bit)
	return lista

# Ahora leemos un caracter unicode y lo transformamos en caracter legible, el proceso
# exactamente inverso al que hicimos anteriormente

caracter_terminacion = "11111111"

# Ahora una funcion que dado un caracter en unicode, lo transforma a numero decimal

def caracter_desde_codigo_ascii(numero):
	return chr(numero)

# Ahora queremos hacer nuestra primera funcion grande, aquella que nos va a ocultar el mensaje que queramos dentro de nuestra imagen.
# Para ello, recibiremos como parametros la imagen que queremos utilizar para ocultar el mensaje. Dada una imagen original, que es la que
# hemos definido arriba al principio, lo que haremos sera abrir la imagen y extraer todos los pixeles, junto a su altura y anchura.
# Seguido de esto, obtendremos en una lista la cantidad de bits que tiene la imagen y su longitud, y la recorreremos entera.
# Recorremos tanto la altura como la anchura de la imagen y lo que queremos hacer es obtener los colores que contiene cada pixel,
# para poder luego modificar los binarios de cada color (rojo,verde,azul) para poder insertar el mensaje dentro de la imagen.

def ocultar_texto(rutaImagenOriginal):
        # Abrimos la imagen utilizando el modulo PIL
	imagen = Image.open(rutaImagenOriginal)
	
	# Cargamos los pixeles con la funcion load del moduflo PIL
	pixeles = imagen.load()
	# Abrimos la imagen, con el titulo correspondiente
	imagen.show(title="Imagen original")
	# Calculamos la anchura y la altura utilizando size del modulo PIL
	# que devuelve un array donde la primera posicion es la anchura y la segunda altura
	tamaño = imagen.size
	anchura = tamaño[0]
	altura = tamaño[1]
	# Sacamos por pantalla las dos primeras lineas requeridas por el DPF
	print(rutaImagenOriginal,"tiene de",anchura,"de ancho y de",altura,"de alto")
	print()
	mensaje=input("Introduzca el mensaje de texto a ocultar: ")
	print()
	# Entramos dentro del bucle como explicamos mas arriba para cambiar los valores
	# binarios de los pixeles y luego insertarlos en la imagen junto a nuestro mensaje
	lista = obtener_lista_de_bits(mensaje)
	contador = 0
	longitud = len(lista)
	# Vamos recorriendo tanto por los bits de anchura como los de altura y vamos viendo si el contador es menor a la longitud para seguri recorriendo
	# en caso de ser asi, añadimos los colores modificamos a la lista que tenemos para luego devolverla como pixel.
	for x in range(anchura):
		for y in range(altura):
			if contador < longitud:
				pixel = pixeles[x, y]


				rojo = pixel[0]
				verde = pixel[1]
				azul = pixel[2]

				if contador < longitud:
					rojo_modificado = modificar_color(rojo, lista[contador])
					contador += 1
				else:
					rojo_modificado = rojo

				if contador < longitud:
					verde_modificado = modificar_color(verde, lista[contador])
					contador += 1
				else:
					verde_modificado = verde

				if contador < longitud:
					azul_modificado = modificar_color(azul, lista[contador])
					contador += 1
				else:
					azul_modificado = azul

				pixeles[x, y] = (rojo_modificado, verde_modificado, azul_modificado)
			else:
				break
		else:
			continue
		break

	if contador >= longitud:
                # De nuevo, los prints necesarios por el PDF, con sus huecos correspondientes
		print("Insertando el texto en la imagen...")
		print()
	else:
		print("Advertencia: no se pudo escribir todo el mensaje, sobraron {} caracteres".format( math.floor((longitud - contador) / 8) ))
	# Guardamos la imagen en otro archivo, como se nos pide
	imagen.save("proyimod1T.png")
	# Guardamos en una variable el nombre del archivo de salida para poder meterlo en el print
	imagenDeSalida = "proyimod1T.png"
	print ("El fichero",rutaImagenOriginal,"es diferente a",imagenDeSalida)
	imagenSalida = Image.open(imagenDeSalida)
	imagenSalida.show()


# Ahora queremos hacer lo mismo, obtener un byte entero de terminacion para poder saber cuando dejar de leer y de traducir el mensaje de la imagen,
# Para ello vamos a obtener lo que se llama lsb o bit menos significativo

caracter_terminacion = "11111111"


# Obtenemos una funcion que obtiene el ultimo bit de un byte, para poder leer correctamente, es decir
# obtenemos el bit menos significativo

def obtener_lsb(byte):
	return byte[-1]

# Dada una ruta de la imagen, cargamos dicha imagen y tanto los pixeles como la altura y la anchura de la misma
# Para luego inicializar un byte y mensaje vacios, para ir introduciendo datos poco a poco

def leer(ruta_imagen):
	imagen = Image.open(ruta_imagen)
	pixeles = imagen.load()

	tamaño = imagen.size
	anchura = tamaño[0]
	altura = tamaño[1]

	byte = ""
	mensaje = ""

	# Recorremos con dos bucles todo el archivo, el primero para anchura y el siguiente para altura

	for x in range(anchura):
		for y in range(altura):

                        # Creamos un pixel con los elementos de ambos bucles

                        # Creamos los colores de los pixeles, los colores son RGB
                        
			pixel = pixeles[x, y]

			rojo = pixel[0]
			verde = pixel[1]
			azul = pixel[2]

			# Poco a poco vamos obtieniendo la representacion de los bytes que vamos a ir añadiendo
			# A la variable byte y vamos añadiendo dentro de mensaje el resultado que vamos encontrando en la imagen
			# Por ultimo, devolvemos el mensaje que se encontro en la imagen

			byte += obtener_lsb(obtener_representacion_binaria(rojo))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

			byte += obtener_lsb(obtener_representacion_binaria(verde))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

			byte += obtener_lsb(obtener_representacion_binaria(azul))
			if len(byte) >= 8:
				if byte == caracter_terminacion:
					break
				mensaje += caracter_desde_codigo_ascii(binario_a_decimal(byte))
				byte = ""

		else:
			continue
		break
	return mensaje

# Por ultimo creamos la opcion de convertir a escala de grises
# Abrimos la imagen original y lo guardamos en una imagen que se llama escalaGris con formato png
# Utilizamos la funcion convert con LA para poderlo convertir completamente en escala de grises.
# Segun la documentacion oficial, L convierte a escala de grises, mientras que A, amplia las tonalidades de grises
# segun la norma ITU-R 601-2. Doc oficial: https://pillow.readthedocs.io/en/stable/reference/Image.html


def cambiarEscalaGrises():
        print ("OPCIÓN: convertir la imagen a escala de grises")
        print()
        print ("El fichero con la imagen se llama: ",rutaImagenOriginal)
        print ("Conviertiendo la imagen a escala de grises...")
        img = Image.open(rutaImagenOriginal).convert('LA')
        img.save('escalaGrises.png')
        img.show()

# Simplemente queda definir el menu, imprimir por pantalla las opciones correctas y con los formatos necesarios
# Y llamar a las funciones correspondientes.

ans=True
while ans:
    print ("""
    1) Insertar mensaje oculto en una imagen
    2) Extraer mensaje oculto de una imagen
    3) Convertir la imagen a escala de grises
    4) Salir
    """)
    ans=input("Por favor, seleccione una opción: ")
    print()
    if ans=="1":
        print ("OPCIÓN: Insertar mensaje oculto en una imagen")
        print()
        ocultar_texto(rutaImagenOriginal)
    elif ans=="2":
        print ("OPCION: extraer mensaje oculto de una imagen")
        print()
        mensaje = leer("proyimod1T.png")
        print ("Extrayendo el texto de la imagen...")
        print()
        print("El texto oculto es: ",mensaje)
    elif ans=="3":
        cambiarEscalaGrises()
    elif ans=="4":
        raise SystemExit
    elif ans !="":
      print("Opcion inválida, por favor selecciona otra opcion")
