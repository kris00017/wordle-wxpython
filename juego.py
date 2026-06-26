import wx
import json
import os
from config import ARCHIVO_STATS
from menu_panel import MenuPanel
from juego_panel import JuegoPanel

class WordleAppFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Wordle", size=(420, 660))
        self.SetMinSize((420, 660))
        
        self.victorias, self.derrotas = self.cargar_estadisticas()
        self.ultimo_tiempo_seleccionado = None
        
        self.contenedor_principal = wx.BoxSizer(wx.VERTICAL)
        
        self.panel_menu = MenuPanel(self, self.mostrar_pantalla_juego)
        self.panel_juego = JuegoPanel(self, self.mostrar_pantalla_menu, self.procesar_resultado)
        
        self.contenedor_principal.Add(self.panel_menu, 1, wx.EXPAND)
        self.contenedor_principal.Add(self.panel_juego, 1, wx.EXPAND)
        
        self.panel_juego.Hide()
        self.panel_menu.actualizar_puntuacion_ui(self.victorias, self.derrotas)
        
        self.SetSizer(self.contenedor_principal)
        self.Center()

    def cargar_estadisticas(self):
        if os.path.exists(ARCHIVO_STATS):
            try:
                with open(ARCHIVO_STATS, "r") as f:
                    datos = json.load(f)
                    return datos.get("victorias", 0), datos.get("derrotas", 0)
            except (json.JSONDecodeError, IOError):
                return 0, 0
        return 0, 0

    def guardar_estadisticas(self):
        datos = {"victorias": self.victorias, "derrotas": self.derrotas}
        try:
            with open(ARCHIVO_STATS, "w") as f:
                json.dump(datos, f, indent=4)
        except IOError as e:
            print(f"Error guardando estadísticas: {e}")

    def procesar_resultado(self, ganado):
        if ganado:
            self.victorias += 1
        else:
            self.derrotas += 1
        
        self.guardar_estadisticas()
        self.panel_menu.actualizar_puntuacion_ui(self.victorias, self.derrotas)

    def mostrar_pantalla_juego(self, tiempo_segundos):
        self.ultimo_tiempo_seleccionado = tiempo_segundos
        self.panel_menu.Hide()
        self.panel_juego.Show()
        self.panel_juego.iniciar_partida(tiempo_segundos)
        self.Layout()
        self.panel_juego.SetFocus()

    def mostrar_pantalla_menu(self):
        self.panel_juego.Hide()
        self.panel_menu.Show()
        self.Layout()