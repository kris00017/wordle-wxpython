# main.py
import wx
import os
import sys
import wx.lib.agw.advancedsplash as AS

# Configuración dinámica simplificada de directorios
dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

class WordleAdvancedSplash(AS.AdvancedSplash):
    def __init__(self, splash_image_path):
        es_png = ".png" in splash_image_path.lower()
        tipo_bitmap = wx.BITMAP_TYPE_PNG if es_png else wx.BITMAP_TYPE_JPEG

        if os.path.exists(splash_image_path) == False:
            # Fallback en caso de pérdida de recurso
            bitmap = wx.Bitmap(415, 231)
            dc = wx.MemoryDC(bitmap)
            dc.SetBackground(wx.Brush(wx.Colour(247, 247, 247)))
            dc.Clear()
            dc.SetTextForeground(wx.Colour(106, 170, 100)) 
            dc.DrawText("WORDLE", 140, 70)
            dc.SelectObject(wx.NullBitmap)
        else:
            bitmap = wx.Bitmap(splash_image_path, tipo_bitmap)
            
        super().__init__(None, bitmap=bitmap, timeout=2500,
                         agwStyle=AS.AS_TIMEOUT | AS.AS_CENTER_ON_SCREEN | AS.AS_SHADOW_BITMAP,
                         shadowcolour=wx.Colour(40, 40, 40))
        
        self.Bind(wx.EVT_CLOSE, self.al_cerrar_splash)

    def al_cerrar_splash(self, event):
        import juego
        main_frame = juego.WordleAppFrame()
        main_frame.Show()
        event.Skip()

if __name__ == '__main__':
    aplicacion_wx = wx.App(redirect=False) 
    
    archivo_splash = os.path.join(dirName, "wordle-splash.png")
    if not os.path.exists(archivo_splash):
        archivo_splash = os.path.join(dirName, "bitmaps", "wordle-splash.png")
        
    obj_splash = WordleAdvancedSplash(archivo_splash)
    obj_splash.Show()
    aplicacion_wx.MainLoop()