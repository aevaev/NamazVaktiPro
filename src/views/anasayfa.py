from customtkinter import CTkFrame, CTkLabel, CTkButton
from src.views.bildirim import Bildirim
from src.views.widgets import Widgets
from src.core.config import namazVaktiProConfig, configDegistir
import time

class AnaSayfa(CTkFrame,Widgets):
    def __init__(self, master,namaz,zaman, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.namaz = namaz
        self.zaman = zaman
        
        self.namazvakti = self.namaz.getirVakit()
        self.vakit_labels = {}

        self.columnconfigure([0,1], weight=1)

        self.icerik()

        self.zaman.asenkronSaat(self.saatiGuncelle)
        self.namaz.asenkronKalanSure(self.kalanSureGuncelle)

    def icerik(self):
        
        tarihFrame = self.frameGFX()
        tarihFrame.grid(row=0, column=0, sticky="we",padx=(0,2),pady=(0,10))
        tarihFrame.columnconfigure(0, weight=1)
        
        mevcutTarihText = self.labelGFX(tarihFrame, "Tarih",font=2)
        mevcutTarihText.grid(row=0, column=0,sticky="w",padx=(10,0), pady=5)
        
        self.mevcutTarih = self.labelGFX(tarihFrame, self.zaman.tarih(),2, font=2)
        self.mevcutTarih.grid(row=0, column=2,sticky="w",padx=(0,10), pady=5)


        saatFrame = self.frameGFX()
        saatFrame.grid(row=0, column=1, sticky="we",padx=(2,0),pady=(0,10))
        saatFrame.columnconfigure(0, weight=1)

        saatText = self.labelGFX(saatFrame, "Saat",font=2)
        saatText.grid(row=0, column=0, sticky="w", padx=(10,0), pady=5)
        
        self.saatGoster = self.labelGFX(saatFrame, self.zaman.saat(),2, font=2)
        self.saatGoster.grid(row=0, column=2,sticky="w",padx=(0,10), pady=5)

        mevcutVakitFrame = self.frameGFX()
        mevcutVakitFrame.grid(row=1, column=0, sticky="we",padx=(0,2),pady=(0,5))

        kalanVakitFrame = self.frameGFX()
        kalanVakitFrame.grid(row=1, column=1, sticky="we",padx=(2,0),pady=(0,5))
        
        mevcutVakitFrame.grid_columnconfigure(0, weight=1)
        kalanVakitFrame.grid_columnconfigure(0, weight=1)

        mevcutVakitText = self.labelGFX(mevcutVakitFrame, "Mevcut Vakit",font=2)
        mevcutVakitText.grid(row=0, column=0,sticky="w",padx=(10,0), pady=5)
        
        self.mevcutVakit = self.labelGFX(mevcutVakitFrame, self.namaz.mevcutVakit().get("vakit"),2 , font=2)
        self.mevcutVakit.grid(row=0, column=2,sticky="w",padx=(0,10), pady=5)
        

        kalanVakitText = self.labelGFX(kalanVakitFrame, "Kalan Vakit",font=2)
        kalanVakitText.grid(row=0, column=0, sticky="w", padx=(10,0), pady=5)
        
        self.kalanVakit = self.labelGFX(kalanVakitFrame, self.namaz.mevcutVakit()["kalanSure"], 2, font=2)
        self.kalanVakit.grid(row=0, column=2,sticky="w",padx=(0,10), pady=5)
        
        vakitFrame =self.frameGFX()
        vakitFrame.grid(row=2, column=0,columnspan=2, sticky="we",pady=(5,10))
        
        vakitFrame.grid_columnconfigure([0,1],weight=1)
        
        vakitText = self.labelGFX(vakitFrame, "Vakitler",font=2)
        vakitText.grid(row=0, column=0,columnspan=2, padx=5, pady=5)
        
        for index,i in enumerate(self.namazvakti,3):

            vakitAdi = self.frameGFX()
            vakitAdi.grid(row=index+1, column=0,columnspan=2, sticky="we", padx=5, pady=10)
            vakitAdi.grid_columnconfigure([0,1,2,3],weight=1)
            
            vakitAdı = self.labelGFX(vakitAdi, i, font=2)
            vakitAdı.grid(row=index+1, column=1, sticky="w", padx=10, pady=5)
            
            if i == self.namaz.mevcutVakit()["vakit"]:
                vakitAdi.configure(fg_color="#29166B")
            
            self.vakit_labels[i] = vakitAdi
            
            vakitSaat = self.labelGFX(vakitAdi, self.namazvakti[i], 2, font=2)
            vakitSaat.grid(row=index+1, column=2, sticky="e", padx=10, pady=5)
        
        self.bildirim = self.frameGFX()
        self.bildirim.grid(row=10,column=0,columnspan=2)
        
        self.bildirimButon = CTkButton(
            self.bildirim,
            text="Test Bildirimi",
            command=lambda:Bildirim(
                self,
                {
                    "vakitSaat":self.namaz.mevcutVakit()["kalanSure"],
                    "saat":self.zaman.saat(False),
                    "vakit":self.namaz.mevcutVakit().get("vakit"),
                    "sonrakiVakit":self.namazvakti[self.vakitAdi]
                }
            )
        )

        self.bildirimButon.grid(row=0,column=0)
        
    def saatiGuncelle(self,text):
        self.saatGoster.configure(text=text)
        
        if self.namaz.mevcutVakit()["kalanSure"] == "0:00:00":
            self.mevcutTarih.configure(text=self.zaman.tarih())

    def kalanSureGuncelle(self,text):
        self.kalanVakit.configure(text=text)
        
        self.kalanSure = self.namaz.mevcutVakit()["kalanSure"]

        self.sonraki = list(self.namazvakti.keys()).index(self.namaz.mevcutVakit().get("vakit")) + 1
        
        try:
            self.vakitAdi = list(self.namazvakti.keys())[self.sonraki]
        except IndexError:
            self.vakitAdi = list(self.namazvakti.keys())[0]
        
        if self.kalanSure == "0:00:01":
            self.mevcutVakit.configure(text=self.vakitAdi)
            
            self.vakit_labels[self.namaz.mevcutVakit().get("vakit")].configure(fg_color="transparent")
            self.vakit_labels[self.vakitAdi].configure(fg_color="#29166B")

        if self.kalanSure == "2:00:00" or self.kalanSure == "1:00:00" or self.kalanSure == "0:30:00" or self.kalanSure == "0:15:00" or self.kalanSure == "0:00:01":
            sureJson = {#örnek
                "vakitSaat":"1 Saat",
                "saat":"13.00",
                "vakit":"Öğle",
                "sonrakiVakit":"17.00"
            }
            
            if not namazVaktiProConfig()["bildirim"]:
                if self.kalanSure == "0:00:01":
                    configDegistir(bildirim=True)
                else:
                    return

            # if self.namaz.mevcutVakit().get("vakit") == "Sabah" and self.kalanSure != "0:00:01":return
            
            if "2:" in self.kalanSure:
                sureJson["vakitSaat"] = "2 Saat"
            elif "1:" in self.kalanSure:
                sureJson["vakitSaat"] = "1 Saat"
            elif "30" in self.kalanSure:
                sureJson["vakitSaat"] = "30 Dakika"
            elif "15" in self.kalanSure:
                sureJson["vakitSaat"] = "15 Dakika"
            elif ":01" in self.kalanSure:
                sureJson["vakitSaat"] = "vakit"
                
            sureJson["vakit"] = self.namaz.mevcutVakit().get("vakit")
            sureJson["saat"] = self.zaman.saat(False)
            sureJson["sonrakiVakit"] = self.namazvakti[self.vakitAdi]
            sureJson["sonrakiVakitAdi"] = self.vakitAdi
            
            Bildirim(
                self,
                sureJson
            )