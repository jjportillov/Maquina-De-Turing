import os

class MaquinaDeTuringDosCintas:
    def __init__(self, estados, alfabeto_entrada, alfabeto_cinta, estado_inicial, estados_finales, transiciones, blanco):
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_cinta = alfabeto_cinta
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.transiciones = transiciones
        self.blanco = blanco
        
        # Inicialización de las cintas y cabezales
        self.cinta1 = []
        self.cinta2 = []
        self.head1 = 0
        self.head2 = 0
        self.estado_actual = estado_inicial
        self.historial = []
        self.log = ""

    def cargar_cintas(self, cadena):
        """Carga la cadena en la cinta 1 y vacía la cinta 2, ambas con blancos al final."""
        self.cinta1 = list(cadena) + [self.blanco]
        self.cinta2 = [self.blanco] * len(self.cinta1)
        self.head1 = 0
        self.head2 = 0
        self.estado_actual = self.estado_inicial
        self.historial.clear()
        self.log = f"Iniciando procesamiento para la cadena '{cadena}'\n"

    def obtener_cinta_id_di(self):
        """Obtiene el contenido de las cintas en ambas direcciones."""
        cinta1_id = ''.join(self.cinta1)  # Izquierda a derecha en cinta 1
        cinta1_di = ''.join(reversed(self.cinta1))  # Derecha a izquierda en cinta 1
        cinta2_id = ''.join(self.cinta2)  # Izquierda a derecha en cinta 2
        cinta2_di = ''.join(reversed(self.cinta2))  # Derecha a izquierda en cinta 2
        return cinta1_id, cinta1_di, cinta2_id, cinta2_di

    def paso(self):
        """Ejecuta un paso de la máquina de Turing según la función de transición."""
        simbolo1 = self.cinta1[self.head1] if self.head1 < len(self.cinta1) else self.blanco
        simbolo2 = self.cinta2[self.head2] if self.head2 < len(self.cinta2) else self.blanco
        transicion = self.transiciones.get((self.estado_actual, simbolo1, simbolo2))

        if not transicion:
            self.log += f"No se encontró una transición para ({self.estado_actual}, {simbolo1}, {simbolo2})\n"
            return False  # No hay transición posible

        nuevo_estado, escribir1, mover1, escribir2, mover2 = transicion
        self.log += f"({self.estado_actual}, {simbolo1}, {simbolo2}) -> ({nuevo_estado}, {escribir1}, {mover1}, {escribir2}, {mover2})\n"

        # Escribir en las cintas
        self.cinta1[self.head1] = escribir1
        self.cinta2[self.head2] = escribir2

        # Mover los cabezales
        if mover1 == 'R':
            self.head1 += 1
        elif mover1 == 'L':
            self.head1 -= 1

        if mover2 == 'R':
            self.head2 += 1
        elif mover2 == 'L':
            self.head2 -= 1

        # Expandir las cintas con blancos si los cabezales salen del tamaño actual
        if self.head1 >= len(self.cinta1):
            self.cinta1.append(self.blanco)
        if self.head2 >= len(self.cinta2):
            self.cinta2.append(self.blanco)
        if self.head1 < 0:
            self.cinta1.insert(0, self.blanco)
            self.head1 = 0
        if self.head2 < 0:
            self.cinta2.insert(0, self.blanco)
            self.head2 = 0

        # Actualizar el estado
        self.estado_actual = nuevo_estado
        # Añadir al historial para el árbol de derivación
        cinta1_id, cinta1_di, cinta2_id, cinta2_di = self.obtener_cinta_id_di()
        self.historial.append((self.estado_actual, simbolo1, simbolo2, nuevo_estado, cinta1_id, cinta1_di, cinta2_id, cinta2_di))

        return True

    def ejecutar(self, cadena):
        """Ejecuta la máquina en la cadena dada y genera el árbol de derivación y la tabla de transición."""
        self.cargar_cintas(cadena)
        
        while self.estado_actual not in self.estados_finales:
            if not self.paso():
                break  # Termina si no hay transición válida

        es_valida = self.estado_actual in self.estados_finales
        self.log += f"Resultado: La cadena '{cadena}' es {'válida' if es_valida else 'inválida'}\n"
        self.mostrar_tabla_transicion(cadena)
        self.mostrar_arbol_derivacion(cadena)

        return es_valida

    def mostrar_tabla_transicion(self, cadena):
        tabla = f"Tabla de Transición para la cadena '{cadena}':\n"
        tabla += f"{'Estado Actual':<15} {'Símbolo Cinta 1':<15} {'Símbolo Cinta 2':<15} {'Nuevo Estado':<15} {'Cinta1 ID':<15} {'Cinta1 DI':<15} {'Cinta2 ID':<15} {'Cinta2 DI':<15}\n"
        tabla += "-" * 120 + "\n"
        for estado_ant, simbolo1, simbolo2, estado_nuevo, cinta1_id, cinta1_di, cinta2_id, cinta2_di in self.historial:
            tabla += f"{estado_ant:<15} {simbolo1:<15} {simbolo2:<15} {estado_nuevo:<15} {cinta1_id:<15} {cinta1_di:<15} {cinta2_id:<15} {cinta2_di:<15}\n"
        self.log += tabla + "\n"

    def mostrar_arbol_derivacion(self, cadena):
        arbol = f"Árbol de Derivación para la cadena '{cadena}':\n"
        for i, (estado_ant, simbolo1, simbolo2, estado_nuevo, cinta1_id, cinta1_di, cinta2_id, cinta2_di) in enumerate(self.historial):
            arbol += f"Paso {i + 1}: ({estado_ant}) --[{simbolo1}, {simbolo2}]--> ({estado_nuevo}), Cinta1 ID: {cinta1_id}, Cinta1 DI: {cinta1_di}, Cinta2 ID: {cinta2_id}, Cinta2 DI: {cinta2_di}\n"
        self.log += arbol + "\n"

# Función para leer cadenas desde un archivo .txt
def leer_cadenas_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            # Lee y limpia cada línea del archivo
            cadenas = [linea.strip() for linea in archivo if linea.strip()]
        return cadenas
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return []

# Función para guardar el log completo en un archivo
def guardar_log_en_txt(log, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(log)

# Configuración de la Máquina de Turing
estados = {'q0', 'q1', 'q2', 'q3', 'qf', 'q7'}
alfabeto_entrada = {'a', 'b', '#', '*'}
alfabeto_cinta = {'a', 'b', '#', '*', '_'}
estado_inicial = 'q0'
estados_finales = {'qf'}
blanco = '_'

# Transiciones: (estado_actual, simbolo_cinta1, simbolo_cinta2): (nuevo_estado, escribir1, mover1, escribir2, mover2)
transiciones = {
    ('q0', 'a', '_'): ('q1', 'a', 'R', '_', 'R'),
    ('q1', 'b', '_'): ('q2', 'b', 'R', '_', 'R'),
    ('q2', '#', '_'): ('q3', '#', 'R', '_', 'R'),
    ('q3', 'a', '_'): ('qf', 'a', 'R', '_', 'R'),  # Aceptación en qf al encontrar 'a'
    ('q3', '*', '_'): ('qf', '*', 'R', '_', 'R'),   # Aceptación en qf al encontrar '*'
}

# Archivo de entrada y salida
nombre_archivo_entrada = 'cadenasturing.txt'
nombre_archivo_salida = 'resultado.txt'

# Leer las cadenas del archivo de entrada
cadenas = leer_cadenas_desde_archivo(nombre_archivo_entrada)

# Inicializar la máquina de Turing
mt = MaquinaDeTuringDosCintas(estados, alfabeto_entrada, alfabeto_cinta, estado_inicial, estados_finales, transiciones, blanco)

# Procesar cada cadena y almacenar el log
log_completo = ""
for cadena in cadenas:
    es_valida = mt.ejecutar(cadena)
    log_completo += mt.log + "\n"  # Añadir el log de cada ejecución
    print(mt.log)  # Mostrar log en consola (opcional)

# Guardar el log completo en el archivo de salida
guardar_log_en_txt(log_completo, nombre_archivo_salida)
