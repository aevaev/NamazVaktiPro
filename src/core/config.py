import os
import json
import tempfile

config_path = os.path.join(tempfile.gettempdir(), "namazVaktiPro.json")

config = {
    "il": "İstanbul",
    "ilce": "İstanbul",
    "bildirim":True,
}


def namazVaktiProConfig():
    
    if not os.path.exists(config_path):configDegistir()

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def configDegistir(
    il="boş",
    ilce="boş",
    bildirim=False,
):

    if il == "boş":
        il = namazVaktiProConfig()["il"]
    if ilce == "boş":
        ilce = namazVaktiProConfig()["ilce"]
    
    config["il"] = il
    config["ilce"] = ilce
    config["bildirim"] = bildirim

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

if not os.path.exists(config_path):configDegistir("i̇stanbul","i̇stanbul")
