import wx
import random
from config import INTENTOS_MAX, LARGO_PALABRA, LISTA_PALABRAS

class JuegoPanel(wx.Panel):
    def __init__(self, parent, on_volver_callback, on_resultado_callback):
        super().__init__(parent)
        self.on_volver_callback = on_volver_callback
        self.on_resultado_callback = on_resultado_callback
        self.SetBackgroundColour(wx.Colour(18, 18, 19))
        
        # Variables de control de estado interno
        self.palabra_oculta = ""
        self.intento_actual = 0
        self.letra_actual = 0
        self.tiempo_restante = None
        self.juego_activo = False
        self.grilla_letras = [["" for _ in range(LARGO_PALABRA)] for _ in range(INTENTOS_MAX)]
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_tick, self.timer)
        
        self.init_ui()

    def init_ui(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        
        titulo = wx.StaticText(self, label="WORDLE")
        titulo.SetForegroundColour(wx.WHITE)
        titulo.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(titulo, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        
        self.lbl_cronometro = wx.StaticText(self, label="")
        self.lbl_cronometro.SetForegroundColour(wx.Colour(231, 76, 60))
        self.lbl_cronometro.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(self.lbl_cronometro, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        # Grilla del tablero
        self.grid_sizer = wx.GridBagSizer(vgap=8, hgap=8)
        self.labels = [[None for _ in range(LARGO_PALABRA)] for _ in range(INTENTOS_MAX)]
        fuente_celda = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        for fila in range(INTENTOS_MAX):
            for col in range(LARGO_PALABRA):
                lbl = wx.StaticText(self, label="", style=wx.ALIGN_CENTER_HORIZONTAL | wx.ST_NO_AUTORESIZE)
                lbl.SetMinSize((52, 52))
                lbl.SetForegroundColour(wx.WHITE)
                lbl.SetFont(fuente_celda)
                self.labels[fila][col] = lbl
                self.grid_sizer.Add(lbl, pos=(fila, col), flag=wx.ALIGN_CENTER)
                
        layout.Add(self.grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.txt_estado = wx.StaticText(self, label="")
        self.txt_estado.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(self.txt_estado, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        
        # Botonera de control inferior
        self.btn_reiniciar = wx.Button(self, label="Volver a Intentar")
        self.btn_reiniciar.SetBackgroundColour(wx.Colour(83, 141, 78))
        self.btn_reiniciar.SetForegroundColour(wx.WHITE)
        
        self.btn_menu = wx.Button(self, label="Menú Principal")
        self.btn_menu.SetBackgroundColour(wx.Colour(70, 70, 70))
        self.btn_menu.SetForegroundColour(wx.WHITE)
        
        sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botones.Add(self.btn_reiniciar, 0, wx.ALL, 5)
        sizer_botones.Add(self.btn_menu, 0, wx.ALL, 5)
        layout.Add(sizer_botones, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        
        self.SetSizer(layout)
        
        # Eventos compartidos
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.btn_reiniciar.Bind(wx.EVT_BUTTON, self.on_reiniciar_click)
        self.btn_menu.Bind(wx.EVT_BUTTON, self.on_menu_click)
        self.ocultar_controles_finales()

    def iniciar_partida(self, tiempo_limite):
        self.tiempo_restante = tiempo_limite
        self.juego_activo = True
        self.actualizar_ui_cronometro()
        
        if self.tiempo_restante is not None:
            self.timer.Start(1000)
        else:
            self.timer.Stop()
            
        self.reiniciar_juego()

    def actualizar_ui_cronometro(self):
        if self.tiempo_restante is None:
            self.lbl_cronometro.SetLabel("Modo: Sin Límite de Tiempo")
        else:
            minutos, segundos = divmod(self.tiempo_restante, 60)
            self.lbl_cronometro.SetLabel(f"Tiempo restante: {minutos:02d}:{segundos:02d}")

    def on_timer_tick(self, event):
        if self.tiempo_restante is not None and self.juego_activo:
            self.tiempo_restante -= 1
            self.actualizar_ui_cronometro()
            
            if self.tiempo_restante <= 0:
                self.juego_activo = False
                self.timer.Stop()
                self.txt_estado.SetForegroundColour(wx.Colour(231, 76, 60))
                self.txt_estado.SetLabel(f"¡Tiempo terminado! La palabra era: {self.palabra_oculta}")
                self.on_resultado_callback(ganado=False)
                self.finalizar_partida()

    def finalizar_partida(self):
        self.juego_activo = False
        self.timer.Stop()
        self.btn_reiniciar.Show()
        self.btn_menu.Show()
        self.Layout()

    def ocultar_controles_finales(self):
        self.btn_reiniciar.Hide()
        self.btn_menu.Hide()

    def on_menu_click(self, event):
        self.timer.Stop()
        self.on_volver_callback()

    def reiniciar_juego(self):
        self.palabra_oculta = random.choice(LISTA_PALABRAS).upper()
        self.intento_actual = 0
        self.letra_actual = 0
        self.juego_activo = True
        self.grilla_letras = [["" for _ in range(LARGO_PALABRA)] for _ in range(INTENTOS_MAX)]
        
        for fila in range(INTENTOS_MAX):
            for col in range(LARGO_PALABRA):
                lbl = self.labels[fila][col]
                lbl.SetLabel("")
                lbl.SetBackgroundColour(wx.Colour(18, 18, 19))
                lbl.SetWindowStyle(wx.BORDER_SIMPLE)
        
        self.txt_estado.SetLabel("")
        self.ocultar_controles_finales()
        self.Layout()
        self.SetFocus()

    def on_reiniciar_click(self, event):
        self.reiniciar_juego()
        if self.tiempo_restante is not None:
            app_parent = self.GetTopLevelParent()
            self.tiempo_restante = app_parent.ultimo_tiempo_seleccionado
            self.actualizar_ui_cronometro()
            self.timer.Start(1000)
    
    def on_key_down(self, event):
        if not self.juego_activo or self.intento_actual >= INTENTOS_MAX:
            event.Skip()
            return

        codigo_tecla = event.GetKeyCode()
        
        # Procesar Letras (A-Z)
        if (65 <= codigo_tecla <= 90) or (97 <= codigo_tecla <= 122):
            letra = chr(codigo_tecla).upper()
            if self.letra_actual < LARGO_PALABRA:
                self.grilla_letras[self.intento_actual][self.letra_actual] = letra
                self.labels[self.intento_actual][self.letra_actual].SetLabel(letra)
                self.letra_actual += 1
                
        # Procesar Borrado
        elif codigo_tecla == wx.WXK_BACK:
            if self.letra_actual > 0:
                self.letra_actual -= 1
                self.grilla_letras[self.intento_actual][self.letra_actual] = ""
                self.labels[self.intento_actual][self.letra_actual].SetLabel("")
                
        # Procesar Enter
        elif codigo_tecla in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if self.letra_actual == LARGO_PALABRA:
                self.verificar_intento()
                
        self.Refresh()
        event.Skip()

    def verificar_intento(self):
        fila = self.intento_actual
        palabra_intento = "".join(self.grilla_letras[fila])
        
        COLOR_VERDE = wx.Colour(83, 141, 78)
        COLOR_AMARILLO = wx.Colour(181, 159, 59)
        COLOR_GRIS = wx.Colour(58, 58, 60)
        
        letras_restantes = list(self.palabra_oculta)
        colores_finales = [COLOR_GRIS] * LARGO_PALABRA
        
        # Primer pasada: Buscar coincidencias exactas (Verdes)
        for i in range(LARGO_PALABRA):
            if palabra_intento[i] == self.palabra_oculta[i]:
                colores_finales[i] = COLOR_VERDE
                letras_restantes[i] = None
                
        # Segunda pasada: Coincidencias de posición incorrecta (Amarillos)
        for i in range(LARGO_PALABRA):
            if colores_finales[i] != COLOR_VERDE:
                if palabra_intento[i] in letras_restantes:
                    colores_finales[i] = COLOR_AMARILLO
                    letras_restantes[letras_restantes.index(palabra_intento[i])] = None

        # Pintar la fila en la interfaz
        for i in range(LARGO_PALABRA):
            self.labels[fila][i].SetBackgroundColour(colores_finales[i])
            self.labels[fila][i].SetWindowStyle(wx.BORDER_NONE)

        # se valida condición de Victoria
        if palabra_intento == self.palabra_oculta:
            self.txt_estado.SetForegroundColour(COLOR_VERDE)
            self.txt_estado.SetLabel("¡Felicidades ganaste!")
            self.on_resultado_callback(ganado=True)
            self.finalizar_partida()
            return

        self.intento_actual += 1
        self.letra_actual = 0

        # se valida la condición de Derrota
        if self.intento_actual >= INTENTOS_MAX:
            self.txt_estado.SetForegroundColour(wx.Colour(231, 76, 60))
            self.txt_estado.SetLabel(f"Perdiste. La palabra era: {self.palabra_oculta}")
            self.on_resultado_callback(ganado=False)
            self.finalizar_partida()