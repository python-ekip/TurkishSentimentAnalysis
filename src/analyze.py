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

    # Negatif kuralları kontrol et
    if rule.degismemPozitifMi(analysis_results):
        return "pozitif", "değişmem pozitif kuralı"
    if rule.neNeYapisiNegatifMi(analysis_results):
        return "negatif", "ne ne yapısı negatif"
    if rule.olumsuzFiilVar(analysis_results):
        return "negatif", "olumsuz fiil"
    if rule.yetersizlikEkiVar(analysis_results):
        return "negatif", "yetersizlik eki"
    if rule.negatifSifatVar(sentence):
        return "negatif", "negatif sıfat kuralı"
    if rule.ironiVar(sentence):
        return "negatif", "ironi kuralı"
    # Varsayılan sınıf
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
    evaluate_model_with_reasons("train_data2.xlsx", "classification_results.txt")











# # Logger ayarları
# logger = logging.getLogger(__name__)
# morphology = TurkishMorphology.create_with_defaults()

# rule = rules.RULE()

# class MockSingleAnalysis:
#     def __init__(self, text):
#         self.text = text
#     def format_string(self):
#         return self.text

# sentence = "bugün çok kötüleştim"
# analysis = morphology.analyze_sentence(sentence)
# after = morphology.disambiguate(sentence, analysis)

# analysis_results = after.best_analysis()
# for analysis in analysis_results:
#     print(analysis.format_string())


# is_negatif = rule.neNeYapisiNegatifMi(analysis_results)
# print("Ne ... ne ... yapısı negatif mi?", is_negatif)

# Analiz sonuçlarını ekrana yazdırma



# # Test cümlesi
# analysis = morphology.analyze_sentence(sentence)
# after = morphology.disambiguate(sentence, analysis)

# # Analiz sonuçlarını ekrana yazdırma
# print("\nBefore disambiguation")
# for e in analysis:
#     print(f"Word = {e.inp}")
#     for s in e:
#         print(s.format_string())

# print("\nAfter disambiguation")
# for s in after.best_analysis():
#     print(s.format_string())

# # Fiil cümlesi kontrolü
# if rule.fiilVar(after.best_analysis()):
#     if rule.fiildeOlumsuzlukEkiVar(after.best_analysis()):
#         print("\nOlumsuz cümle.")
#     else:
#         print("\nOlumlu cümle.")
# else:
#     print("\nisim cümlesi")

# file_path = "train_data.xlsx"
# output_file = "output.txt"
# data = pd.read_excel(file_path)
# sentences = data['Cümle'].tolist()

# with open(output_file, 'w', encoding='utf-8') as f:
#     i = 0
#     for sentence in sentences:
#         f.write(f"Cümle: {sentences[i]}\n")
#         analysis = morphology.analyze_sentence(sentence)
#         after = morphology.disambiguate(sentence, analysis)
        
#         f.write("Analiz Sonuçları:\n")
#         for s in after.best_analysis():
#             f.write(f"{s.format_string()}\n")
#         if rule.fiilVar(after.best_analysis()):
#             if rule.fiildeOlumsuzlukEkiVar(after.best_analysis()):
#                 f.write("\nOlumsuz cümle.\n")
#             else:
#                 f.write("\nOlumlu cümle.\n")
#         else:
#             f.write("\nisim cümlesi\n")
#         f.write("-------------------------------------------------------\n\n")
#         i += 1

# print(f"Analiz sonuçları '{output_file}' dosyasına kaydedildi.")