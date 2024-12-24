# Turkish Sentiment Analysis

Bu proje, Türkçe metinlere yönelik duygu analizi yapmak amacıyla geliştirilmiştir. Proje, verilen metinleri belirli kurallar ve model ile sınıflandırarak pozitif veya negatif olarak etiketler. Ayrıca, modelin performansını değerlendiren metrikler (doğruluk, kesinlik, anma, F1-ölçütü) hesaplanır ve sonuçlar bir dosyaya kaydedilir.

## Özellikler

- Türkçe metinlerin pozitif veya negatif olarak sınıflandırılması.
- Modelin doğruluk, kesinlik, anma ve F1-ölçütü ile değerlendirilmesi.
- Karmaşıklık matrisi hesaplanması.
- Kullanıcı tarafından sağlanan verilerle modelin çalıştırılması.

## Gereksinimler

Projenin çalışabilmesi için aşağıdaki Python kütüphanelerine ihtiyacınız olacak:

- `pandas`: Verilerin işlenmesi için.
- `argparse`: Komut satırı argümanlarını işlemek için.
- `zemberek`: Türkçe dil işleme kütüphanesi (eğer projenizde kullanılacaksa).

Proje ile birlikte gelen `requirements.txt` dosyasını kullanarak tüm bağımlılıkları kolayca kurabilirsiniz.

### Bağımlılıkların Yüklenmesi

```bash
pip install -r requirements.txt
```

### Gerekli Veriyi Sağlayın

Proje, Türkçe metinlerin bulunduğu bir Excel dosyasına ihtiyaç duyar. Bu dosya, her satırda bir cümle ve onun doğru sınıf etiketini (`pozitif` veya `negatif`) içermelidir. Örnek veri formatı aşağıdaki gibi olmalıdır:

| Cümle                           | Sınıf   |
|----------------------------------|---------|
| Bugün hava çok güzel.            | pozitif |
| Bu hafta işler çok yoğun.        | negatif |
| Harika bir film izledim!         | pozitif |
| Yazın gelmesi çok sevindirici.   | pozitif |

Bu dosyayı */data* dizinine eklemenizi tavsiye ederiz. Çünkü model çalıştırılırken dosya yolu parametre olarak girilecektir.

### Modelin Çalıştırılması

```bash
python src/analyze.py <input_file_path> <output_file_path>
```

- `<input_file_path>`: Analiz edilecek Excel dosyasının yolu *(örneğin data/yenidataset.xlsx)*.
- `<output_file_path>`: Sonuçların kaydedileceği çıktı dosyasının yolu *(örneğin reports/results.txt)*.

#### Örnek Kullanım

```bash
python src/analyze.py data/yenidataset.xlsx reports/results.txt
```

### Sonuçları İnceleme

Model çalıştıktan sonra, sonuçlar belirtilen çıktı dosyasına yazılacaktır. Dosya, her bir cümle için tahmin edilen sınıf ve sebebi içerecek şekilde düzenlenmiştir. Ayrıca, modelin genel performansı (doğruluk, kesinlik, anma, F1-ölçütü) da özet olarak eklenir.

## Katkıda Bulunanlar

Bu proje, aşağıdaki kişilerin katkılarıyla şekillendi:

- [Fatih Parmaksız](https://github.com/fatihyilmaz) - Model geliştirme ve kodlama
- [Aytuğ Değer](https://github.com/Aytgg) - İyileştirmeler ve testler
- [Elif Pazarbaşı](https://github.com/elifpazarda) - Test verisi ekleme ve kural yazımı
- [Zehra Aktürk](https://github.com/Zehrakturk) - Raporlama
- [Melike Badem](https://github.com/MelikeBadem) - Sunum hazırlama

Teşekkürler!