# Simulador Educativo de CPU
Un simulador de CPU desarrollado en Python que ejecuta programas en lenguaje ensamblador, diseñado para la enseñanza de arquitectura de computadoras.

## Descripción
Este proyecto implementa un simulador educativo de CPU capaz de ejecutar programas escritos en un lenguaje ensamblador, soportando seis modos de direccionamiento clásicos, teniendo como objetivo principal **visualizar el ciclo de instrucción** (fetch-decode-execute) y comprender cómo los modos de direccionamiento afectan el acceso a operandos, sin necesidad de hardware físico.

## Características Principales

- **Ciclo completo de instrucción**: Implementación del ciclo fetch-decode-execute
- **Modos de direccionamiento**: Soporte para 6 modos clásicos de direccionamiento
- **Visualización en tiempo real**: Trazado del estado de registros y memoria
- **Conjunto de instrucciones básicas**: 8 instrucciones fundamentales implementadas
- **Propósito educativo**: Diseñado específicamente para el aprendizaje

## Arquitectura del Simulador

### Componentes Implementados

#### Registros
- **ACC** (Acumulador): Almacena resultados de operaciones
- **PC** (Program Counter): Control de ejecución de instrucciones
- **R1, R2**: Registros de propósito general

#### Sistema de Memoria
-Memoria RAM simulada como arreglo configurable
-Almacenamiento compartido de instrucciones y datos (arquitectura Von Neumann)
-Inicialización automática en ceros

#### Unidades Funcionales
- **Unidad de Control (UC)**: Coordina el ciclo de instrucción
- **Unidad Aritmético-Lógica (ALU)**: Ejecuta operaciones matemáticas y lógicas

## Conjunto de Instrucciones
- **CARGA x**: Carga valor x en el acumulador 
- **ALMACENA x**: Guarda ACC en dirección x
- **SUMA x**: Suma valor x al acumulador 
- **RESTA x**: Resta valor x del acumulador 
- **SALIDA x**: Muestra valor en consola 
- **SALTA x**: Salto incondicional a posición x 
- **SALTA_SI_CERO x**: Salto condicional si ACC = 0 
- **DETENER**: Finaliza ejecución

## Modos de Direccionamiento Soportados

1. **Inmediato**: Operando incluido en la instrucción
2. **Directo**: Acceso directo a dirección de memoria
3. **Indirecto**: Dirección contenida en registro
4. **De registros**: Operando en registro
5. **Relativo**: Dirección calculada con desplazamiento del PC
6. **Indexado**: Combinación de registro índice y desplazamiento

## Objetivos Educativos
Este simulador permite:
-Comprender el funcionamiento interno de los procesadores
-Visualizar el ciclo de instrucción en tiempo real
-Analizar el impacto de diferentes modos de direccionamiento
-Conectar teoría y práctica de arquitectura de computadoras
-Aprender programación en lenguaje ensamblador

## Autores
- **ALAN  JESÚS  TRUJILLO  CAMARILLO**
- **EDUARDO  LÓPEZ  ATANASIO**
- **JIMENA  TORRES  PÉREZ**
- **ALEXANDER  LÓPEZ  HERNÁNDEZ**
- **ANGEL  YAEL  TELLEZ  ORTIZ**
## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.