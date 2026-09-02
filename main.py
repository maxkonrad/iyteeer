import bs4
import requests
import time
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from send_email import send_email
from datetime import datetime, timezone, timedelta

WEBSITE_URL = "https://eee.iyte.edu.tr"
FILE_NAME = "previous_content.txt"

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Sistem ayakta yorgun kral!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

def main():
    print("Sistem çalışmaya başladı kral...")
    
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write("\n\n")

    while True:
        try:
            response = requests.get(WEBSITE_URL, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Siteye erişilemedi hacı: {e}")
            time.sleep(60)
            continue

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        etkinlikler_section = soup.select_one(".etkinlikler > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > h3:nth-child(1)")
        haberler_section = soup.select_one(".haberler > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > h3:nth-child(1)")
        duyurular_section = soup.select_one(".duyurular > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > p:nth-child(1) > b:nth-child(1)")

        etkinlikler_text = etkinlikler_section.get_text(strip=True) if etkinlikler_section else ""
        haberler_text = haberler_section.get_text(strip=True) if haberler_section else ""
        duyurular_text = duyurular_section.get_text(strip=True) if duyurular_section else ""

        with open(FILE_NAME, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            if len(lines) >= 3:
                previous_etkinlikler, previous_haberler, previous_duyurular = lines[0], lines[1], lines[2]
            else:
                previous_etkinlikler, previous_haberler, previous_duyurular = "", "", ""

        tz_gmt3 = timezone(timedelta(hours=3))
        current_time = datetime.now(tz_gmt3)
        
        if current_time.hour in [8, 13, 17]:
            if etkinlikler_text != previous_etkinlikler or haberler_text != previous_haberler or duyurular_text != previous_duyurular:
                print("Yeni bir şeyler var dayı, maili ateşliyorum...")
                send_email()
                
                with open(FILE_NAME, "w", encoding="utf-8") as file:
                    file.write(f"{etkinlikler_text}\n{haberler_text}\n{duyurular_text}")

        time.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    main()