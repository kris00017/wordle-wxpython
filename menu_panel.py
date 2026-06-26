# panel_menu.py
import wx

class MenuPanel(wx.Panel):
    def __init__(self, parent, on_play_callback):
        super().__init__(parent)
        self.on_play_callback = on_play_callback
        self.SetBackgroundColour(wx.Colour(43, 43, 43)) 
        
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        color_verde = wx.Colour(46, 204, 113) 
        color_texto_boton = wx.WHITE
        fuente_labels = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        label_titulo = wx.StaticText(self, label="Wordle", style=wx.ALIGN_CENTER)
        label_titulo.SetForegroundColour(wx.WHITE)
        label_titulo.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        btn_play = wx.Button(self, label="iniciar", size=(160, 35))
        self.configurar_estilo_boton(btn_play, color_verde, color_texto_boton)
        btn_play.Bind(wx.EVT_BUTTON, self.on_play_click)
        
        label_tiempo = wx.StaticText(self, label="Elegi el tiempo para terminar", style=wx.ALIGN_CENTER)
        label_tiempo.SetForegroundColour(wx.Colour(200, 200, 200))
        label_tiempo.SetFont(fuente_labels)
        
        opciones_tiempo = ["1 Minutos", "3 Minutos", "5 Minutos", "Sin Límite"]
        self.selector_tiempo = wx.Choice(self, choices=opciones_tiempo, size=(160, 35))
        self.selector_tiempo.SetSelection(1) 
        self.selector_tiempo.SetBackgroundColour(color_verde)
        self.selector_tiempo.SetForegroundColour(color_texto_boton)
        
        self.btn_victorias = wx.Button(self, label="Victorias: 0", size=(160, 35))
        self.configurar_estilo_boton(self.btn_victorias, color_verde, color_texto_boton)
        
        self.btn_derrotas = wx.Button(self, label="Derrotas: 0", size=(160, 35))
        self.configurar_estilo_boton(self.btn_derrotas, color_verde, color_texto_boton)
        
        sizer_principal.AddStretchSpacer(1)
        sizer_principal.Add(label_titulo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        sizer_principal.Add(btn_play, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        sizer_principal.Add(label_tiempo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        sizer_principal.Add(self.selector_tiempo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 35)
        sizer_principal.Add(self.btn_victorias, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sizer_principal.Add(self.btn_derrotas, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        sizer_principal.AddStretchSpacer(1)
        
        self.SetSizer(sizer_principal)

    def configurar_estilo_boton(self, boton, bg_color, fg_color):
        boton.SetBackgroundColour(bg_color)
        boton.SetForegroundColour(fg_color)
        boton.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def actualizar_puntuacion_ui(self, victorias, derrotas):
        self.btn_victorias.SetLabel(f"Victorias: {victorias}")
        self.btn_derrotas.SetLabel(f"Derrotas: {derrotas}")

    def on_play_click(self, event):
        seleccion = self.selector_tiempo.GetSelection()
        tiempos_segundos = {0: 60, 1: 180, 2: 300, 3: None}
        self.on_play_callback(tiempos_segundos[seleccion])