# menu_inicio.py
import wx

class MenuPanel(wx.Panel):
    def __init__(self, parent, on_play_callback):
        wx.Panel.__init__(self, parent)
        self.on_play_callback = on_play_callback
        self.SetBackgroundColour(wx.Colour(43, 43, 43)) 
        
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        color_verde = wx.Colour(46, 204, 113) 
        color_texto_boton = wx.WHITE
        
        label_titulo = wx.StaticText(self, label="Wordle", style=wx.ALIGN_CENTER)
        label_titulo.SetForegroundColour(wx.WHITE)
        label_titulo.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        btn_play = wx.Button(self, label="iniciar", size=(160, 35))
        btn_play.SetBackgroundColour(color_verde)
        btn_play.SetForegroundColour(color_texto_boton)
        btn_play.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn_play.Bind(wx.EVT_BUTTON, self.on_play_click)
        
        label_tiempo = wx.StaticText(self, label="Elegi el tiempo para terminar", style=wx.ALIGN_CENTER)
        label_tiempo.SetForegroundColour(wx.WHITE)
        label_tiempo.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Combo selector de tiempo
        opciones_c = ["1 Minuto", "3 Minutos", "5 Minutos", "Sin Límite"]
        self.selector_tiempo = wx.Choice(self, choices=opciones_c, size=(160, 35))
        self.selector_tiempo.SetSelection(1)
        self.selector_tiempo.SetBackgroundColour(color_verde)
        self.selector_tiempo.SetForegroundColour(color_texto_boton)
        
        # Botones de marcador estáticos (truco manual)
        self.btn_victorias = wx.Button(self, label="Victorias: 0", size=(160, 35))
        self.btn_victorias.SetBackgroundColour(color_verde)
        self.btn_victorias.SetForegroundColour(color_texto_boton)
        
        self.btn_derrotas = wx.Button(self, label="Derrotas: 0", size=(160, 35))
        self.btn_derrotas.SetBackgroundColour(color_verde)
        self.btn_derrotas.SetForegroundColour(color_texto_boton)
        
        # Armado secuencial del sizer
        sizer_principal.AddStretchSpacer(1)
        sizer_principal.Add(label_titulo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        sizer_principal.Add(btn_play, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        sizer_principal.Add(label_tiempo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
        sizer_principal.Add(self.selector_tiempo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 35)
        sizer_principal.Add(self.btn_victorias, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sizer_principal.Add(self.btn_derrotas, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        sizer_principal.AddStretchSpacer(1)
        
        self.SetSizer(sizer_principal)

    def actualizar_puntuacion_ui(self, v, d):
        self.btn_victorias.SetLabel("Victorias: " + str(v))
        self.btn_derrotas.SetLabel("Derrotas: " + str(d))

    def on_play_click(self, event):
        idx = self.selector_tiempo.GetSelection()
        segundos_map = [60, 180, 300, None]
        t_final = segundos_map[idx]
        self.on_play_callback(t_final)