# juego.py
import wx
import json
import os
from config import ARCHIVO_STATS

# Importaciones explícitas de tus nuevos nombres de archivo modificados
import menu_inicio
import tablero_juego

class WordleAppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Wordle", size=(420, 660))
        self.SetMinSize((420, 660))
        
        # Lectura tradicional de variables sin destructuración avanzada
        self.victorias = 0
        self.derrotas = 0
        self.cargar_estadisticas_manual()
        
        self.ultimo_tiempo_seleccionado = None
        self.contenedor_principal = wx.BoxSizer(wx.VERTICAL)
        
        # Inicialización de paneles apuntando a las nuevas librerías
        self.panel_menu = menu_inicio.MenuPanel(self, self.mostrar_pantalla_juego)
        self.panel_juego = tablero_juego.JuegoPanel(self, self.mostrar_pantalla_menu, self.procesar_resultado)
        
        self.contenedor_principal.Add(self.panel_menu, 1, wx.EXPAND)
        self.contenedor_principal.Add(self.panel_juego, 1, wx.EXPAND)
        
        self.panel_juego.Hide()
        self.panel_menu.actualizar_puntuacion_ui(self.victorias, self.derrotas)
        
        self.SetSizer(self.contenedor_principal)
        self.Center()

    def cargar_estadisticas_manual(self):
        if os.path.exists(ARCHIVO_STATS):
            try:
                archivo = open(ARCHIVO_STATS, "r")
                datos_dict = json.load(archivo)
                self.victorias = datos_dict["victorias"]
                self.derrotas = datos_dict["derrotas"]
                archivo.close()
            except:
                self.victorias = 0
                self.derrotas = 0

    def procesar_resultado(self, ganado):
        if flag_ganado := ganado:
            self.victorias = self.victorias + 1
        else:
            self.derrotas = self.derrotas + 1
        
        # Guardar estadísticas a archivo plano
        datos_guardar = {"victorias": self.victorias, "derrotas": self.derrotas}
        try:
            with open(ARCHIVO_STATS, "w") as f_out:
                f_out.write(json.dumps(datos_guardar, indent=4))
        except:
            print("Error guardando datos de puntuacion.")
            
        self.panel_menu.actualizar_puntuacion_ui(self.victorias, self.derrotas)

    def mostrar_pantalla_juego(self, tiempo_segundos):
        self.ultimo_tiempo_seleccionado = tiempo_segundos
        self.panel_menu.Hide()
        self.panel_juego.Show()
        self.panel_juego.iniciar_juego(tiempo_segundos)
        self.Layout()
        self.panel_juego.SetFocus()

    def mostrar_pantalla_menu(self):
        self.panel_juego.Hide()
        self.panel_menu.Show()
        self.Layout()