import time
import logging
import pandas as pd
import os
import rules
from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)

# Logger ayarları
logger = logging.getLogger(__name__)
morphology = TurkishMorphology.create_with_defaults()

rule = rules.RULE()
# Zemberek nesnelerini oluşturma
start = time.time()
normalizer = TurkishSentenceNormalizer(morphology)
logger.info(f"Normalization instance created in: {time.time() - start} s")

start = time.time()
sc = TurkishSpellChecker(morphology)
logger.info(f"Spell checker instance created in: {time.time() - start} s")

# Fiil var mı kontrol fonksiyonu


# Test cümlesi
sentence = "eve gittim."
analysis = morphology.analyze_sentence(sentence)
after = morphology.disambiguate(sentence, analysis)

# Analiz sonuçlarını ekrana yazdırma
print("\nBefore disambiguation")
for e in analysis:
    print(f"Word = {e.inp}")
    for s in e:
        print(s.format_string())

print("\nAfter disambiguation")
for s in after.best_analysis():
    print(s.format_string())

# Fiil cümlesi kontrolü
if rule.fiilVar(after.best_analysis()):
    if rule.fiildeOlumsuzlukEkiVar(after.best_analysis()):
        print("\nOlumsuz cümle.")
    else:
        print("\nOlumlu cümle.")
else:
    print("\nisim cümlesi")
