class RULE():
    def __init__(self):
        pass

    def sonFiilBul(self, analysis_results):
        """
        Cümledeki son fiili bulur.
        Args:
            analysis_results (list): Zemberek'ten alınan analiz sonuçlarının listesi.
        Returns:
            str: Son fiilin format_string() çıktısı. Eğer fiil yoksa None döner.
        """
        last_verb = None

        for analysis in analysis_results:
            # Eğer bir fiil bulunursa, son fiili güncelle
            if ":Verb" in analysis.format_string():
                last_verb = analysis.format_string()
        return last_verb

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

    def fiildeOlumsuzlukEkiVar(self, analysis_results):
        for single_analysis in analysis_results:
            if ":Neg" in single_analysis.format_string():
                return True
        return False
    
    def olumsuzFiilVar(self, analysis_results):
        for single_analysis in analysis_results:
            if ":Verb+Neg" in single_analysis.format_string(): 
                return True
        return False

    def yetersizlikEkiVar(self, analysis_results):
        for single_analysis in analysis_results:
            if ":Unable" in single_analysis.format_string():
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
        fiil_bulundu = False  # Ne yapısından sonra fiilin olup olmadığını kontrol etmek için

        for i, analysis in enumerate(analysis_results):
            if "ne:Adj" in analysis.format_string():
                ne_counter += 1
            if ":Verb" in analysis.format_string():
                fiil_bulundu = True
        if ne_counter == 2:
            last_verb = sonFiilBul(analysis_results)

            # Eğer son fiil varsa ve olumsuzluk içeriyorsa negatif olarak değerlendir
            if last_verb and (":Neg" in last_verb or ":Unable" in last_verb):
                return False  # Negatif
            return True  # Pozitif
        return False  # 'Ne ... ne ...' yapısı yoksa negatif olarak değerlendir
