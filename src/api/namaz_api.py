import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from threading import Thread
import time,os
from src.core.config import namazVaktiProConfig
from fake_useragent import UserAgent

class NamazVaktiAPI:
    def __init__(self):
        self.vakitler = {}
        
        self._istek = requests.Session()
        self._istek.headers = {
            "User-Agent": UserAgent().random,
            "Connection": "keep-alive",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding":"gzip, deflate, br, zstd"
        }
        
    sehirUrl = "https://namazvakitleri.diyanet.gov.tr/tr-TR/home/GetRegList?ChangeType=country&CountryId=2&Culture=tr-TR"
    ilceUrl = "https://namazvakitleri.diyanet.gov.tr/tr-TR/home/GetRegList?ChangeType=state&CountryId=2&Culture=tr-TR&StateId="
    baseUrl = "https://namazvakitleri.diyanet.gov.tr"
    rastgeleAyetHadisUrl = "https://www.diyanethaber.com.tr/istanbul-namaz-vakitleri"
    
    def mevcutVakit(self):
        if not self.vakitler:
            return "Şehir Ayarlanmadı"
        
        su_an = datetime.now().strftime("%H:%M:%S")
        
        sonraki_imsak = self.bsDiyanet.find("table",attrs={"class":"vakit-table"}).find_all("tr")[2].find_all("td")[2].text.strip()
        
        print(sonraki_imsak)
        
        def strp(vakit):
            if len(vakit.split(":")) == 2: vakit += ":00"

            return datetime.strptime(vakit, "%H:%M:%S")
        
        if self.vakitler["İmsak"] <= su_an <= self.vakitler["Sabah"]:
            return {
                "vakit":"İmsak",
                "kalanSure":str(strp(self.vakitler["Sabah"]) - strp(su_an))
            }

        elif self.vakitler["Sabah"] <= su_an <= self.vakitler["Öğle"]:
            return {
                "vakit":"Sabah",
                "kalanSure":str(strp(self.vakitler["Öğle"]) - strp(su_an))
            }

        elif self.vakitler["Öğle"] <= su_an <= self.vakitler["İkindi"]:
            return {
                "vakit":"Öğle",
                "kalanSure":str(strp(self.vakitler["İkindi"]) - strp(su_an))
            }

        elif self.vakitler["İkindi"] <= su_an <= self.vakitler["Akşam"]:            
            return {
                "vakit":"İkindi",
                "kalanSure":str(strp(self.vakitler["Akşam"]) - strp(su_an))
            }

        elif self.vakitler["Akşam"] <= su_an <= self.vakitler["Yatsı"]:
            return {
                "vakit":"Akşam",
                "kalanSure":str(strp(self.vakitler["Yatsı"]) - strp(su_an))
            }

        else:
            return {
                "vakit":"Yatsı",
                "kalanSure":str(strp(sonraki_imsak) - strp(su_an))
            }
    
    def asenkronKalanSure(self,callback):
        def guncelle():
            while True:
                callback(self.mevcutVakit()["kalanSure"])
                time.sleep(1)
        
        Thread(target=guncelle, daemon=True).start()

    
    def getirSehir(self):
        self.sehirList = []
        r = self._istek.get(self.sehirUrl, timeout=10).json()["StateList"]

        for i in r:
            self.sehirList.append({
                "ad": i["SehirAdi"].lower(),
                "id": i["SehirID"]
            })
            
        return self.sehirList
    
    def getirIlce(self, sehir):
        sehir = sehir.lower()
        
        sehirGetir = self.getirSehir()
        
        for i in sehirGetir:
            if i["ad"] == sehir:
                self.sehirNo = i["id"]
                break
        
        self.ilceList = []

        r = self._istek.get(self.ilceUrl + str(self.sehirNo),timeout=10).json()["StateRegionList"]
        
        for i in r:
            self.ilceList.append({
                "ad": i["IlceAdi"].lower(),
                "url": i["IlceUrl"]
            })
            
        return self.ilceList
    
    def getirVakit(self):
        
        self.il = namazVaktiProConfig()["il"]
        self.ilce = namazVaktiProConfig()["ilce"]
        
        ilceGetir = self.getirIlce(self.il.lower())
        for i in ilceGetir:
            if i["ad"] == self.ilce.lower():
                self.ilceUrlAdi = i["url"]
                break
        
        r = self._istek.get(self.baseUrl + self.ilceUrlAdi,timeout=10).text
        
        self.bsDiyanet = BeautifulSoup(r, "html.parser")

        vakitler = self.bsDiyanet.find("div", {"class": "today-pray-times"})
        
        def vakitBul(vakitAdi):
            return vakitler.find("div", {"data-vakit-name": vakitAdi}).text.split("\n")[2]
        
        vakitJson = {
            "İmsak":vakitBul("imsak"),
            "Sabah":vakitBul("gunes"),
            "Öğle":vakitBul("ogle"),
            "İkindi":vakitBul("ikindi"),
            "Akşam":vakitBul("aksam"),
            "Yatsı":vakitBul("yatsi")
        }
        
        self.vakitler = vakitJson

        return vakitJson
    
    def rastgeleAyet_Hadis(self):
        r = requests.get(self.rastgeleAyetHadisUrl,timeout=10).text
        
        b = BeautifulSoup(r, "html.parser")
        veri = b.find("div", {"class": "hadith"}).text.strip()
        
        return veri
