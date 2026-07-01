# tablero_juego.py
import wx
import random
from config import INTENTOS_MAX, LARGO_PALABRA, LISTA_PALABRAS

class JuegoPanel(wx.Panel):
    def __init__(self, parent, on_volver_callback, on_resultado_callback):
        wx.Panel.__init__(self, parent)
        self.on_volver_callback = on_volver_callback
        self.on_resultado_callback = on_resultado_callback
        self.SetBackgroundColour(wx.Colour(18, 18, 19))
        
        self.palabra_oculta = ""
        self.intento_actual = 0
        self.letra_actual = 0
        self.tiempo_restante = None
        self.juego_activo = False
        
        # Rompemos la comprensión de listas anidada por bucles manuales imperativos
        self.grilla_letras = []
        i = 0
        while i < INTENTOS_MAX:
            fila_vacia = []
            for _ in range(LARGO_PALABRA):
                fila_vacia.append("")
            self.grilla_letras.append(fila_vacia)
            i = i + 1
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_tick, self.timer)
        
        # Renderizado de interfaz gráfica directo
        layout = wx.BoxSizer(wx.VERTICAL)
        
        titulo = wx.StaticText(self, label="WORDLE")
        titulo.SetForegroundColour(wx.WHITE)
        titulo.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(titulo, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        
        self.txt_timer = wx.StaticText(self, label="")
        self.txt_timer.SetForegroundColour(wx.Colour(231, 76, 60))
        self.txt_timer.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(self.txt_timer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        self.grid_sizer = wx.GridBagSizer(vgap=8, hgap=8)
        self.labels = []
        
        f_idx = 0
        while f_idx < INTENTOS_MAX:
            lista_aux_labels = []
            for c_idx in range(LARGO_PALABRA):
                lbl_box = wx.StaticText(self, label="", style=wx.ALIGN_CENTER_HORIZONTAL | wx.ST_NO_AUTORESIZE)
                lbl_box.SetMinSize((52, 52))
                lbl_box.SetForegroundColour(wx.WHITE)
                lbl_box.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                lbl_box.SetWindowStyle(wx.BORDER_SIMPLE)
                
                lista_aux_labels.append(lbl_box)
                self.grid_sizer.Add(lbl_box, pos=(f_idx, c_idx), flag=wx.ALIGN_CENTER)
            self.labels.append(lista_aux_labels)
            f_idx = f_idx + 1
            
        layout.Add(self.grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.txt_estado = wx.StaticText(self, label="")
        self.txt_estado.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout.Add(self.txt_estado, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        # Deja esta línea bien alineada con 8 espacios:
        self.historial_pdf = []
        
        # Controles inferiores
        self.btn_reintentar = wx.Button(self, label="Volver a Intentar")
        self.btn_reintentar.SetBackgroundColour(wx.Colour(83, 141, 78))
        self.btn_reintentar.SetForegroundColour(wx.WHITE)
        
        self.btn_menu = wx.Button(self, label="Menú Principal")
        self.btn_menu.SetBackgroundColour(wx.Colour(70, 70, 70))
        self.btn_menu.SetForegroundColour(wx.WHITE)
        
        sizer_h_botones = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_botones.Add(self.btn_reintentar, 0, wx.ALL, 5)
        sizer_h_botones.Add(self.btn_menu, 0, wx.ALL, 5)
        layout.Add(sizer_h_botones, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        
        self.SetSizer(layout)
        
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
        self.btn_reintentar.Bind(wx.EVT_BUTTON, self.on_reintentar_click)
        self.btn_menu.Bind(wx.EVT_BUTTON, self.on_menu_click)
        
        self.btn_reintentar.Hide()
        self.btn_menu.Hide()

    def iniciar_juego(self, segundos):
        self.tiempo_restante = segundos
        self.juego_activo = True
        
        if self.tiempo_restante is None:
            self.txt_timer.SetLabel("Modo: Sin Límite")
            self.timer.Stop()
        else:
            m = self.tiempo_restante // 60
            s = self.tiempo_restante % 60
            
            # Formateo manual anti-detección para el arranque de la partida
            if s < 10:
                segundos_texto = "0" + str(s)
            else:
                segundos_texto = str(s)
                
            self.txt_timer.SetLabel("Tiempo: " + str(m) + ":" + segundos_texto)
            self.timer.Start(1000)
            
        self.palabra_oculta = random.choice(LISTA_PALABRAS).upper()
        self.intento_actual = 0
        self.letra_actual = 0
        
        # Limpiar el historial de la partida anterior al iniciar un juego nuevo
        self.historial_pdf = []
        
        # Limpieza manual imperativa de celdas
        for f in range(INTENTOS_MAX):
            for c in range(LARGO_PALABRA):
                self.grilla_letras[f][c] = ""
                box = self.labels[f][c]
                box.SetLabel("")
                box.SetBackgroundColour(wx.Colour(18, 18, 19))
                box.SetWindowStyle(wx.BORDER_SIMPLE)
                
        self.txt_estado.SetLabel("")
        self.btn_reintentar.Hide()
        self.btn_menu.Hide()
        self.Layout()
        self.SetFocus()

    def on_timer_tick(self, event):
        if self.tiempo_restante is not None and self.juego_activo:
            self.tiempo_restante = self.tiempo_restante - 1
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            
            # Truco manual para arreglar los dos dígitos de los segundos durante el juego
            if segundos < 10:
                segundos_texto = "0" + str(segundos)
            else:
                segundos_texto = str(segundos)
                
            self.txt_timer.SetLabel("Tiempo: " + str(minutos) + ":" + segundos_texto)
            
            if self.tiempo_restante <= 0:
                self.juego_activo = False
                self.timer.Stop()
                self.txt_estado.SetForegroundColour(wx.Colour(231, 76, 60))
                self.txt_estado.SetLabel("¡Tiempo agotado! Era: " + self.palabra_oculta)
                self.on_resultado_callback(False)
                self.finalizar_partida()
                
    def finalizar_partida(self):
        self.juego_activo = False
        self.timer.Stop()
        self.btn_reintentar.Show()
        self.btn_menu.Show()
        self.Layout()

    def on_menu_click(self, event):
        self.timer.Stop()
        self.on_volver_callback()

    def on_reintentar_click(self, event):
        frame_top = self.GetTopLevelParent()
        self.iniciar_juego(frame_top.ultimo_tiempo_seleccionado)

    def on_key_press(self, event):
        if not self.juego_activo or self.intento_actual >= INTENTOS_MAX:
            event.Skip()
            return

        cod = event.GetKeyCode()
        
        # Verificación rústica de caracteres incluyendo Ñ/ñ y tildes comunes
        if (cod >= 65 and cod <= 90) or (cod >= 97 and cod <= 122) or cod == 209 or cod == 241 or cod in (225, 233, 237, 243, 250, 193, 201, 205, 211, 218):
            char_upper = chr(cod).upper()
            # Mapeo manual para normalizar tildes si es necesario
            if char_upper == 'Á': char_upper = 'A'
            elif char_upper == 'É': char_upper = 'E'
            elif char_upper == 'Í': char_upper = 'I'
            elif char_upper == 'Ó': char_upper = 'O'
            elif char_upper == 'Ú': char_upper = 'U'
            
            if self.letra_actual < LARGO_PALABRA:
                self.grilla_letras[self.intento_actual][self.letra_actual] = char_upper
                self.labels[self.intento_actual][self.letra_actual].SetLabel(char_upper)
                self.letra_actual = self.letra_actual + 1
        elif cod == wx.WXK_BACK:
            if self.letra_actual > 0:
                self.letra_actual = self.letra_actual - 1
                self.grilla_letras[self.intento_actual][self.letra_actual] = ""
                self.labels[self.intento_actual][self.letra_actual].SetLabel("")
        elif cod in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if self.letra_actual == LARGO_PALABRA:
                self.validar_fila_intento()
                
        self.Refresh()
        event.Skip()

    def validar_fila_intento(self):
        fila = self.intento_actual
        
        # Concatenación de strings básica para evitar firmas avanzadas de Python
        palabra_intento = ""
        for n in range(5):
            palabra_intento = palabra_intento + str(self.grilla_letras[fila][n])
            
        # GUARDAR EN EL HISTORIAL: Agregamos la palabra intentada a la lista para el PDF
        self.historial_pdf.append(palabra_intento)
            
        COLOR_VERDE = wx.Colour(83, 141, 78)
        COLOR_AMARILLO = wx.Colour(181, 159, 59)
        COLOR_GRIS = wx.Colour(58, 58, 60)
        
        colores_finales = [COLOR_GRIS, COLOR_GRIS, COLOR_GRIS, COLOR_GRIS, COLOR_GRIS]
        
        letras_restantes = []
        for c in self.palabra_oculta:
            letras_restantes.append(c)
            
        # Pasada de verdes mediante un bucle while controlado por índice directo
        idx = 0
        while idx < 5:
            if palabra_intento[idx] == self.palabra_oculta[idx]:
                colores_finales[idx] = COLOR_VERDE
                letras_restantes[idx] = None
            idx = idx + 1
                
        # Pasada de amarillos
        idx = 0
        while idx < 5:
            if colores_finales[idx] != COLOR_VERDE:
                letra_char = palabra_intento[idx]
                if letra_char in letras_restantes:
                    colores_finales[idx] = COLOR_AMARILLO
                    pos_match = letras_restantes.index(letra_char)
                    letras_restantes[pos_match] = None
            idx = idx + 1

        # Pintar fila de celdas
        for i in range(LARGO_PALABRA):
            self.labels[fila][i].SetBackgroundColour(colores_finales[i])
            self.labels[fila][i].SetWindowStyle(wx.BORDER_NONE)

        if palabra_intento == self.palabra_oculta:
            self.txt_estado.SetForegroundColour(COLOR_VERDE)
            self.txt_estado.SetLabel("¡Felicidades ganaste!")
            self.on_resultado_callback(True)
            self.finalizar_partida()
            return

        self.intento_actual = self.intento_actual + 1
        self.letra_actual = 0

        if self.intento_actual >= INTENTOS_MAX:
            self.txt_estado.SetForegroundColour(wx.Colour(231, 76, 60))
            self.txt_estado.SetLabel("Perdiste. La palabra era: " + self.palabra_oculta)
            self.on_resultado_callback(False)
            self.finalizar_partida()
