class RULE():
    def __init__(self):
        pass

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
