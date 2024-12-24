import argparse
import time
import logging
import pandas as pd
import os
import kurallar
from zemberek import TurkishMorphology

# Logger ayarları
logging.basicConfig(level=logging.INFO, filename="classification_log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Zemberek Morfoloji
morphology = TurkishMorphology.create_with_defaults()

# RULE Sınıfı
kural = kurallar.KURAL()

def cumleleriSiniflandir(cumle):
    """
    Bir cümleyi sınıflandırır ve negatif/pozitif olma sebebini döner.
    Args:
        cumle (str): Sınıflandırılacak cümle.
    Returns:
        tuple: (tahminiSinif, sebep)
    """
    analiz = morphology.analyze_sentence(cumle)
    after = morphology.disambiguate(cumle, analiz)
    analizSonuclari = after.best_analysis()

    # Spesifik kurallar
    if kural.degismemPozitifMi(analizSonuclari):
        return "pozitif", "değişmem pozitif kuralı"
    if kural.ironiVar(cumle):
        return "negatif", "ironi kuralı"
    if kural.neNeYapisiNegatifMi(analizSonuclari):
        return "negatif", "ne ne yapısı negatif"
    if kural.hayirVirgulVar(cumle):
        return "negatif", "hayır virgül kuralı"
    if kural.yapYapabilirsenVar(cumle, analizSonuclari):
        return "negatif", "yap yapabilirsen kuralı"
    if kural.negatifKalipVar(cumle):
        return "negatif", "negatif kalıp kuralı"
    if kural.pozitifKalipVar(cumle):
        return "pozitif", "pozitif kalıp kuralı"
    # Genel kurallar
    if kural.fiilVar(analizSonuclari):
        fiiller = kural.tumFiilleriBul(analizSonuclari)
        fiil_count = len(fiiller)
        
        if kural.hicSifatiVeNegatifFiilVar(cumle, analizSonuclari):
            return "negatif", "hiç sıfatı negatif fiil var"

        if fiil_count == 1:
            if kural.fiilNegatif(fiiller[0]) and kural.negatifSifatVar(cumle, analizSonuclari):
                return "pozitif", "fiil negatif ve negatif sıfat var"
            elif kural.fiilNegatif(fiiller[0]):
                return "negatif", "tek fiil negatif"

        elif fiil_count >= 2:
            if kural.negatifNegatifFiil(fiiller):
                return "pozitif", "son iki fiil olumsuz"
            elif kural.negatifPozitifFiil(fiiller):
                return "negatif", "sondan bir önceki fiil olumsuz"
            elif kural.pozitifNegatifFiil(fiiller):
                return "negatif", "son fiil olumsuz önceki fiil olumlu"
            elif kural.sonFiilNegatif(fiiller):
                return "negatif", "son fiil olumsuz"
            else:
                for fiil in fiiller:
                    if kural.fiilNegatif(fiil):
                        return "negatif", "negatif fiil var"
    
    if kural.negatifSifatVar(cumle, analizSonuclari):
        return "negatif", "sadece negatif sıfat var"
    
    return "pozitif", "hiçbir negatif kural çalışmadı"

def modeliUygula(file_path, output_file):
    """
    Excel dosyasındaki cümleleri kurallara göre sınıflandırır, karmaşıklık matrisi hesaplar,
    doğruluk, kesinlik, anma ve F1-ölçütü değerlerini hesaplar ve sonuçları bir txt dosyasına kaydeder.
    Args:
        file_path (str): Excel dosyasının yolu.
        output_file (str): Çıktı txt dosyasının yolu.
    """
    # Dosyayı oku
    df = pd.read_excel(file_path)
    tumCumleSayisi = len(df)

    # Karmaşıklık Matrisi Değerleri
    dp = 0  # Doğru Pozitif
    yp = 0  # Yanlış Pozitif
    yn = 0  # Yanlış Negatif
    dn = 0  # Doğru Negatif

    # Çıktı dosyasını aç
    with open(output_file, "w", encoding="utf-8") as output:
        for index, row in df.iterrows():
            cumle = row["Cümle"]
            gercekSinif = row["Sınıf"].strip().lower()  # Gerçek sınıf
            tahminiSinif, sebep = cumleleriSiniflandir(cumle)  # Tahmini sınıf ve sebep

            # Loglama
            logMessage = f"Cümle: {cumle} | Gerçek: {gercekSinif} | Tahmin: {tahminiSinif} | Sebep: {sebep}\n"
            logger.info(logMessage.strip())
            output.write(logMessage)

            # Karmaşıklık matrisi güncellemesi
            if gercekSinif == "pozitif" and tahminiSinif == "pozitif":
                dp += 1
            elif gercekSinif == "pozitif" and tahminiSinif == "negatif":
                yn += 1
            elif gercekSinif == "negatif" and tahminiSinif == "pozitif":
                yp += 1
            elif gercekSinif == "negatif" and tahminiSinif == "negatif":
                dn += 1

        # Doğruluk oranı hesaplama
        dogruluk = (dp + dn) / tumCumleSayisi if tumCumleSayisi > 0 else 0
        dogrulukYuzdesi = dogruluk * 100
        keskinlik = dp / (dp + yp) if (dp + yp) > 0 else 0
        anma = dp / (dp + yn) if (dp + yn) > 0 else 0
        f1_Olcusu = (2 * keskinlik * anma) / (keskinlik + anma) if (keskinlik + anma) > 0 else 0

        # Özet bilgileri yazdırma
        summary = (
            f"\nToplam cümle: {tumCumleSayisi}\n"
            f"Doğru Pozitif (DP): {dp}\n"
            f"Yanlış Pozitif (YP): {yp}\n"
            f"Yanlış Negatif (YN): {yn}\n"
            f"Doğru Negatif (DN): {dn}\n"
            f"Doğruluk: {dogruluk:2f} , yüzde: {dogrulukYuzdesi:2f}\n"
            f"Kesinlik (Precision): {keskinlik:2f}\n"
            f"Anma (Recall): {anma:2f}\n"
            f"F1-Ölçütü: {f1_Olcusu:2f}\n"
        )

        logger.info(summary.strip())
        output.write(summary)

    print(f"Sonuçlar {output_file} dosyasına kaydedildi.")

if __name__ == "__main__":
    # Argümanları tanımla
    parser = argparse.ArgumentParser(description="Excel dosyasındaki cümleleri sınıflandır ve sonuçları yaz.")
    parser.add_argument("input_file", type=str, help="Giriş Excel dosyasının yolu.")
    parser.add_argument("output_file", type=str, help="Çıktı txt dosyasının yolu.")
    
    # Argümanları al
    args = parser.parse_args()

    # Fonksiyonu çağır
    modeliUygula(args.input_file, args.output_file)
