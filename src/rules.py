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
    