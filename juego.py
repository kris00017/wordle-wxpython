# juego.py
import wx
import json
import os
import wx.adv
from wx.lib.wordwrap import wordwrap
from config import ARCHIVO_STATS

# Importar ReportLab de forma segura
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Importaciones explícitas de los archivos de tu amigo
import menu_inicio
import tablero_juego

class WordleAppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Wordle", size=(420, 660))
        self.SetMinSize((420, 660))
        
        # Variables de puntuación
        self.victorias = 0
        self.derrotas = 0
        self.cargar_estadisticas_manual()
        
        self.ultimo_tiempo_seleccionado = None
        self.contenedor_principal = wx.BoxSizer(wx.VERTICAL)
        
        # Inicialización de paneles apuntando a las librerías de tu amigo
        self.panel_menu = menu_inicio.MenuPanel(self, self.mostrar_pantalla_juego)
        self.panel_juego = tablero_juego.JuegoPanel(self, self.mostrar_pantalla_menu, self.procesar_resultado)
        
        self.contenedor_principal.Add(self.panel_menu, 1, wx.EXPAND)
        self.contenedor_principal.Add(self.panel_juego, 1, wx.EXPAND)
        
        self.panel_juego.Hide()
        self.panel_menu.actualizar_puntuacion_ui(self.victorias, self.derrotas)
        
        self.SetSizer(self.contenedor_principal)
        
        # CONFIGURAR LA BARRA DE MENÚS (Tu asignación)
        self.InitMenuBar()
        
        self.Center()

    def InitMenuBar(self):
        """Crea y acopla la barra de menús requerida"""
        menubar = wx.MenuBar()

        menu_archivo = wx.Menu()
        menu_ayuda = wx.Menu()

        # Items de menú con atajos de teclado estándar
        self.item_guardar_pdf = menu_archivo.Append(wx.ID_SAVEAS, "&Guardar partida como PDF\tCtrl+S", "Exportar la partida a PDF")
        item_salir = menu_archivo.Append(wx.ID_EXIT, "&Salir\tCtrl+Q", "Cerrar el juego")
        
        item_about = menu_ayuda.Append(wx.ID_ABOUT, "&Acerca de Wordle...\tF1", "Información del proyecto")

        menubar.Append(menu_archivo, "&Archivo")
        menubar.Append(menu_ayuda, "&Ayuda")
        self.SetMenuBar(menubar)

        # Enlazar los clics de los menús a tus funciones
        self.Bind(wx.EVT_MENU, self.OnGuardarPDF, self.item_guardar_pdf)
        self.Bind(wx.EVT_MENU, self.OnSalir, item_salir)
        self.Bind(wx.EVT_MENU, self.OnAbout, item_about)
        
        # Empezar desactivado porque no hay ninguna partida activa en el menú de inicio
        self.item_guardar_pdf.Enable(False)

    # --- TUS NUEVAS FUNCIONES ---

    def OnSalir(self, event):
        self.Close()

    def OnAbout(self, event):
        """Muestra el cuadro de diálogo About adaptando el código de wxdemo"""
        info = wx.adv.AboutDialogInfo()
        info.Name = "Wordle Python"
        info.Version = "1.0.0"
        info.Copyright = "(c) 2026 - Desarrollado en Python"
        
        desc = (
            "Este es nuestro proyecto escolar de Wordle desarrollado en Python "
            "utilizando la librería gráfica wxPython.\n\n"
            "Modo de juego: Adivina la palabra oculta de 5 letras en un máximo de "
            "6 intentos controlando tu tiempo de juego."
        )
        info.Description = wordwrap(desc, 380, wx.ClientDC(self))
        info.WebSite = ("https://github.com/kris00017/wordle-wxpython", "Código fuente del proyecto")
        info.Developers = ["Maxi y Maycol"]
        
        wx.adv.AboutBox(info)

    def OnGuardarPDF(self, event):
        """Manejador para el guardado y generación del PDF"""
        if not REPORTLAB_AVAILABLE:
            wx.MessageBox(
                "La librería 'reportlab' no está instalada.\nEjecuta en tu consola: pip install reportlab",
                "Falta Dependencia", wx.OK | wx.ICON_ERROR
            )
            return

        # Validar si hay intentos registrados
        if not self.panel_juego.historial_pdf:
            wx.MessageBox("No hay datos de juego activos en este momento para exportar.", "Aviso", wx.OK | wx.ICON_WARNING)
            return

        with wx.FileDialog(self, "Guardar Historial de Wordle", wildcard="Archivos PDF (*.pdf)|*.pdf",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            path_destino = fileDialog.GetPath()
            try:
                self.GenerarArchivoPDF(path_destino)
                wx.MessageBox(f"¡Partida guardada con éxito!\n\nDestino: {path_destino}", "PDF Generado", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al escribir el PDF:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def GenerarArchivoPDF(self, ruta):
        """Genera el PDF con los datos reales del tablero de tu amigo"""
        doc = SimpleDocTemplate(ruta, pagesize=letter)
        estilos = getSampleStyleSheet()
        
        estilo_titulo = ParagraphStyle(
            'T', parent=estilos['Title'], fontName='Helvetica-Bold', fontSize=22, spaceAfter=15
        )
        estilo_cuerpo = ParagraphStyle(
            'C', parent=estilos['Normal'], fontName='Helvetica', fontSize=12, spaceAfter=8
        )
        estilo_intento = ParagraphStyle(
            'I', parent=estilos['Code'], fontName='Courier', fontSize=14, leftIndent=20, spaceAfter=6
        )

        historia = []
        historia.append(Paragraph("Reporte de Juego: Wordle", estilo_titulo))
        historia.append(Spacer(1, 10))
        historia.append(Paragraph(f"<b>Palabra Secreta:</b> {self.panel_juego.palabra_oculta}", estilo_cuerpo))
        historia.append(Paragraph(f"<b>Intentos Empleados:</b> {len(self.panel_juego.historial_pdf)} de 6", estilo_cuerpo))
        historia.append(Spacer(1, 10))
        historia.append(Paragraph("<b>Progreso de la partida:</b>", estilo_cuerpo))
        historia.append(Spacer(1, 5))

        for idx, item in enumerate(self.panel_juego.historial_pdf, 1):
            historia.append(Paragraph(f"Intento {idx}: {item}", estilo_intento))

        doc.build(historia)

    # --- LÓGICA DE CONTROL DE PANTALLAS (CÓDIGO ORIGINAL DE TU AMIGO MODIFICADO) ---

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
        
        # ACTIVAR la opción de PDF si el jugador ya está jugando
        self.item_guardar_pdf.Enable(True)
        
        self.Layout()
        self.panel_juego.SetFocus()

    def mostrar_pantalla_menu(self):
        self.panel_juego.Hide()
        self.panel_menu.Show()
        
        # DESACTIVAR la opción del PDF si vuelve al menú principal
        self.item_guardar_pdf.Enable(False)
        
        self.Layout()
