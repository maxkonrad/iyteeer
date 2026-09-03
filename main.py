import bs4
import requests
import os
from send_email import send_email

WEBSITE_URL = "https://eee.iyte.edu.tr"
FILE_NAME = "previous_content.txt"

def main():
    try:
        response = requests.get(WEBSITE_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Siteye erişilemedi hacı: {e}")
        return

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    
    etkinlikler_section = soup.select_one(".etkinlikler > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > h3:nth-child(1)")
    haberler_section = soup.select_one(".haberler > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > h3:nth-child(1)")
    duyurular_section = soup.select_one(".duyurular > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > div:nth-child(2) > p:nth-child(1) > b:nth-child(1)")

    etkinlikler_text = etkinlikler_section.get_text(strip=True) if etkinlikler_section else ""
    haberler_text = haberler_section.get_text(strip=True) if haberler_section else ""
    duyurular_text = duyurular_section.get_text(strip=True) if duyurular_section else ""

    previous_etkinlikler, previous_haberler, previous_duyurular = "", "", ""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            if len(lines) >= 3:
                previous_etkinlikler, previous_haberler, previous_duyurular = lines[0], lines[1], lines[2]

    updated = False

    # Her kategoriyi tek tek kontrol edip, değişenleri kendi parametreleriyle mail atıyoruz
    if etkinlikler_text != previous_etkinlikler:
        send_email("Etkinlikler", previous_etkinlikler, etkinlikler_text)
        updated = True
        
    if haberler_text != previous_haberler:
        send_email("Haberler", previous_haberler, haberler_text)
        updated = True
        
    if duyurular_text != previous_duyurular:
        send_email("Duyurular", previous_duyurular, duyurular_text)
        updated = True

    if updated:
        print("Yeni bir şeyler var dayı, mailleri ateşledim...")
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write(f"{etkinlikler_text}\n{haberler_text}\n{duyurular_text}")
    else:
        print("Yeni bir güncelleme yok kral, ortalık sakin.")

if __name__ == "__main__":
    main()