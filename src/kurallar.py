import json
import string

path = "data/kelimeler.json"

with open(path, "r", encoding="utf-8") as f:
    kelimeler = json.load(f)

class KURAL():
    def __init__(self):
        self.negatifSifatlar = set(kelimeler["negatifSifatlar"]) 
        self.negatifFiiller = set(kelimeler["negatifFiiller"])
        self.negatifKaliplar = set(kelimeler["negatifKaliplar"])
        self.pozitifKaliplar  = set(kelimeler["pozitifKaliplar"])

    def tumFiilleriBul(self, analizSonuclari):
        fiiller = []

        for analiz in analizSonuclari:
            analizString = analiz if isinstance(analiz, str) else analiz.format_string()

            if ":Verb" in analizString:
                fiiller.append(analizString)

        return fiiller

    def sifatlariBul(self, analizSonuclari):
        sifatlar = []
        for analiz in analizSonuclari:
            if ":Adj" in analiz.format_string() or ":Noun" in analiz.format_string():
                sifatKok = analiz.format_string().split("[")[1].split(":")[0]
                sifatlar.append(sifatKok)
        return sifatlar

    def negatifSifatVar(self, cumle, analizSonuclari):
        sifatlar = self.sifatlariBul(analizSonuclari)
        for sifat in sifatlar:
            if sifat in self.negatifSifatlar:
                return True

        translator = str.maketrans('', '', string.punctuation)
        temizCumle = cumle.translate(translator).lower()
        for kelime in temizCumle.split():
            if kelime in self.negatifSifatlar:
                return True

        for analiz in analizSonuclari:
            if ":Without→Adj" in analiz.format_string() or ":Without→Noun" in analiz.format_string() or ":Unable→Noun" in analiz.format_string() or ":Unable→Adj" in analiz.format_string():
                return True
        return False

    def ironiVar(self, cumle):
        if "(!)" in cumle.lower():
            return True
        return False

    def fiilVar(self, analizSonuclari):
        for analiz in analizSonuclari:
            if ":Verb" in analiz.format_string():
                return True
        return False
    
    def fiilNegatif(self, analiz):
        if isinstance(analiz, list):
            for a in analiz:
                if self.fiilNegatif(a):
                    return True
            return False

        analizString = analiz.format_string() if hasattr(analiz, "format_string") else analiz
        fiil = analizString.split(":")[0].split("[")[-1].strip()
        if fiil in self.negatifFiiller:
            if ":Verb+Neg" in analizString or ":Unable" in analizString or ":Neg" in analizString:
                return False
            return True

        if ":Verb+Neg" in analizString or ":Unable" in analizString or ":Neg" in analizString:
            return True

        return False
    
    def negatifNegatifFiil(self, analizSonuclari):
        fiiller = self.tumFiilleriBul(analizSonuclari)
        if len(fiiller) >= 2:
            if self.fiilNegatif(fiiller[-1]) and self.fiilNegatif(fiiller[-2]):
                return True
        return False

    def negatifPozitifFiil(self, analizSonuclari):
        fiiller = self.tumFiilleriBul(analizSonuclari)
        if len(fiiller) >= 2:
            if self.fiilNegatif(fiiller[-2]) and not self.fiilNegatif(fiiller[-1]):
                return True
        return False
    
    def pozitifNegatifFiil(self, analizSonuclari):
        fiiller = self.tumFiilleriBul(analizSonuclari)
        if len(fiiller) >= 2:
            if self.fiilNegatif(fiiller[-1]) and not self.fiilNegatif(fiiller[-2]):
                return True
        return False
        
    def sonFiilNegatif(self, analizSonuclari):
        fiiller = self.tumFiilleriBul(analizSonuclari)
        if len(fiiller) >= 1:
            if self.fiilNegatif(fiiller[-1]):
                return True
        return False
    
    def hicSifatiVeNegatifFiilVar(self, cumle, analizSonuclari):
        if "hiç " in cumle and self.sonFiilNegatif(analizSonuclari):
            return True
        if "Hiç " in cumle and self.sonFiilNegatif(analizSonuclari):
            return True
        return False
    
    def degismemPozitifMi(self, analizSonuclari):
        for i, analiz in enumerate(analizSonuclari):
            if "değiş:Verb+me:Neg" in analiz.format_string():
                if i > 0 and ":Dat" in analizSonuclari[i - 1].format_string():
                    return True
        return False
    
    def neNeYapisiNegatifMi(self, analizSonuclari):
        neSayaci = 0
        for analiz in analizSonuclari:
            if "ne:Adj" in analiz.format_string() or "ne:Adv" in analiz.format_string():
                neSayaci += 1
        if neSayaci == 2 and not self.sonFiilNegatif(analizSonuclari):
            return True

    def hayirVirgulVar(self, cumle):
        if "Hayır" in cumle or "hayır" in cumle:
            if "," in cumle:
                return True
        return False

    def maalesefVar(self, cumle):
        if "maalesef" in cumle or "Maalesef" in cumle:
            return True
        return False
    
    def negatifKalipVar(self, cumle):
        for kalip in self.negatifKaliplar:
            if kalip in cumle.lower():
                return True
        return False

    def pozitifKalipVar(self, cumle):
        for kalip in self.pozitifKaliplar:
            if kalip in cumle.lower():
                return True
        return False

    def yapYapabilirsenVar(self, cumle, analizSonuclari):
        fiiller = self.tumFiilleriBul(analizSonuclari)
        if not fiiller:
            return False
        
        sonFiilIndeksi = next((i for i, analiz in enumerate(analizSonuclari) if analiz.format_string() == fiiller[-1]), None)
        sonFiil = fiiller[-1]
        sonFiilKoku = sonFiil.split(":")[0]

        oncekiKelime = None
        if sonFiilIndeksi and sonFiilIndeksi > 0:
            oncekiKelimeAnalizi = analizSonuclari[sonFiilIndeksi - 1]
            oncekiKelime = oncekiKelimeAnalizi.format_string().split(":")[0]

        if oncekiKelime is None:
            return False

        if ":Cond" in sonFiil and sonFiilKoku == oncekiKelime:
            return True

        return False
