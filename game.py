import curses
import random
import time
import threading
from data import preguntas_faciles, preguntas_intermedias, preguntas_dificiles

RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def animacion_ruleta(nivel):
    """Animación de ruleta giratoria antes de cada pregunta con nivel"""
    simbolos = ['◐', '◓', '◑', '◒']
    print(f"\n{CYAN}╔════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║   🎡 GIRANDO LA RULETA...  🎡      ║{RESET}")
    print(f"{CYAN}║                                    ║{RESET}")
    print(f"{CYAN}║   NIVEL: {nivel:^22}║{RESET}")
    print(f"{CYAN}╚════════════════════════════════════╝{RESET}\n")
    
    for _ in range(15):
        for simbolo in simbolos:
            print(f"\r{MAGENTA}        {simbolo} {simbolo} {simbolo}  PREPARANDO PREGUNTA  {simbolo} {simbolo} {simbolo}{RESET}", end='', flush=True)
            time.sleep(0.1)
    
    print(f"\n\n{GREEN}✓ ¡Pregunta lista!{RESET}\n")
    time.sleep(0.5)


def inicializar_colores():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_YELLOW, -1)
    curses.init_pair(7, curses.COLOR_GREEN, -1)
    curses.init_pair(8, curses.COLOR_RED, -1)
    
    
def seleccionar_pregunta(pregunta):
    texto = pregunta["texto"]
    opciones = pregunta["opciones"].copy()
    correcta = opciones[pregunta["correcta"]]
    random.shuffle(opciones)
    indice_correcta = opciones.index(correcta)
    return texto, opciones, indice_correcta


def aplicar_50_50(opciones, indice_correcta):
    """Elimina 2 opciones incorrectas, dejando solo la correcta y una incorrecta"""
    indices_incorrectos = [i for i in range(len(opciones)) if i != indice_correcta]
    random.shuffle(indices_incorrectos)
    eliminados = indices_incorrectos[:2]
    return eliminados


def aplicar_llamada_amigo(stdscr, opciones, indice_correcta):
    """Simula una llamada a un amigo con temporizador de 1 minuto"""
    stdscr.clear()
    stdscr.nodelay(True)
    curses.curs_set(0)
    
    # Crear temporizador de 1 minuto para la llamada
    temporizador_llamada = TemporizadorPregunta(60)
    temporizador_llamada.iniciar()
    
    # El amigo tiene 70% de probabilidad de acertar
    if random.random() < 0.7:
        respuesta_amigo = indice_correcta
    else:
        respuesta_amigo = random.choice([i for i in range(len(opciones)) if i != indice_correcta])
    
    # Esperar mientras el temporizador corre
    while temporizador_llamada.tiempo_restante > 0:
        stdscr.clear()
        
        # Obtener dimensiones de la pantalla
        altura, ancho = stdscr.getmaxyx()
        
        # Dibujar temporizador en la esquina superior derecha
        x_temporizador = ancho - 15
        dibujar_temporizador(stdscr, temporizador_llamada, 0, x_temporizador)
        
        stdscr.addstr(2, 0, "📞 LLAMADA A UN AMIGO", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(4, 0, "Tienes 1 minuto para llamar a tu amigo", curses.color_pair(4))
        stdscr.addstr(6, 0, "Ring... Ring... Ring...", curses.color_pair(6))
        
        # Mostrar la sugerencia del amigo después de 3 segundos
        if temporizador_llamada.tiempo_restante <= 57:
            stdscr.addstr(8, 0, "¡Tu amigo contestó?!", curses.color_pair(2))
        
        stdscr.addstr(altura - 2, 0, "Presione cualquier tecla para regresar a la pregunta...", curses.color_pair(4))
        
        stdscr.refresh()
        
        # Verificar si el usuario presiona una tecla para salir antes
        try:
            tecla = stdscr.getch()
            if tecla != -1 and temporizador_llamada.tiempo_restante <= 57:
                break
        except:
            pass
        
        time.sleep(0.1)
    
    temporizador_llamada.detener()
    stdscr.nodelay(False)


def aplicar_pregunta_publico(stdscr, opciones, indice_correcta):
    """Simula pregunta al público con porcentajes"""
    stdscr.clear()
    stdscr.addstr(0, 0, "👥 PREGUNTA AL PÚBLICO", curses.color_pair(5))
    stdscr.addstr(2, 0, "Contando votos...", curses.color_pair(4))
    stdscr.refresh()
    time.sleep(2)
    
    # Generar porcentajes (la respuesta correcta tiene mayor probabilidad)
    porcentajes = [0] * len(opciones)
    porcentajes[indice_correcta] = random.randint(40, 60)
    
    restante = 100 - porcentajes[indice_correcta]
    for i in range(len(opciones)):
        if i != indice_correcta:
            if i == len(opciones) - 1 and sum(porcentajes) < 100:
                porcentajes[i] = 100 - sum(porcentajes)
            else:
                porcentajes[i] = random.randint(5, restante // 2)
                restante -= porcentajes[i]
    
    # Ajustar para que sume exactamente 100
    diferencia = 100 - sum(porcentajes)
    porcentajes[indice_correcta] += diferencia
    
    stdscr.addstr(4, 0, "Resultados:", curses.color_pair(6))
    for i, opcion in enumerate(opciones):
        barra = "█" * (porcentajes[i] // 2)
        stdscr.addstr(6 + i, 0, f"{opcion[:30]}: {porcentajes[i]}% {barra}", curses.color_pair(4))
    
    stdscr.addstr(6 + len(opciones) + 2, 0, "Presione cualquier tecla para continuar...", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()


class TemporizadorPregunta:
    """Clase para manejar el temporizador de cada pregunta"""
    def __init__(self, tiempo_limite):
        self.tiempo_limite = tiempo_limite
        self.tiempo_restante = tiempo_limite
        self.activo = True
        self.tiempo_agotado = False
        
    def iniciar(self):
        """Inicia el contador regresivo en un hilo separado"""
        def contar():
            while self.activo and self.tiempo_restante > 0:
                time.sleep(1)
                if self.activo:
                    self.tiempo_restante -= 1
            if self.tiempo_restante <= 0:
                self.tiempo_agotado = True
        
        hilo = threading.Thread(target=contar, daemon=True)
        hilo.start()
    
    def detener(self):
        """Detiene el temporizador"""
        self.activo = False
    
    def obtener_tiempo_restante(self):
        """Devuelve el tiempo restante formateado"""
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        return f"{minutos:02d}:{segundos:02d}"
    
    def obtener_color(self):
        """Devuelve el color según el tiempo restante"""
        porcentaje = (self.tiempo_restante / self.tiempo_limite) * 100
        if porcentaje > 50:
            return 7  # Verde
        elif porcentaje > 20:
            return 6  # Amarillo
        else:
            return 8  # Rojo


def dibujar_temporizador(stdscr, temporizador, y_pos, x_pos):
    """Dibuja el cuadro del temporizador en la pantalla"""
    tiempo_texto = temporizador.obtener_tiempo_restante()
    color = temporizador.obtener_color()
    
    # Dibujar cuadro decorativo
    stdscr.addstr(y_pos, x_pos, "╔══════════╗", curses.color_pair(color))
    stdscr.addstr(y_pos + 1, x_pos, "║  TIEMPO  ║", curses.color_pair(color))
    stdscr.addstr(y_pos + 2, x_pos, f"║  {tiempo_texto}  ║", curses.color_pair(color) | curses.A_BOLD)
    stdscr.addstr(y_pos + 3, x_pos, "╚══════════╝", curses.color_pair(color))


def seleccionar_opcion(stdscr, texto, opciones, comodines, indice_correcta, opciones_eliminadas, tiempo_limite):
    curses.curs_set(0)
    posicion_seleccion = 0
    
    # Crear y iniciar temporizador
    temporizador = TemporizadorPregunta(tiempo_limite)
    temporizador.iniciar()
    
    # Configurar para no bloquear en getch
    stdscr.nodelay(True)
    
    continuar = True
    while continuar:
        # Verificar si el tiempo se agotó
        if temporizador.tiempo_agotado:
            temporizador.detener()
            stdscr.nodelay(False)
            return -1  # Indica tiempo agotado
        
        stdscr.clear()
        
        # Obtener dimensiones de la pantalla
        altura, ancho = stdscr.getmaxyx()
        
        # Dibujar temporizador en la esquina superior derecha
        x_temporizador = ancho - 15
        dibujar_temporizador(stdscr, temporizador, 0, x_temporizador)
        
        # Mostrar comodines disponibles
        comodines_texto = "Comodines: "
        if comodines["50_50"]:
            comodines_texto += "[1] 50:50  "
        else:
            comodines_texto += "[X] 50:50  "
        
        if comodines["llamada"]:
            comodines_texto += "[2] Llamada  "
        else:
            comodines_texto += "[X] Llamada  "
        
        if comodines["publico"]:
            comodines_texto += "[3] Publico"
        else:
            comodines_texto += "[X] Publico"
        
        stdscr.addstr(0, 0, comodines_texto, curses.color_pair(6))
        stdscr.addstr(1, 0, "-" * (ancho - 16), curses.color_pair(4))
        stdscr.addstr(2, 0, texto, curses.color_pair(4))
        
        for i, opcion in enumerate(opciones):
            if i in opciones_eliminadas:
                stdscr.addstr(i + 4, 0, f"  [ELIMINADA]", curses.color_pair(3))
            elif i == posicion_seleccion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i + 4, 0, f"> {opcion}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i + 4, 0, f"  {opcion}")
        
        stdscr.addstr(len(opciones) + 6, 0, "Flechas: navegar | Enter: confirmar | 1,2,3: comodines", curses.color_pair(4))
        
        stdscr.refresh()
        
        try:
            tecla_presionada = stdscr.getch()
        except:
            tecla_presionada = -1
        
        if tecla_presionada != -1:
            # Navegación
            if tecla_presionada == curses.KEY_UP and posicion_seleccion > 0:
                posicion_seleccion -= 1
                while posicion_seleccion in opciones_eliminadas and posicion_seleccion > 0:
                    posicion_seleccion -= 1
            elif tecla_presionada == curses.KEY_DOWN and posicion_seleccion < len(opciones) - 1:
                posicion_seleccion += 1
                while posicion_seleccion in opciones_eliminadas and posicion_seleccion < len(opciones) - 1:
                    posicion_seleccion += 1
            elif tecla_presionada == curses.KEY_ENTER or tecla_presionada in [10, 13]:
                if posicion_seleccion not in opciones_eliminadas:
                    continuar = False
            
            # Comodines (pausan el temporizador)
            elif tecla_presionada == ord('1') and comodines["50_50"]:
                temporizador.detener()
                stdscr.nodelay(False)
                eliminados = aplicar_50_50(opciones, indice_correcta)
                opciones_eliminadas.extend(eliminados)
                comodines["50_50"] = False
                while posicion_seleccion in opciones_eliminadas:
                    posicion_seleccion = (posicion_seleccion + 1) % len(opciones)
                # Reiniciar temporizador con el tiempo restante
                tiempo_restante = temporizador.tiempo_restante
                temporizador = TemporizadorPregunta(tiempo_restante)
                temporizador.iniciar()
                stdscr.nodelay(True)
            
            elif tecla_presionada == ord('2') and comodines["llamada"]:
                tiempo_guardado = temporizador.tiempo_restante
                temporizador.detener()
                stdscr.nodelay(False)
                aplicar_llamada_amigo(stdscr, opciones, indice_correcta)
                comodines["llamada"] = False
                # Reiniciar temporizador con el tiempo que tenía ANTES de usar el comodín
                temporizador = TemporizadorPregunta(tiempo_guardado)
                temporizador.iniciar()
                stdscr.nodelay(True)
            
            elif tecla_presionada == ord('3') and comodines["publico"]:
                temporizador.detener()
                stdscr.nodelay(False)
                aplicar_pregunta_publico(stdscr, opciones, indice_correcta)
                comodines["publico"] = False
                # Reiniciar temporizador con el tiempo restante
                tiempo_restante = temporizador.tiempo_restante
                temporizador = TemporizadorPregunta(tiempo_restante)
                temporizador.iniciar()
                stdscr.nodelay(True)
        
        time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
    
    temporizador.detener()
    stdscr.nodelay(False)
    return posicion_seleccion


def mostrar_feedback(stdscr, texto, opciones, seleccion, indice_correcto, tiempo_agotado=False):
    stdscr.clear()
    stdscr.addstr(0, 0, texto, curses.color_pair(4))
    
    if tiempo_agotado:
        stdscr.addstr(1, 0, "⏰ ¡TIEMPO AGOTADO!", curses.color_pair(8) | curses.A_BOLD)
    
    linea_inicio = 3 if tiempo_agotado else 2
    
    for i, op in enumerate(opciones):
        if i == indice_correcto:  
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(i + linea_inicio, 0, f"✓ {op}")
            stdscr.attroff(curses.color_pair(2))
        elif i == seleccion and not tiempo_agotado:  
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(i + linea_inicio, 0, f"✗ {op}")
            stdscr.attroff(curses.color_pair(3))
        else:  
            stdscr.addstr(i + linea_inicio, 0, f"  {op}")
    
    stdscr.addstr(len(opciones) + linea_inicio + 2, 0, "Presione cualquier tecla para continuar", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()


def juego_curses(stdscr):
    inicializar_colores()
    curses.curs_set(0)
    
    # Inicializar comodines (cada uno se puede usar una vez)
    comodines = {
        "50_50": True,
        "llamada": True,
        "publico": True
    }
    
    niveles = [
        ("Fácil", preguntas_faciles.copy(), 30),        # 30 segundos
        ("Intermedio", preguntas_intermedias.copy(), 40),  # 40 segundos
        ("Difícil", preguntas_dificiles.copy(), 60)      # 60 segundos (1 minuto)
    ]
    
    puntuacion = 0
    
    for nombre_nivel, lista, tiempo_limite in niveles:
        random.shuffle(lista)
        
        for indice, preg in enumerate(lista):
            # Salir temporalmente de curses para mostrar la animación con el nivel
            curses.endwin()
            animacion_ruleta(nombre_nivel)
            stdscr = curses.initscr()
            inicializar_colores()
            curses.curs_set(0)
            
            texto, opciones_mezcladas, indice_correcta = seleccionar_pregunta(preg)
            
            opciones_eliminadas = []
            
            stdscr.clear()
            stdscr.addstr(0, 0, f"{nombre_nivel} - Pregunta {indice+1}", curses.color_pair(4))
            stdscr.refresh()
            
            seleccion = seleccionar_opcion(stdscr, texto, opciones_mezcladas, comodines, indice_correcta, opciones_eliminadas, tiempo_limite)
            
            tiempo_agotado = False
            if seleccion == -1:
                tiempo_agotado = True
            elif seleccion == indice_correcta:
                puntuacion += 1
            
            mostrar_feedback(stdscr, texto, opciones_mezcladas, seleccion, indice_correcta, tiempo_agotado)
    
    return {"puntuacion": puntuacion}


def jugar():
    resultado = curses.wrapper(juego_curses)
    print(f"\n{GREEN}═══════════════════════════════════════{RESET}")
    print(f"{YELLOW}   🏆 JUEGO TERMINADO 🏆{RESET}")
    print(f"{GREEN}═══════════════════════════════════════{RESET}")
    print(f"{CYAN}Puntuación final: {resultado['puntuacion']}/15{RESET}\n")
