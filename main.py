import tkinter as tk
from tkinter import messagebox
import os
import threading
import requests
import time
import psutil
from PIL import Image, ImageTk
import subprocess
import webbrowser
from dotenv import load_dotenv
import locale

# .env dosyasını yükle
load_dotenv()

try:
    locale.setlocale(locale.LC_ALL, '')
    sys_locale = locale.getlocale()[0]
except Exception:
    sys_locale = os.environ.get("LANG", "en")

if not sys_locale:
    sys_locale = "en"

if "tr" in sys_locale.lower():
    LANG = "tr"
elif "de" in sys_locale.lower():
    LANG = "de"
elif "palisch" in sys_locale.lower():
    LANG = "palisch"
else:
    LANG = "en"

TRANSLATIONS = {
    "tr": {
        "waiting": "Veri bekleniyor...",
        "secure": "RETREX OS: GÜVENLİ ERİŞİM",
        "connect": "SİSTEME BAĞLAN",
        "error": "HATA",
        "invalid": "Geçersiz Kimlik!",
        "mag": "Şiddet",
        "fail": "Veri alınamadı.",
        "weather": "HAVA: 12°C / Eskişehir",
        "sys": "SİSTEM DURUMU",
        "cpu": "CPU (%)",
        "ram": "RAM (%)",
        "market": "CANLI PİYASA (TRY)",
        "loading": "Yükleniyor...",
        "eq": "SON DEPREM (KANDİLLİ)",
        "user_info": "KULLANICI: {}\nRÜTBE    : {}\nDURUM    : AKTİF\nGÜVENLİK : SEVİYE 5",
        "app": "UYG",
        "ai_msg": "Sistem kararlı, Retrex.",
        "date_format": "TARİH: {0}\nSAAT : {1}",
        "curr": "DOLAR: {0} ₺ | EURO: {1} ₺",
        "menu": "Sistem Menüsü",
        "term": "TERMİNAL",
        "browser": "TARAYICI"
    },
        "palisch": {
        "waiting": "Vewi beqlyeniyow...",
        "secure": "RETREX OS: CÜVENLyİ EWİSchİM",
        "connect": "SchİSchTEME BAĞLyAN",
        "error": "HATA",
        "invalid": "Ceçewschitz Qimlyiq!",
        "mag": "Schiddet",
        "fail": "Vewi alyınamadı.",
        "weather": "HAVA: 12°C / Eschqischehiw",
        "sys": "SchİSchTEM DUWUMU",
        "cpu": "CPU (%)",
        "ram": "RAM (%)",
        "market": "CANLyI PİYASchA (TRY)",
        "loading": "Yüqlyeniyow...",
        "eq": "SchON DEPWEM (QANDİLyLyİ)",
        "user_info": "QULyLyANICI: {}\nWÜTBE    : {}\nDUWUM    : AQTİF\nCÜVENLyİQ : SchEVİYE 5",
        "app": "UYC",
        "ai_msg": "Schischtem qawawlyı, Wetwex.",
        "date_format": "TAWİH: {0}\nSchAAT : {1}",
        "curr": "DOLyAW: {0} ₺ | EUWO: {1} ₺",
        "menu": "Schischtem Menüschü",
        "term": "TEWMİNALy",
        "browser": "TAWAYICI"
    },
    "en": {
        "waiting": "Waiting for data...",
        "secure": "RETREX OS: SECURE ACCESS",
        "connect": "CONNECT TO SYSTEM",
        "error": "ERROR",
        "invalid": "Invalid Identity!",
        "mag": "Magnitude",
        "fail": "Data not received.",
        "weather": "WEATHER: 12°C / Eskisehir",
        "sys": "SYSTEM STATUS",
        "cpu": "CPU (%)",
        "ram": "RAM (%)",
        "market": "LIVE MARKET (TRY)",
        "loading": "Loading...",
        "eq": "LAST EARTHQUAKE (KANDILLI)",
        "user_info": "USER     : {}\nRANK     : {}\nSTATUS   : ACTIVE\nSECURITY : LEVEL 5",
        "app": "APP",
        "ai_msg": "System stable, Retrex.",
        "date_format": "DATE: {0}\nTIME: {1}",
        "curr": "USD: {0} ₺ | EUR: {1} ₺",
        "menu": "System Menu",
        "term": "TERMINAL",
        "browser": "BROWSER"
    },
    "de": {
        "waiting": "Warte auf Daten...",
        "secure": "RETREX OS: SICHERER ZUGANG",
        "connect": "MIT DEM SYSTEM VERBINDEN",
        "error": "FEHLER",
        "invalid": "Ungültige Identität!",
        "mag": "Magnitude",
        "fail": "Daten nicht empfangen.",
        "weather": "WETTER: 12°C / Eskisehir",
        "sys": "SYSTEMSTATUS",
        "cpu": "CPU (%)",
        "ram": "RAM (%)",
        "market": "LIVE MARKT (TRY)",
        "loading": "Lade...",
        "eq": "LETZTE ERDBEBEN (KANDILLI)",
        "user_info": "BENUTZER     : {}\nRANG     : {}\nSTATUS   : AKTIV\nSICHERHEIT : STUFE 5",
        "app": "APP",
        "ai_msg": "System stabil, Retrex.",
        "date_format": "DATUM: {0}\nZEIT : {1}",
        "curr": "USD: {0} ₺ | EUR: {1} ₺",
        "menu": "Systemmenü",
        "term": "TERMINAL",
        "browser": "BROWSER"
    }
}
t = TRANSLATIONS[LANG]

# Sabitler / Ayarlar ( .env dosyasından yüklenir )
PROFILE_IMG_PATH = os.getenv("PROFILE_IMG_PATH", "assets/profile.png")
BG_PATH = os.getenv("BG_PATH", "assets/background.jpg")
SIFRE = os.getenv("SIFRE", "1234")
KULLANICI = os.getenv("KULLANICI", "Retrex User")
RUTBE = os.getenv("RUTBE", "Admin")

class RetrexOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Retrex OS")
        self.geometry("1000x750")
        self.resizable(False, False)
        self.configure(bg="#000")

        self.giris_img = None
        self.bg_img = None
        self.cpu_data = [0] * 50
        self.ram_data = [0] * 50

        self.usd_rate = "..."
        self.eur_rate = "..."
        self.deprem_bilgi = t["waiting"]

        self.giris_ekranini_olustur()

    def giris_ekranini_olustur(self):
        self.login_frame = tk.Frame(self, bg="#000")
        self.login_frame.pack(expand=True, fill="both")

        if os.path.exists(PROFILE_IMG_PATH):
            img = Image.open(PROFILE_IMG_PATH).resize((180, 180), Image.Resampling.LANCZOS)
            self.giris_img = ImageTk.PhotoImage(img)
            tk.Label(self.login_frame, image=self.giris_img, bg="#000").pack(pady=20)

        tk.Label(self.login_frame, text=t["secure"], fg="cyan", bg="#000", font=("Consolas", 18, "bold")).pack()
        self.pass_entry = tk.Entry(self.login_frame, show="*", width=25, justify="center", bg="#111", fg="white", insertbackground="white")
        self.pass_entry.pack(pady=15)
        self.pass_entry.focus_set()

        tk.Button(self.login_frame, text=t["connect"], command=self.giris_kontrol, bg="#00CED1", fg="black", font=("Consolas", 10, "bold"), width=20).pack()

    def giris_kontrol(self):
        if self.pass_entry.get() == SIFRE:
            threading.Thread(target=self.veri_guncelleme_dongusu, daemon=True).start()
            self.dashboard_baslat()
        else:
            messagebox.showerror(t["error"], t["invalid"])

    def veri_guncelleme_dongusu(self):
        while True:
            try:
                # Döviz
                r_usd = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
                self.usd_rate = f"{r_usd.json()['rates']['TRY']:.2f}"
                r_eur = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=5)
                self.eur_rate = f"{r_eur.json()['rates']['TRY']:.2f}"

                # Deprem
                r_deprem = requests.get("https://api.orhanaydogdu.com.tr/deprem/kandilli/live", timeout=5)
                d = r_deprem.json()['result'][0]
                self.deprem_bilgi = f"{d['lokasyon'][:20]}\n{t['mag']}: {d['mag']} | {d['date'][11:16]}"
            except:
                self.deprem_bilgi = t["fail"]
            time.sleep(600)

    def dashboard_baslat(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self, width=1000, height=750, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        if os.path.exists(BG_PATH):
            bg = Image.open(BG_PATH).resize((1000, 750), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(bg)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # Paneller
        self.canvas.create_rectangle(20, 20, 280, 140, fill="#050505", outline="cyan", width=2)
        self.info_label = tk.Label(self, text="", bg="#050505", fg="white", font=("Consolas", 11), justify="left")
        self.canvas.create_window(150, 65, window=self.info_label)
        self.weather_label = tk.Label(self, text=t["weather"], bg="#050505", fg="#FFD700", font=("Consolas", 11, "bold"))
        self.canvas.create_window(150, 115, window=self.weather_label)

        # Sağ Üst: Performans
        self.canvas.create_rectangle(720, 20, 980, 240, fill="#050505", outline="white", width=2)
        self.canvas.create_text(850, 40, text=t["sys"], fill="cyan", font=("Consolas", 10, "bold"))
        self.canvas.create_text(755, 130, text=t["cpu"], fill="cyan", font=("Consolas", 9, "bold"), anchor="w")
        self.canvas.create_text(755, 220, text=t["ram"], fill="#FF4500", font=("Consolas", 9, "bold"), anchor="w")

        # Orta: Döviz ve Deprem Panelleri
        self.canvas.create_rectangle(350, 20, 650, 130, fill="#050505", outline="#00FF00", width=2)
        self.canvas.create_text(500, 35, text=t["market"], fill="#00FF00", font=("Consolas", 10, "bold"))
        self.currency_label = tk.Label(self, text="...", bg="#050505", fg="white", font=("Consolas", 11, "bold"))
        self.canvas.create_window(500, 85, window=self.currency_label)

        self.canvas.create_rectangle(350, 145, 650, 240, fill="#050505", outline="#FF4500", width=2)
        self.canvas.create_text(500, 160, text=t["eq"], fill="#FF4500", font=("Consolas", 9, "bold"))
        self.deprem_label = tk.Label(self, text=t["loading"], bg="#050505", fg="white", font=("Consolas", 8, "bold"))
        self.canvas.create_window(500, 200, window=self.deprem_label)

        # Sol Alt: Bilgiler
        self.canvas.create_rectangle(20, 580, 320, 730, fill="#050505", outline="cyan", width=2)
        kisi_bilgi = t["user_info"].format(KULLANICI, RUTBE)
        self.canvas.create_text(170, 655, text=kisi_bilgi, fill="white", font=("Consolas", 12, "bold"), justify="left")

        # Butonlar
        self.hud_buton(930, 680, t["app"], "#00CED1", self.menu_ac)
        self.hud_buton(930, 590, "AI", "#FF4500", lambda e: messagebox.showinfo("AI", t["ai_msg"]))

        self.guncelleme_dongusu()

    def hud_buton(self, x, y, metin, renk, fonk):
        b = self.canvas.create_oval(x-35, y-35, x+35, y+35, fill=renk, outline="white", width=2)
        self.canvas.create_text(x, y, text=metin, fill="black", font=("Consolas", 10, "bold"))
        self.canvas.tag_bind(b, "<Button-1>", fonk)

    def guncelleme_dongusu(self):
        self.info_label.config(text=t["date_format"].format(time.strftime('%d/%m/%Y'), time.strftime('%H:%M:%S')))
        self.currency_label.config(text=t["curr"].format(self.usd_rate, self.eur_rate))
        self.deprem_label.config(text=self.deprem_bilgi)

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_data.pop(0); self.cpu_data.append(cpu)
        self.ram_data.pop(0); self.ram_data.append(ram)

        self.canvas.delete("grafik_iz")
        for i in range(len(self.cpu_data) - 1):
            x1, x2 = 750 + (i * 4), 750 + ((i + 1) * 4)
            self.canvas.create_line(x1, 130-(self.cpu_data[i]*0.7), x2, 130-(self.cpu_data[i+1]*0.7), fill="cyan", tags="grafik_iz")
            self.canvas.create_line(x1, 220-(self.ram_data[i]*0.7), x2, 220-(self.ram_data[i+1]*0.7), fill="#FF4500", tags="grafik_iz")
        self.after(1000, self.guncelleme_dongusu)

    def menu_ac(self, event):
        m = tk.Toplevel(self)
        m.title(t["menu"])
        m.geometry("250x150")
        m.configure(bg="#111")
        tk.Button(m, text=t["term"], command=lambda: subprocess.Popen(["gnome-terminal"]), bg="cyan", width=20, font=("Consolas", 9, "bold")).pack(pady=10)
        tk.Button(m, text=t["browser"], command=lambda: webbrowser.open("https://www.youtube.com"), bg="white", width=20, font=("Consolas", 9, "bold")).pack(pady=10)

if __name__ == "__main__":
    app = RetrexOS()
    app.mainloop()
