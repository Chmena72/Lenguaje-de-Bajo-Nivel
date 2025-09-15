class SimuladorEnsamblador:
    def __init__(self, tamaño_memoria=100):
        # Registros
        self.acc = 0          # Acumulador
        self.pc = 0           # Contador de programa
        self.r1 = 0           # Registro general 1
        self.r2 = 0           # Registro general 2
        
        # Memoria
        self.memoria = [0] * tamaño_memoria
        self.tamaño_memoria = tamaño_memoria
        
        # Programa
        self.programa = []
        
        # Estado de ejecución
        self.ejecutando = False
    
    def cargar_programa(self, instrucciones):
        """Carga un programa en memoria"""
        self.programa = instrucciones
    
    #Modos de direccionamiento
    def obtener_operando(self, op):
        if op is None:
            return None
        
        # Inmediato (#n)
        if isinstance(op, str) and op.startswith("#"):
            return int(op[1:])

        # Indirecto (@n)
        elif isinstance(op, str) and op.startswith("@"):
            dir = int(op[1:])
            return self.memoria[self.memoria[dir]]

        # Relativo (+n)
        elif isinstance(op, str) and op.startswith("+"):
            desplazamiento = int(op[1:])
            return self.memoria[self.pc + desplazamiento]

        # Indexado (n(R1), n(R2))
        elif isinstance(op, str) and "(" in op and ")" in op:
            base, reg = op.split("(")
            reg = reg.replace(")", "")
            base = int(base)
            if reg == "R1":
                return self.memoria[base + self.r1]
            elif reg == "R2":
                return self.memoria[base + self.r2]
            else:
                raise Exception(f"Registro {reg} no soportado en indexado")

        # Registro directo
        elif op == "ACC":
            return self.acc
        elif op == "R1":
            return self.r1
        elif op == "R2":
            return self.r2

        # Directo (n)
        else:
            return self.memoria[int(op)]
    
    def guardar_operando(self, destino, valor):
        if destino == "ACC":
            self.acc = valor
        elif destino == "R1":
            self.r1 = valor
        elif destino == "R2":
            self.r2 = valor
        else:
            self.memoria[int(destino)] = valor
    
    # Instrucciones
    def LOAD(self, x):
        """Carga el valor x en el acumulador"""
        self.acc = self.obtener_operando(x)
        self.pc += 1
    
    def STORE(self, x):
        """Almacena el ACC en la dirección de memoria x"""
        self.guardar_operando(x, self.acc)
        self.pc += 1
    
    def ADD(self, x):
        """Suma x al acumulador"""
        self.acc += self.obtener_operando(x)  # Acc += x
        self.pc += 1
    
    def SUB(self, x):
        """Resta x del acumulador"""
        self.acc -= self.obtener_operando(x)  # Acc -= x
        self.pc += 1
    
    def OUTPUT(self, x):
        """Simula una salida (puede ser impresión o almacenamiento)"""
        print(f"SALIDA: {x} (ACC = {self.acc}), R1 = {self.r1}, R2 = {self.r2}")
        self.pc += 1
    
    def JMP(self, x):
        """Salto incondicional a la dirección x"""
        self.pc = int(x) 
    
    def JZ(self, x):
        """Salta a x si el acumulador es cero"""
        if self.acc == 0:
            self.pc = int(x)  
        else:
            self.pc += 1
    
    def HALT(self):
        """Detiene la ejecución del programa"""
        self.ejecutando = False
        self.pc += 1
        
    def ejecutar(self):
        """Ejecuta el programa cargado"""
        if not self.programa:
            print("Error: No hay programa cargado")
            return
        
        self.ejecutando = True
        self.pc = 0  # Empezar desde la primera instrucción
        
        print("INICIANDO EJECUCIÓN")
        
        while self.ejecutando and self.pc < len(self.programa):
            # Obtener instrucción actual
            instruccion = self.programa[self.pc]
            opcode = instruccion[0]
            operando = instruccion[1] if len(instruccion) > 1 else None
            
            print(f"PC={self.pc}: {opcode} {operando if operando is not None else ''}")
            
            # Ejecutar instrucción
            try:
                if opcode == "CARGA":
                    self.LOAD(operando)
                elif opcode == "ALMACENA":
                    self.STORE(operando)
                elif opcode == "SUMA":
                    self.ADD(operando)
                elif opcode == "RESTA":
                    self.SUB(operando)
                elif opcode == "SALIDA":
                    self.OUTPUT(operando)
                elif opcode == "SALTA":
                    self.JMP(operando)
                elif opcode == "SALTA_SI_CERO":
                    self.JZ(operando)
                elif opcode == "DETENER":
                    self.HALT()
                else:
                    print(f"Error: Instrucción desconocida '{opcode}'")
                    break
            except Exception as e:
                print(f"Error en ejecución: {e}")
                break
            
            # Mostrar estado actual
            print(f"  ACC={self.acc}, R1={self.r1}, R2={self.r2}")
            print(f"  Memoria[0:5]: {self.memoria[:5]}...")
            print()
        
        print("EJECUCIÓN FINALIZADA")
        print(f"Estado final: ACC={self.acc}, PC={self.pc}")
        print(f"Memoria: {self.memoria}")

# Ejemplo de uso
def suma_simple():
    """Crea un programa de ejemplo que suma 5 + 3 y almacena el resultado"""
    programa = [
    ["CARGA", "#5"],        # Inmediato → ACC = 5
    ["ALMACENA", "10"],     # Directo → MEM[10] = 5
    ["CARGA", "10"],        # Directo → ACC = MEM[10] = 5
    ["SUMA", "#3"],         # Inmediato → ACC = 8
    ["ALMACENA", "R1"],     # Guarda en registro R1 → R1 = 8
    ["CARGA", "0(R1)"],     # Indexado → ACC = MEM[0 + R1]
    ["DETENER"]
    ]
    return programa

def suma_con_salto():
    """Crea un programa de ejemplo que suma 2 números con salto condicional"""
    programa = [
        ["CARGA", "#0"],        # ACC = 0
        ["ALMACENA", "20"],     # MEM[20] = 0 (acumulador)
        ["CARGA", "#5"],        # ACC = 5 (primer sumando)
        ["ALMACENA", "21"],     # MEM[21] = 5
        ["CARGA", "#3"],        # ACC = 3 (segundo sumando)
        ["ALMACENA", "22"],     # MEM[22] = 3
        ["CARGA", "21"],        # ACC = MEM[21] (primer sumando)
        ["SUMA", "22"],         # ACC += MEM[22] (segundo sumando)
        ["ALMACENA", "20"],     # MEM[20] = ACC (resultado)
        ["CARGA", "20"],        # ACC = MEM[20] (cargar resultado)
        ["SALIDA", "ACC"],      # Salida del resultado
        ["DETENER"]
    ]
    return programa

def resta():
    """Crea un programa de ejemplo que resta 10 - 4 y almacena el resultado"""
    programa = [
        ["CARGA", "#10"],       # ACC = 10
        ["ALMACENA", "30"],     # MEM[30] = 10
        ["CARGA", "#4"],        # ACC = 4
        ["ALMACENA", "31"],     # MEM[31] = 4
        ["CARGA", "30"],        # ACC = MEM[30] (10)
        ["RESTA", "31"],        # ACC -= MEM[31] (4) → ACC = 6
        ["ALMACENA", "R2"],     # R2 = 6
        ["CARGA", "0(R2)"],     # ACC = MEM[0 + R2]
        ["DETENER"]
    ]
    return programa

def direccionamiento_indirecto():
    """Crea un programa de ejemplo que usa direccionamiento indirecto"""
    programa = [
        ["CARGA", "#7"],        # ACC = 7
        ["ALMACENA", "40"],     # MEM[40] = 7
        ["CARGA", "#1"],        # ACC = 1
        ["ALMACENA", "41"],     # MEM[41] = 1 (dirección de MEM[40])
        ["CARGA", "@41"],       # ACC = MEM[MEM[41]] = MEM[1] = 7
        ["DETENER"]
    ]
    return programa

def direccionamiento_relativo():
    """Crea un programa de ejemplo que usa direccionamiento relativo"""
    programa = [
        ["CARGA", "#10"],       # ACC = 10
        ["ALMACENA", "50"],     # MEM[50] = 10
        ["CARGA", "+2"],        # ACC = MEM[PC + 2] = MEM[3] (que es 20)
        ["ALMACENA", "51"],     # MEM[51] = 20
        ["CARGA", "50"],        # ACC = MEM[50] = 10
        ["SUMA", "51"],         # ACC += MEM[51] = 20 → ACC = 30
        ["DETENER"],
        ["#20"]                 # Esta instrucción es solo un dato para el relativo
    ]
    return programa

def direccionamiento_indexado():
    """Crea un programa de ejemplo que usa direccionamiento indexado"""
    programa = [
        ["CARGA", "#3"],        # ACC = 3
        ["ALMACENA", "60"],     # MEM[60] = 3
        ["CARGA", "#2"],        # ACC = 2
        ["ALMACENA", "61"],     # MEM[61] = 2
        ["CARGA", "60"],        # ACC = MEM[60] = 3
        ["ALMACENA", "R1"],     # R1 = 3
        ["CARGA", "0(R1)"],     # ACC = MEM[0 + R1] = MEM[3]
        ["DETENER"]
    ]
    return programa

def programa_completo():
    """Crea un programa de ejemplo que usa varias instrucciones y modos"""
    programa = [
        ["CARGA", "#4"],        # ACC = 4
        ["ALMACENA", "70"],     # MEM[70] = 4
        ["CARGA", "#6"],        # ACC = 6
        ["ALMACENA", "71"],     # MEM[71] = 6
        ["CARGA", "70"],        # ACC = MEM[70] = 4
        ["SUMA", "71"],         # ACC += MEM[71] = 6 → ACC = 10
        ["ALMACENA", "R2"],     # R2 = 10
        ["CARGA", "0(R2)"],     # ACC = MEM[0 + R2] = MEM[10]
        ["SALIDA", "ACC"],      # Salida del resultado
        ["DETENER"]
    ]
    return programa

def error_programa():
    """Crea un programa de ejemplo que contiene un error (instrucción desconocida)"""
    programa = [
        ["CARGA", "#5"],        # ACC = 5
        ["ALMACENA", "80"],     # MEM[80] = 5
        ["CARGA", "80"],        # ACC = MEM[80] = 5
        ["MULTIPLICA", "#2"],   # Instrucción inválida
        ["DETENER"]
    ]
    return programa

# Ejecutar demostración
if __name__ == "__main__":
    casos = [
        ("Suma simple", suma_simple()),
    ]
    simulador = SimuladorEnsamblador()
    
    # Cargar y ejecutar programa de ejemplo
    print("Suma simple")
    simulador.cargar_programa(suma_simple())
    simulador.ejecutar()
    
    print("\nSuma con salto condicional")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(suma_con_salto())
    simulador.ejecutar()
    
    print("\nResta")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(resta())
    simulador.ejecutar()
    
    print("\nDireccionamiento indirecto")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(direccionamiento_indirecto())
    simulador.ejecutar()
    
    print("\nDireccionamiento relativo")
    simulador = SimuladorEnsamblador()    
    simulador.cargar_programa(direccionamiento_relativo())
    simulador.ejecutar()
    
    print("\nDireccionamiento indexado")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(direccionamiento_indexado())
    simulador.ejecutar()
    
    print("\nPrograma completo")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(programa_completo())
    simulador.ejecutar()
    
    print("\nPrograma con error")
    simulador = SimuladorEnsamblador()
    simulador.cargar_programa(error_programa())
    simulador.ejecutar()