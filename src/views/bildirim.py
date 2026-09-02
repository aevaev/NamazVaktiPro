import customtkinter as ctk
from customtkinter import CTkToplevel, CTkFrame
from src.views.widgets import Widgets
from src.core.config import configDegistir
from src.api.namaz_api import NamazVaktiAPI
import random

class Bildirim(CTkToplevel,Widgets):

    def __init__(self, parent,kalanZaman=False):
        super().__init__(parent)
        
        self.kalanZaman = kalanZaman
        self.namaz = NamazVaktiAPI()
        
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#29166B")

        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.icerik()

    def icerik(self):
        
        self.baslikFrame = self.frameGFX("","transparent")
        self.baslikFrame.grid(row=0,column=0,columnspan=4,sticky="we")
        self.baslikFrame.grid_columnconfigure((0,1,2,3), weight=1)
        

        self.baslik = self.labelGFX(
            self.baslikFrame,
            "وَالْحَمْدُ لِلّٰهِ رَبِّ الْعَالَم۪ينَ",
            font=3
        )
        
        self.baslik.grid(row=0,column=0,columnspan=4,pady=10)
        
        hr = self.hr(self.baslikFrame)
        hr.grid(row=1,column=0,columnspan=4,sticky="we")
        
        self.taslak = self.frameGFX("","transparent")
        self.taslak.grid(row=1,column=0,columnspan=4,sticky="n")
        self.taslak.grid_columnconfigure((0,1,2,3), weight=1)
        
        if self.kalanZaman["vakitSaat"] == "vakit":
            self.labelGFX(
                self.taslak,
                self.kalanZaman['sonrakiVakitAdi'],
                "#90A70E",
                font=('Times New Roman', 50)
            ).grid(row=0,column=0,columnspan=4,pady=10)

            self.labelGFX(
                self.taslak,
                "Vakti Girdi",
                font=('Times New Roman', 50)
            ).grid(row=1,column=0,columnspan=4,pady=10)
        else:
            self.labelGFX(
                self.taslak,
                self.kalanZaman['vakit'],
                "#90A70E",
                font=('Times New Roman', 50)
            ).grid(row=0,column=0,columnspan=4,pady=10)

            self.labelGFX(
                self.taslak,
                "Vaktinin Bitmesine Kalan Süre",
                font=('Times New Roman', 50)
            ).grid(row=1,column=0,columnspan=4,pady=10)
            
            self.labelGFX(
                self.taslak,
                self.kalanZaman['vakitSaat'],
                "#90A70E",
                font=('Times New Roman', 50)
                ).grid(row=2,column=0,columnspan=4,pady=10)
        
        self.ekBilgi = self.frameGFX("","transparent")
        self.ekBilgi.grid(row=2,column=0,columnspan=4,sticky="we")
        self.ekBilgi.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.labelGFX(
            self.ekBilgi,
            f"Saat: {self.kalanZaman['saat']}",
            font=('Times New Roman', 50)
        ).grid(row=0,column=0,columnspan=2,pady=10)
        
        self.labelGFX(
            self.ekBilgi,
            f"Sonraki Vakit: {self.kalanZaman['sonrakiVakit']}",
            font=('Times New Roman', 50)
        ).grid(row=0,column=2,columnspan=4,padx=10)
        
        self.namazDurum = self.frameGFX("","transparent")
        self.namazDurum.grid(row=3,column=0,columnspan=4,sticky="we")
        self.namazDurum.grid_columnconfigure((0,1,2,3,4), weight=1)
        
        self.buttonGFX(
            self.namazDurum,
            "Namazı Kıl / Kıldım",
            self.namazKil
        ).grid(row=0,column=2,sticky="w",ipadx=10,ipady=10)

        self.buttonGFX(
            self.namazDurum,
            "Namazı Ertele",
            self.namazErtele
        ).grid(row=0,column=2,sticky="e",ipadx=10,ipady=10)

    def bildirimDialog(self,tus=False):
        
        for widget in list(self.children.values()):
            widget.destroy()
        
        if tus:
            configDegistir(bildirim=False)
            
        veri = self.namaz.rastgeleAyet_Hadis().split()
        if len(veri) > 10:
            for i in range(0,len(veri),10):
                veri.insert(i,"\n")
        
        veri = " ".join(veri)

        self.labelGFX(
            self,
            f"{veri}",
            text_color="#FFFFFF",
            font=("Segoe UI", 20, "bold")
        ).grid(row=1,column=0,columnspan=4,pady=10)

        self.bind("<Button-1>", lambda event: self.destroy())
        return

    def namazKil(self):
        self.bildirimDialog(True)

    def namazErtele(self):
        self.bildirimDialog(False)