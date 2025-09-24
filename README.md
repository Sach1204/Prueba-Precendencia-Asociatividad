# Prueba-Precedencia-Asociatividad
# Calculadora ANTLR4 - Precedencia y Asociatividad

Este proyecto implementa una calculadora usando **ANTLR4** para demostrar conceptos de **precedencia** y **asociatividad** de operadores matemáticos. Incluye dos gramáticas diferentes para mostrar cómo estos conceptos afectan la evaluación de expresiones.

## Estructura del Proyecto

```
proyecto/
├── calc.py                 # Programa principal
├── EvalVisitor.py         # Visitor para evaluar expresiones
├── labeldExpr.g4         # Gramática original
├── labeldExpr_alt.g4     # Gramática alternativa (modificada)
├── tests.txt             # Casos de prueba
```

## Componentes del Proyecto

### 1. `calc.py` - Programa Principal

Este es el punto de entrada del programa que:

```python
def load_parser_and_lexer(use_alt):
    # Permite alternar entre las dos gramáticas
    if use_alt:
        lexer_mod = 'labeldExpr_altLexer'
        parser_mod = 'labeldExpr_altParser'
    else:
        lexer_mod = 'labeldExprLexer'
        parser_mod = 'labeldExprParser'
```

**Características principales:**
- **Carga dinámica de gramáticas**: Puede usar la gramática original o la alternativa con `--alt`
- **Entrada flexible**: Acepta archivos o entrada estándar
- **Manejo de errores**: Verifica que los módulos ANTLR estén generados

### 2. `EvalVisitor.py` - Evaluador de Expresiones

Implementa el patrón Visitor para evaluar el árbol sintáctico:

```python
class EvalVisitor(labeldExprVisitor):
    def __init__(self):
        self.memory = {}          # Variables almacenadas
        self.use_degrees = True   # Modo de ángulos por defecto
```

**Funcionalidades implementadas:**

#### Operadores Básicos
- **Suma y resta**: `visitAddSub()`
- **Multiplicación y división**: `visitMulDiv()` (con protección contra división por cero)
- **Exponenciación**: `visitPow()` usando `math.pow()`
- **Menos unario**: `visitUnaryMinus()`

#### Funciones Avanzadas
- **Factorial**: `visitFact()` usando `math.factorial()`
- **Funciones trigonométricas**: `sin()`, `cos()`, `tan()` con conversión automática de grados/radianes
- **Logaritmos**: `ln()` (natural) y `log()` (base 10)
- **Raíz cuadrada**: `sqrt()`

#### Variables y Memoria
- **Asignación**: `x = 5` almacena valores en `self.memory`
- **Recuperación**: Las variables se evalúan desde la memoria

### 3. Gramáticas ANTLR4

#### `labeldExpr.g4` - Gramática Original

```antlr
expr
  : expr POW expr            #Pow
  | expr op=(MUL | DIV) expr #MulDiv
  | expr op=(ADD | SUB) expr #AddSub
  | expr FACT                #Fact
  | SUB expr                 #UnaryMinus
  | ID '(' expr ')'          #Function
  | INT | DOUBLE | ID        #Literales
  | '(' expr ')'             #Parens
  ;
```

**Precedencia (de mayor a menor):**
1. Paréntesis y funciones
2. Menos unario
3. Factorial (postfijo)
4. Exponenciación (`^`)
5. Multiplicación y división (`*`, `/`)
6. Suma y resta (`+`, `-`)

**Asociatividad:** Izquierda para todos los operadores binarios

#### `labeldExpr_alt.g4` - Gramática Alternativa

```antlr
expr
  : expr POW expr                            #Pow
  | <assoc=right> expr op=(ADD | SUB) expr   #AddSub
  | expr op=(MUL | DIV) expr                 #MulDiv
  | expr FACT                                #Fact
  | SUB expr                                 #UnaryMinus
  | ID '(' expr ')'                          #Function
  | INT | DOUBLE | ID                        #Literales
  | '(' expr ')'                             #Parens
  ;
```

**Diferencia clave:** 
- **Suma y resta tienen asociatividad derecha** (`<assoc=right>`)
- **Orden de precedencia alterado**: Suma/resta tienen mayor precedencia que multiplicación/división

## Instalación y Uso

### Prerrequisitos
```bash
pip install antlr4-python3-runtime
```

### Generar los archivos Python desde las gramáticas
```bash
# Para la gramática original
antlr4 -Dlanguage=Python3 -visitor labeldExpr.g4

# Para la gramática alternativa
antlr4 -Dlanguage=Python3 -visitor labeldExpr_alt.g4
```

### Ejecutar la calculadora

#### Usando la gramática original:
```bash
python calc.py tests.txt
```

#### Usando la gramática alternativa:
```bash
python calc.py --alt tests.txt
```
## Casos de Prueba

El archivo `tests.txt` contiene ejemplos que demuestran las diferencias:

```
2+3*4      # 14 o 20 Depende de la precedencia
2+3-4      # 1 o 5 Depende de la asociatividad  
2+3*(4-5)  # Los paréntesis tienen máxima precedencia
10-4-3     # 3 o 9 Asociatividad de la resta
2^3^2      # 64 o 512 Asociatividad de la exponenciación
5!         # Factorial: 120
sin(90)    # Funciones trigonométricas en grados
```

### Resultados Esperados

#### Gramática Original (precedencia estándar):
- `2+3*4` = 14 (multiplicación antes que suma)
- `2+3-4` = 1 (asociatividad izquierda: (2+3)-4)
- `10-4-3` = 3 (asociatividad izquierda: (10-4)-3)

<img width="1278" height="186" alt="image" src="https://github.com/user-attachments/assets/64f182fb-d7bb-4413-a05e-e779a363b968" />

#### Gramática Alternativa (precedencia modificada):
- `2+3*4` = 20 (suma antes que multiplicación)
- `2+3-4` = 5 (asociatividad derecha: 2+(3-4))
- `10-4-3` = 9 (asociatividad derecha: 10-(4-3))

<img width="1278" height="186" alt="image" src="https://github.com/user-attachments/assets/05293559-a73b-408b-8204-0a00fcc5697a" />

