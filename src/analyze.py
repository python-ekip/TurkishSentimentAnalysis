import time
import logging
import pandas as pd
import os
import rules
from zemberek import TurkishMorphology

# Logger ayarları
logging.basicConfig(level=logging.INFO, filename="classification_log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Zemberek Morfoloji
morphology = TurkishMorphology.create_with_defaults()

# RULE Sınıfı
rule = rules.RULE()

def classify_sentence_with_reason(sentence):
    """
    Bir cümleyi sınıflandırır ve negatif/pozitif olma sebebini döner.
    Args:
        sentence (str): Sınıflandırılacak cümle.
    Returns:
        tuple: (predicted_class, reason)
    """
    analysis = morphology.analyze_sentence(sentence)
    after = morphology.disambiguate(sentence, analysis)
    analysis_results = after.best_analysis()

    # Spesifik kurallar
    if rule.degismemPozitifMi(analysis_results):
        return "pozitif", "değişmem pozitif kuralı"
    if rule.ironiVar(sentence):
        return "negatif", "ironi kuralı"
    if rule.neNeYapisiNegatifMi(analysis_results):
        return "negatif", "ne ne yapısı negatif"

    if rule.fiilVar(analysis_results):
        fiiller = rule.tumFiilleriBul(analysis_results)
        fiil_count = len(fiiller)
        
        if rule.hicSifativeNegatifFiilVar(sentence, analysis_results):
            return "negatif", "hiç sıfatı negatif fiil var"

        if fiil_count == 1:
            if rule.fiilNegatif(fiiller[0]) and rule.negatifSifatVar(sentence, analysis_results):
                return "pozitif", "fiil negatif ve negatif sıfat var"
            elif rule.fiilNegatif(fiiller[0]):
                return "negatif", "tek fiil negatif"

        elif fiil_count >= 2:
            if rule.negatifNegatifFiil(fiiller):
                return "pozitif", "son iki fiil olumsuz"
            elif rule.negatifPozitifFiil(fiiller):
                return "negatif", "sondan bir önceki fiil olumsuz"
            elif rule.pozitifNegatifFiil(fiiller):
                return "negatif", "son fiil olumsuz önceki fiil olumlu"
            elif rule.sonFiilNegatif(fiiller):
                return "negatif", "son fiil olumsuz"
    
    if rule.negatifSifatVar(sentence, analysis_results):
        return "negatif", "sadece negatif sıfat var"
    
    return "pozitif", "hiçbir negatif kural çalışmadı"

def evaluate_model_with_reasons(file_path, output_file):
    """
    Excel dosyasındaki cümleleri kurallara göre sınıflandırır, doğruluk oranını hesaplar
    ve sonuçları bir txt dosyasına kaydeder.
    Args:
        file_path (str): Excel dosyasının yolu.
        output_file (str): Çıktı txt dosyasının yolu.
    """
    # Dosyayı oku
    df = pd.read_excel(file_path)
    total_sentences = len(df)
    correct_predictions = 0

    # Çıktı dosyasını aç
    with open(output_file, "w", encoding="utf-8") as output:
        for index, row in df.iterrows():
            sentence = row["Cümle"]
            true_class = row["Sınıf"].strip().lower()  # Gerçek sınıf
            predicted_class, reason = classify_sentence_with_reason(sentence)  # Tahmini sınıf ve sebep

            # Loglama
            log_message = f"Cümle: {sentence} | Gerçek: {true_class} | Tahmin: {predicted_class} | Sebep: {reason}\n"
            logger.info(log_message.strip())
            output.write(log_message)

            # Doğruluk kontrolü
            if true_class == predicted_class:
                correct_predictions += 1

        # Doğruluk oranı hesaplama
        accuracy = (correct_predictions / total_sentences) * 100
        summary = f"Toplam cümle: {total_sentences}, Doğru tahmin: {correct_predictions}, Doğruluk: {accuracy:.2f}%\n"
        logger.info(summary.strip())
        output.write("\n" + summary)

    print(f"Sonuçlar {output_file} dosyasına kaydedildi.")
if __name__ == "__main__":
    evaluate_model_with_reasons("data/hoca_data.xlsx", "reports/elif_results1.txt")
