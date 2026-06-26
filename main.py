import wx
import os
import sys

# Intentar importar AdvancedSplash desde la librería de wxPython
try:
    from agw import advancedsplash as AS
except ImportError: 
    import wx.lib.agw.advancedsplash as AS

# Configuración de directorios de manera dinámica
dirName = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.path.dirname(os.path.abspath(sys.argv[0]))
bitmapDir = os.path.join(dirName, 'bitmaps')

class WordleAdvancedSplash(AS.AdvancedSplash):
    def __init__(self, splash_image_path):
        # Detectar el formato correcto según la extensión del archivo
        es_png = splash_image_path.lower().endswith('.png')
        tipo_bitmap = wx.BITMAP_TYPE_PNG if es_png else wx.BITMAP_TYPE_JPEG

        # Cargar la imagen o usar el respaldo si no se encuentra
        if not os.path.exists(splash_image_path):
            bitmap = self.crear_bitmap_auxiliar()
        else:
            bitmap = wx.Bitmap(splash_image_path, tipo_bitmap)
            
        # Color de la sombra (gris oscuro para dar profundidad sobre el fondo de pantalla)
        shadow_color = wx.Colour(40, 40, 40) 

        # Inicialización del Splash Screen centrado en la pantalla (resolución 823x468 o la que tenga tu imagen)
        super().__init__(None, bitmap=bitmap, timeout=3500, # 3.5 segundos en pantalla
                         agwStyle=AS.AS_TIMEOUT | AS.AS_CENTER_ON_SCREEN | AS.AS_SHADOW_BITMAP,
                         shadowcolour=shadow_color)
        
        self.Bind(wx.EVT_CLOSE, self.OnCloseSplash)

    def OnCloseSplash(self, event):
        """Se ejecuta al cerrarse el Splash por timeout o por hacer click."""
        try:
            # Importamos el archivo independiente del juego y lanzamos su interfaz principal
            import juego
            main_game = juego.WordleAppFrame()
            main_game.Show()
        except ImportError:
            wx.MessageBox("No se pudo encontrar el archivo 'juego.py' en el mismo directorio.", 
                          "Error de carga", wx.OK | wx.ICON_ERROR)
        
        event.Skip()

    def crear_bitmap_auxiliar(self):
        """Genera un bitmap plano si el archivo original se pierde."""
        bmp = wx.Bitmap(415, 231)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(wx.Colour(247, 247, 247)))
        dc.Clear()
        
        dc.SetTextForeground(wx.Colour(106, 170, 100)) 
        dc.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.DrawText("WORDLE", 140, 70)
        
        dc.SetTextForeground(wx.Colour(120, 124, 126))
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        dc.DrawText("Falta la imagen del splash", 130, 130)
        
        dc.SelectObject(wx.NullBitmap)
        return bmp

if __name__ == '__main__':
    app = wx.App(redirect=False) 
    
    # Busca la imagen PNG de manera prioritaria, si no, busca la JPG
    splash_file = "wordle-splash.png"
    splash_path = os.path.normpath(os.path.join(dirName, splash_file))
    
    if not os.path.exists(splash_path):
        splash_file = "wordle-splash.jpg"
        splash_path = os.path.normpath(os.path.join(dirName, splash_file))
        
    # Si las tienes organizadas dentro de una carpeta /bitmaps
    if not os.path.exists(splash_path):
        splash_path = os.path.normpath(os.path.join(bitmapDir, splash_file))
        
    splash = WordleAdvancedSplash(splash_path)
    splash.Show()
    app.MainLoop()