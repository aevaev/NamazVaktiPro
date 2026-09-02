from customtkinter import CTkFrame, CTkOptionMenu
from src.views.widgets import Widgets
from src.core.config import namazVaktiProConfig,configDegistir
from src.api.namaz_api import NamazVaktiAPI

from tkinter import StringVar

class Ayarlar(CTkFrame,Widgets,NamazVaktiAPI):
    def __init__(self, master):
        CTkFrame.__init__(self, master, fg_color="transparent")
        NamazVaktiAPI.__init__(self)

        self.columnconfigure([0,1,2], weight=1)
        
        self.icerik()

    def icerik(self):
        self.labelGFX(self, "Ayarlar").grid(row=0, column=1,pady=10)
        
        self.il_ilceSec = self.frameGFX()
        self.il_ilceSec.grid(row=1, column=0, columnspan=3)
    
        def ilceGetir(value):
            self.ilceler = [i["ad"] for i in self.getirIlce(value)]
            self.ilce.configure(values=self.ilceler)
            
        self.iller = [i["ad"] for i in self.getirSehir()]
        self.il_baslangic = namazVaktiProConfig()["il"]
        self.ilceler = [i["ad"] for i in self.getirIlce(self.il_baslangic)]
        
        self.il = CTkOptionMenu(
            self.il_ilceSec,
            values=self.iller,
            variable=StringVar(value=self.il_baslangic),
            command=ilceGetir
        )
        self.il.grid(row=0, column=0, padx=10, pady=10)
        
        self.ilce = CTkOptionMenu(
            self.il_ilceSec,
            values=self.ilceler,
            variable=StringVar(value=namazVaktiProConfig()["ilce"])
        )
        self.ilce.grid(row=1, column=0, padx=10, pady=10)
        
        self.kaydet = self.buttonGFX(
            self,
            "Kaydet",
            command=lambda:configDegistir(
                self.il.get(),
                self.ilce.get()
            )
        )
        self.kaydet.grid(row=2, column=1, padx=10, pady=10)