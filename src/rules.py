import json
import string

path = "data/kelimeler.json"

with open(path, "r", encoding="utf-8") as f:
    kelimeler = json.load(f)


class RULE:
    def __init__(self):
        self.negatif_sifatlar = set(
            kelimeler["negatifSifatlar"]
        )  # Negatif sıfatları JSON'dan al
        self.negatif_fiiller = set(
            kelimeler["negatifFiiller"]
        )  # Negatif fiilleri JSON'dan al

    def tumFiilleriBul(self, analysis_results):
        """
        Cümledeki tüm fiilleri bulur.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
            (str veya analiz nesneleri formatında olabilir)
        Returns:
           list: Tüm fiillerin string çıktılarından oluşan bir liste. Eğer fiil yoksa boş bir liste döner.
        """
        verbs = []

        for analysis in analysis_results:
            # Eğer analiz zaten string ise doğrudan kontrol et
            analysis_string = (
                analysis if isinstance(analysis, str) else analysis.format_string()
            )

            # Eğer bir fiil bulunursa listeye ekle
            if ":Verb" in analysis_string:
                verbs.append(analysis_string)
        return verbs

    def sifatlariBul(self, analysis_results):
        """
        Analiz sonuçlarında sıfat (Adj) etiketine sahip kelimeleri bulur.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            list: Sıfatların köklerini içeren bir liste. Eğer sıfat yoksa boş liste döner.
        """
        sifatlar = []
        for analysis in analysis_results:
            if (
                ":Adj" in analysis.format_string()
                or ":Noun" in analysis.format_string()
            ):
                # Kelimenin kökünü almak için format_string'deki ilk kısmı alıyoruz
                sifat_kok = analysis.format_string().split("[")[1].split(":")[0]
                sifatlar.append(sifat_kok)
        return sifatlar

    def negatifSifatVar(self, sentence, analysis_results):
        """
        Cümlede negatif bir sıfat olup olmadığını kontrol eder.
        Args:
            sentence (str): Kontrol edilecek cümle.
        Returns:
            bool: Negatif sıfat varsa True, yoksa False.
        """
        # Noktalama işaretlerini kaldır
        translator = str.maketrans("", "", string.punctuation)
        cleaned_sentence = sentence.translate(translator).lower()
        for word in cleaned_sentence.split():
            if word in self.negatif_sifatlar:
                return True

        sifatlar = self.sifatlariBul(analysis_results)
        for sifat in sifatlar:
            if sifat in self.negatif_sifatlar:
                return True
        return False

    def ironiVar(self, sentence):
        """
        Cümlede ironi olup olmadığını kontrol eder.
        Args:
            sentence (str): Kontrol edilecek cümle.
        Returns:
            bool: İroni varsa True, yoksa False.
        """
        if "(!)" in sentence.lower():
            return True
        return False

    def fiilVar(self, analysis_results):
        """
        Bir cümlede fiil (Verb) olup olmadığını kontrol eder.
        :param analysis_results: Zemberek'in analiz sonuçları (SingleAnalysis listesi)
        :return: True (fiil varsa), False (fiil yoksa)
        """
        for single_analysis in analysis_results:
            if ":Verb" in single_analysis.format_string():
                return True
        return False

    def fiilNegatif(self, analysis):
        s = analysis if isinstance(analysis, str) else analysis.format_string()
        if (
            s.split(":")[0].strip("[]") in self.negatif_fiiller
            or ":Verb+Neg" in s
            or ":Unable" in s
            or ":Neg" in s
        ):
            return True
        return False

    def sonIkiFiilNegatif(self, analysis_results):
        """
        Cümledeki son iki fiilin olumsuz olup olmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: Son iki fiil de olumsuzsa True, değilse False.
        """
        verbs = self.tumFiilleriBul(analysis_results)
        if len(verbs) >= 2:
            if self.fiilNegatif(verbs[-1]) and self.fiilNegatif(verbs[-2]):
                return True
        return False

    def sonFiilNegatif(self, analysis_results):
        """
        Cümledeki son fiilin olumsuz olup olmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: Son fiil olumsuzsa True, değilse False.
        """
        verbs = self.tumFiilleriBul(analysis_results)
        if len(verbs) >= 1:
            if self.fiilNegatif(verbs[-1]):
                return True
        return False

    def hicSifativeNegatifFiilVar(self, sentence, analysis_results):
        """
        Cümlede hiç sıfat veya fiil olup olmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: Sıfat veya fiil yoksa True, varsa False.
        """
        if "hiç" in sentence and self.sonFiilNegatif(analysis_results):
            return True
        if "Hiç" in sentence and self.sonFiilNegatif(analysis_results):
            return True
        return False

    def degismemPozitifMi(self, analysis_results):
        """
        'Değişmem' kelimesinin pozitif anlamda kullanılıp kullanılmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: Pozitifse True, değilse False.
        """
        for i, analysis in enumerate(analysis_results):
            # "değişmem" kelimesini kontrol et
            if "değiş:Verb+me:Neg" in analysis.format_string():
                if i > 0 and ":Dat" in analysis_results[i - 1].format_string():
                    return True  # Pozitif
        return False  # Negatif

    def neNeYapisiNegatifMi(self, analysis_results):
        """
        'Ne ... ne ...' yapısının cümlede kullanılıp kullanılmadığını ve olumsuzluk barındırıp barındırmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: 'Ne ... ne ...' yapısı varsa ve fiil olumsuz değilse True, aksi halde False.
        """
        ne_counter = 0
        for i, analysis in enumerate(analysis_results):
            if (
                "ne:Adj" in analysis.format_string()
                or "ne:Adv" in analysis.format_string()
            ):
                ne_counter += 1
        if ne_counter == 2 and not self.sonFiilNegatif(analysis_results):
            return True
        return False

    def isAcmakNegatifligiVarMi(self, analysis_results):
        """
        'iş açmak' yapısının cümlede bulunup bulunmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: 'iş açmak' yapısı varsa True, aksi halde False.
        """

        index = 0

        for i, analysis in enumerate(analysis_results):
            if "iş:Noun" in analysis.format_string():
                index = i
            elif "açmak:Verb" in analysis.format_string() and (
                (i == index + 1) or (i == index - 1)
            ):
                return True
        return False

    def ikiFiilArasiEdatVarMi(self, analysis_results):
        """
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        """

        indexOfFirstVerb = -1
        indexOfEdat = -1
        indexOfSecondVerb = -1

        for i, analysis in enumerate(analysis_results):
            if ":Verb" in analysis.format_string():
                if indexOfFirstVerb == -1:
                    indexOfFirstVerb = i
                else:
                    indexOfSecondVerb = i
            if "için:Postp" in analysis.format_string():
                indexOfEdat = i
        if indexOfFirstVerb < indexOfEdat < indexOfSecondVerb:
            return True
        return False

    def donakalmakNegatifligiVarMi(self, analysis_results):
        """
        'Donakalmak' veya 'donup kalmak' deyimlerinin cümlede bulunup bulunmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: 'donakalmak' veya 'donup kalmak' deyimleri cümlede varsa True, aksi halde False.
        """

        pass

    def yapYapabilirsenNegatifMi(self, analysis_results):
        """
        'Gel gelebilirsen, git gidebilirsen vb...' yapısının cümlede bulunup bulunmadığını kontrol eder.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            bool: 'yap yapabilirsen' yapısı varsa ve olumsuzluk anlamı katıyorsa True, aksi halde False.
        """
        pass
        # index = 0
        # for i, analysis in enumerate(analysis_results):
        #     if "iş:Noun" in analysis.format_string():
        #         index = i
        #     elif "açmak:Verb" in analysis.format_string() and (
        #         (i == index + 1) or (i == index - 1)
        #     ):
        #         return True
        # return False
