import board, time, neopixel, analogio, pwmio, digitalio

# ── LED de estado ────────────────────────────────────────────
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# ── Sensores de línea (analógico) ────────────────────────────
s1 = analogio.AnalogIn(board.IO35)   # frontal izquierdo
s2 = analogio.AnalogIn(board.IO34)   # frontal derecho
s3 = analogio.AnalogIn(board.IO39)   # trasero izquierdo
s4 = analogio.AnalogIn(board.IO36)   # trasero derecho

# ── Sensor ultrasónico HC-SR04 ───────────────────────────────
trig = digitalio.DigitalInOut(board.IO26)
trig.direction = digitalio.Direction.OUTPUT
echo = digitalio.DigitalInOut(board.IO25)
echo.direction = digitalio.Direction.INPUT

# ── Motores (PWM) ────────────────────────────────────────────
motor1_a = pwmio.PWMOut(board.IO12, frequency=1000)
motor1_b = pwmio.PWMOut(board.IO14, frequency=1000)
motor2_a = pwmio.PWMOut(board.IO13, frequency=1000)
motor2_b = pwmio.PWMOut(board.IO15, frequency=1000)

# ── Velocidades ──────────────────────────────────────────────
VEL_MAX    = 65535   # ataque total
VEL_NORMAL = 65535   # avance estándar → máximo
VEL_BUSCAR = 65535   # búsqueda → máximo para girar rápido
VEL_RETRO  = 65535   # retroceso → máximo para escapar rápido

# ── Distancias de acción (cm) ─────────────────────────────────
DIST_ATAQUE_TOTAL = 12   # rival muy cerca → velocidad máxima
DIST_ATAQUE_MEDIO = 25   # rival a media distancia → velocidad normal
DIST_BUSQUEDA     = 40   # rival lejos pero detectado → orientarse

# ── Umbrales sensores de línea ───────────────────────────────
UMBRAL_S1 = 10000
UMBRAL_S2 = 10000
UMBRAL_S3 = 10000
UMBRAL_S4 = 10000

# ── Estado de búsqueda ───────────────────────────────────────
busqueda_giro_derecha = True   # dirección del giro 360°

# ── Anti-arrastre: si los sensores traseros llevan N ciclos
#    activos seguidos, el robot está siendo empujado → contraataca
arrastre_contador = 0
ARRASTRE_UMBRAL = 3   # ciclos consecutivos para confirmar arrastre


# ================================================================
#  FUNCIONES DE MOVIMIENTO
# ================================================================

def adelante(vel=VEL_NORMAL):
    motor1_a.duty_cycle = vel
    motor1_b.duty_cycle = 0
    motor2_a.duty_cycle = 0
    motor2_b.duty_cycle = vel

def atras(vel=VEL_RETRO):
    motor1_a.duty_cycle = 0
    motor1_b.duty_cycle = vel
    motor2_a.duty_cycle = vel
    motor2_b.duty_cycle = 0

def girar_derecha(vel=VEL_NORMAL):
    motor1_a.duty_cycle = vel
    motor1_b.duty_cycle = 0
    motor2_a.duty_cycle = vel
    motor2_b.duty_cycle = 0

def girar_izquierda(vel=VEL_NORMAL):
    motor1_a.duty_cycle = 0
    motor1_b.duty_cycle = vel
    motor2_a.duty_cycle = 0
    motor2_b.duty_cycle = vel

# MEJORA: curvas diagonales para escapar en ángulo del borde
def curva_atras_derecha():
    """Retrocede girando hacia la derecha (motor izq más fuerte)."""
    motor1_a.duty_cycle = 0
    motor1_b.duty_cycle = VEL_RETRO
    motor2_a.duty_cycle = VEL_RETRO // 2
    motor2_b.duty_cycle = 0

def curva_atras_izquierda():
    """Retrocede girando hacia la izquierda (motor der más fuerte)."""
    motor1_a.duty_cycle = 0
    motor1_b.duty_cycle = VEL_RETRO // 2
    motor2_a.duty_cycle = VEL_RETRO
    motor2_b.duty_cycle = 0

def detener():
    motor1_a.duty_cycle = 0
    motor1_b.duty_cycle = 0
    motor2_a.duty_cycle = 0
    motor2_b.duty_cycle = 0


# ================================================================
#  SENSOR ULTRASÓNICO (más robusto)
# ================================================================

def leer_distancia():
    """
    MEJORA: timeout más estricto (15 ms), evita bloqueos largos.
    Devuelve 999 si no hay eco válido.
    """
    trig.value = False
    time.sleep(0.000002)
    trig.value = True
    time.sleep(0.00001)
    trig.value = False

    timeout = time.monotonic() + 0.015   # era 0.02
    while not echo.value:
        if time.monotonic() > timeout:
            return 999

    inicio = time.monotonic()
    timeout = time.monotonic() + 0.015
    while echo.value:
        if time.monotonic() > timeout:
            return 999

    return (time.monotonic() - inicio) * 34300 / 2


# ================================================================
#  DETECCIÓN DE BORDE (con anti-rebote doble lectura)
# ================================================================

def leer_s1(): return s1.value
def leer_s2(): return s2.value
def leer_s3(): return s3.value
def leer_s4(): return s4.value

def borde_frontal_izq():
    # MEJORA: confirma con 2 lecturas separadas para evitar falsos
    return leer_s1() < UMBRAL_S1 and leer_s1() < UMBRAL_S1

def borde_frontal_der():
    return leer_s2() < UMBRAL_S2 and leer_s2() < UMBRAL_S2

def borde_trasero_izq():
    return leer_s3() < UMBRAL_S3 and leer_s3() < UMBRAL_S3

def borde_trasero_der():
    return leer_s4() < UMBRAL_S4 and leer_s4() < UMBRAL_S4

def borde_frontal():
    return borde_frontal_izq() or borde_frontal_der()

def borde_trasero():
    return borde_trasero_izq() or borde_trasero_der()


# ================================================================
# ================================================================

def escapar_borde():
    global busqueda_giro_derecha
    pixel[0] = (255, 0, 0)   # rojo = borde detectado

    if borde_frontal():
        fi = borde_frontal_izq()
        fd = borde_frontal_der()

        if fi and fd:
            # Ambos sensores: retroceso recto
            atras()
        elif fi:
            # Solo izquierdo: retrocede en curva hacia la derecha
            curva_atras_derecha()
        else:
            # Solo derecho: retrocede en curva hacia la izquierda
            curva_atras_izquierda()

        # Retrocede hasta salir (máx 500 ms)
        for _ in range(10):
            time.sleep(0.05)
            if not borde_frontal():
                break

        # Gira hacia el lado seguro (opuesto al sensor que disparó)
        if fi and not fd:
            girar_derecha(VEL_NORMAL)
            busqueda_giro_derecha = False
        elif fd and not fi:
            girar_izquierda(VEL_NORMAL)
            busqueda_giro_derecha = True
        else:
            # Ambos: gira según alternancia para no repetir
            if busqueda_giro_derecha:
                girar_derecha(VEL_NORMAL)
            else:
                girar_izquierda(VEL_NORMAL)
            busqueda_giro_derecha = not busqueda_giro_derecha

        # Giro más largo (450 ms) para apuntar al centro
        for _ in range(9):
            time.sleep(0.05)
            if borde_frontal() or borde_trasero():
                break

    elif borde_trasero():
        ti = borde_trasero_izq()
        td = borde_trasero_der()

        # Avanza hacia adelante para alejarse del borde
        adelante()
        for _ in range(10):
            time.sleep(0.05)
            if not borde_trasero():
                break

        # Gira para orientar el frente al centro
        if ti and not td:
            girar_derecha(VEL_NORMAL)
        elif td and not ti:
            girar_izquierda(VEL_NORMAL)
        else:
            if busqueda_giro_derecha:
                girar_derecha(VEL_NORMAL)
            else:
                girar_izquierda(VEL_NORMAL)
            busqueda_giro_derecha = not busqueda_giro_derecha

        for _ in range(9):
            time.sleep(0.05)
            if borde_frontal() or borde_trasero():
                break

    detener()
    pixel[0] = (0, 0, 0)


# ================================================================
# BUSQUEDA
# ================================================================

TIEMPO_MEDIO_GIRO = 0.7   # segundos para ~180° a VEL_MAX (ajustar)
busqueda_inicio   = None  # marca de tiempo del inicio de búsqueda
busqueda_vueltas  = 0     # cuántas medias vueltas lleva

def buscar_rival():
    global busqueda_giro_derecha, busqueda_inicio, busqueda_vueltas

    pixel[0] = (0, 100, 255)   # azul claro = buscando

    ahora = time.monotonic()

    # Inicializar marca de tiempo la primera vez
    if busqueda_inicio is None:
        busqueda_inicio = ahora
        busqueda_vueltas = 0

    # Girar continuamente en la dirección elegida
    if busqueda_giro_derecha:
        girar_derecha(VEL_MAX)
    else:
        girar_izquierda(VEL_MAX)

    # Cada TIEMPO_MEDIO_GIRO segundos → completó media vuelta
    # Después de 2 medias vueltas (vuelta completa) invierte dirección
    if ahora - busqueda_inicio >= TIEMPO_MEDIO_GIRO:
        busqueda_inicio = ahora
        busqueda_vueltas += 1
        if busqueda_vueltas >= 2:
            busqueda_vueltas = 0
            busqueda_giro_derecha = not busqueda_giro_derecha


# ================================================================
#  CONTRAATAQUE ANTI-ARRASTRE
# ================================================================

def contrarrestar_arrastre():
    global busqueda_giro_derecha
    pixel[0] = (255, 0, 255)   # magenta = contraataque

    # Giro brusco a máxima velocidad (~150 ms ≈ 90°, ajustar)
    if busqueda_giro_derecha:
        girar_derecha(VEL_MAX)
    else:
        girar_izquierda(VEL_MAX)

    for _ in range(3):         # 3 × 50 ms = 150 ms
        time.sleep(0.05)
        if borde_frontal():    # si giró y ahora ve el borde frontal, para
            break

    # Tras girar, empuja hacia adelante para contraatacar
    adelante(VEL_MAX)
    for _ in range(6):
        if borde_frontal() or borde_trasero():
            break
        time.sleep(0.05)

    detener()
    busqueda_giro_derecha = not busqueda_giro_derecha  # alterna para siguiente vez


# ================================================================
#  ARRANQUE — parpadeo azul 3 segundos
# ================================================================

for _ in range(6):
    pixel[0] = (0, 0, 255)
    time.sleep(0.25)
    pixel[0] = (0, 0, 0)
    time.sleep(0.25)

pixel[0] = (0, 255, 0)   # verde = listo


# ================================================================
#  LOOP PRINCIPAL
# ================================================================

while True:

    # ── PRIORIDAD MÁXIMA: escapar del borde ─────────────────
    if borde_frontal() or borde_trasero():
        escapar_borde()
        busqueda_inicio = None   # resetea el temporizador de búsqueda
        arrastre_contador = 0
        continue

    # ── Prioridad 2: ultrasónico detecta rival ────────────────
    dist = leer_distancia()

    # ── Detección de arrastre ─────────────────────────────────
    # Si el sensor trasero se activa pero NO hay borde frontal,
    # es probable que el rival lo esté empujando por atrás
    if borde_trasero() and not borde_frontal():
        arrastre_contador += 1
    else:
        arrastre_contador = 0

    if arrastre_contador >= ARRASTRE_UMBRAL:
        arrastre_contador = 0
        busqueda_inicio = None
        contrarrestar_arrastre()
        continue

    if dist < DIST_ATAQUE_TOTAL:
        # Rival muy cerca → velocidad MÁXIMA
        pixel[0] = (255, 0, 0)       # rojo = ataque total
        busqueda_inicio = None       # interrumpe búsqueda
        adelante(VEL_MAX)
        for _ in range(6):
            if borde_frontal() or borde_trasero():
                break
            time.sleep(0.05)
        detener()

    elif dist < DIST_ATAQUE_MEDIO:
        # Rival a distancia media → velocidad máxima
        pixel[0] = (255, 165, 0)     # naranja = atacando
        busqueda_inicio = None
        adelante(VEL_MAX)
        for _ in range(8):
            if borde_frontal() or borde_trasero():
                break
            time.sleep(0.05)
        detener()

    elif dist < DIST_BUSQUEDA:
        # Rival detectado lejos → avanza a full
        pixel[0] = (255, 255, 0)     # amarillo = aproximándose
        busqueda_inicio = None
        adelante(VEL_MAX)
        for _ in range(4):
            if borde_frontal() or borde_trasero():
                break
            time.sleep(0.05)
        detener()

    else:
        # Nadie al frente → giro 360° continuo buscando rival
        buscar_rival()

    time.sleep(0.04)