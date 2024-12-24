import logging
import kurallar
from zemberek import TurkishMorphology

# Logger ayarları
logger = logging.getLogger(__name__)
morphology = TurkishMorphology.create_with_defaults()

kural = kurallar.KURAL()

cumle = "Ne yazık ki, ben bunu yaptım"
analysis = morphology.analyze_sentence(cumle)
after = morphology.disambiguate(cumle, analysis)

analysis_results = after.best_analysis()
for analysis in analysis_results:
    print(analysis.format_string())

def cumleleriSiniflandir(cumle):
    """
    Bir cümleyi sınıflandırır ve negatif/pozitif olma sebebini döner.
    Args:
        cumle (str): Sınıflandırılacak cümle.
    Returns:
        tuple: (tahminiSinif, sebep)
    """
    analysis = morphology.analyze_sentence(cumle)
    after = morphology.disambiguate(cumle, analysis)
    analysis_results = after.best_analysis()

    # Spesifik kurallar
    if kural.degismemPozitifMi(analysis_results):
        return "pozitif", "değişmem pozitif kuralı"
    if kural.ironiVar(cumle):
        return "negatif", "ironi kuralı"
    if kural.neNeYapisiNegatifMi(analysis_results):
        return "negatif", "ne ne yapısı negatif"
    if kural.hayirVirgulVar(cumle):
        return "negatif", "hayır virgül kuralı"
    if kural.yapYapabilirsenVar(cumle, analysis_results):
        return "negatif", "yap yapabilirsen kuralı"
    if kural.negatifKalipVar(cumle):
        return "negatif", "negatif kalıp kuralı"
    if kural.pozitifKalipVar(cumle):
        return "pozitif", "pozitif kalıp kuralı"
    # Genel kurallar
    if kural.fiilVar(analysis_results):
        fiiller = kural.tumFiilleriBul(analysis_results)
        fiil_count = len(fiiller)
        
        if kural.hicSifativeNegatifFiilVar(cumle, analysis_results):
            return "negatif", "hiç sıfatı negatif fiil var"

        if fiil_count == 1:
            if kural.fiilNegatif(fiiller[0]) and kural.negatifSifatVar(cumle, analysis_results):
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
    
    if kural.negatifSifatVar(cumle, analysis_results):
        return "negatif", "sadece negatif sıfat var"
    
    return "pozitif", "hiçbir negatif kural çalışmadı"

s = cumleleriSiniflandir(cumle)
print(s)

