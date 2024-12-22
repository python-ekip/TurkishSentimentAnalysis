import logging

from zemberek import TurkishMorphology

import rules

# Logger ayarları
logger = logging.getLogger(__name__)
morphology = TurkishMorphology.create_with_defaults()

rule = rules.RULE()

sentence = "Bunca saat boyunca bütün işittiğin bu sözlerden sonra, uyu uyuyabilirsen!"
analysis = morphology.analyze_sentence(sentence)
after = morphology.disambiguate(sentence, analysis)

analysis_results = after.best_analysis()
for analysis in analysis_results:
    print(analysis.format_string())


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
    if rule.isAcmakNegatifligiVarMi(analysis_results):
        return "negatif", "iş açmak negatif kuralı"
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
            if rule.fiilNegatif(fiiller[0]) and rule.negatifSifatVar(
                sentence, analysis_results
            ):
                return "pozitif", "fiil negatif ve negatif sıfat var"
            elif rule.fiilNegatif(fiiller[0]):
                return "negatif", "tek fiil negatif"

        elif fiil_count >= 2:
            if rule.sonIkiFiilNegatif(fiiller):
                return "pozitif", "son iki fiil olumsuz"
            elif rule.sonFiilNegatif(fiiller):
                return "negatif", "son fiil olumsuz"

    if rule.negatifSifatVar(sentence, analysis_results):
        return "negatif", "sadece negatif sıfat var"

    return "pozitif", "hiçbir negatif kural çalışmadı"


a = classify_sentence_with_reason(sentence)
print("------------------------------------------------------------------")
print(a)
