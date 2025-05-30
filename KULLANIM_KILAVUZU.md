# 📖 Mini Süreç Madenciliği Uygulaması - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Uygulamayı Başlatma
```bash
python app.py
```

### 2. Tarayıcıda Açma
Tarayıcınızda `http://localhost:5000` adresini açın.

## 📊 Uygulama Özellikleri

### ✅ Temel Özellikler
- **CSV Dosyası Yükleme**: Drag & drop veya tıklayarak dosya seçme
- **Otomatik Veri Doğrulama**: Gerekli sütunların kontrolü
- **Case Süre Analizi**: Her case'in toplam süresini hesaplama
- **Aktivite Frekans Analizi**: En sık kullanılan aktiviteleri bulma
- **Geçiş Analizi**: Aktiviteler arası geçiş matrisini oluşturma
- **İnteraktif Grafikler**: Plotly ile dinamik görselleştirmeler
- **Süreç Akış Diyagramı**: BPMN tarzı network grafiği

### 🎨 Gelişmiş Özellikler
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Özet İstatistikler**: Kapsamlı veri özetleri
- **Detaylı Raporlama**: Tablo formatında sonuçlar
- **Örnek Veri**: Test için hazır örnek dosya

## 📋 CSV Dosya Formatı

### Gerekli Sütunlar
Yükleyeceğiniz CSV dosyasında şu sütunlar **mutlaka** bulunmalıdır:

| Sütun Adı | Açıklama | Örnek |
|-----------|----------|-------|
| `Case ID` | Süreç örneği kimliği | CASE_001, CASE_002 |
| `Activity Name` | Aktivite/adım adı | Başvuru Alındı, Onay Bekliyor |
| `Start Time` | Başlangıç tarihi/saati | 2024-01-01 09:00:00 |
| `End Time` | Bitiş tarihi/saati | 2024-01-01 09:30:00 |

### Tarih Formatı
Tarih sütunları şu formatta olmalıdır: `YYYY-MM-DD HH:MM:SS`

**Örnek:**
```
2024-01-01 09:00:00
2024-01-01 14:30:00
```

## 🔧 Adım Adım Kullanım

### 1. Veri Yükleme
1. Ana sayfada "CSV dosyanızı buraya sürükleyin" alanını görün
2. Dosyanızı bu alana sürükleyin VEYA alana tıklayarak dosya seçici açın
3. Sadece `.csv` uzantılı dosyalar kabul edilir
4. Dosya yüklendikten sonra otomatik doğrulama yapılır

### 2. Örnek Dosya İndirme
- "Örnek Dosya İndir" butonuna tıklayın
- `sample_data.csv` dosyası oluşturulur
- Bu dosyayı referans olarak kullanabilirsiniz

### 3. Analiz Sonuçlarını İnceleme
Dosya başarıyla yüklendikten sonra şu bölümler görüntülenir:

#### 📊 Özet İstatistikler
- Toplam Case Sayısı
- Toplam Aktivite Sayısı
- Benzersiz Aktivite Sayısı
- Tarih Aralığı

#### ⏱️ Case Süre Analizi
- Ortalama, minimum, maksimum süreler
- Süre dağılım histogramı
- Detaylı case süre tablosu

#### 📈 Aktivite Frekansları
- En sık kullanılan aktiviteler
- İnteraktif bar chart
- Frekans değerleri

#### 🔄 Geçiş Analizi
- En sık aktivite geçişleri
- Süreç akış diyagramı
- Network grafiği

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: İş Süreci Analizi
```
Amaç: Müşteri başvuru sürecini analiz etmek
Veri: Başvuru formları, onay süreçleri, tamamlanma zamanları
Sonuç: Hangi adımların en uzun sürdüğünü ve darboğazları tespit etmek
```

### Senaryo 2: Sistem Log Analizi
```
Amaç: Yazılım süreçlerinin performansını ölçmek
Veri: Sistem logları, işlem adımları, zaman damgaları
Sonuç: Optimizasyon fırsatlarını ve hata noktalarını bulmak
```

## ⚠️ Yaygın Hatalar ve Çözümleri

### Hata: "Eksik sütunlar"
**Sebep:** CSV dosyasında gerekli sütunlar eksik
**Çözüm:** Dosyanızda şu sütunların bulunduğundan emin olun:
- Case ID
- Activity Name  
- Start Time
- End Time

### Hata: "Tarih formatı hatası"
**Sebep:** Tarih sütunları yanlış formatta
**Çözüm:** Tarihleri `YYYY-MM-DD HH:MM:SS` formatında düzenleyin

### Hata: "Dosya yükleme hatası"
**Sebep:** Dosya .csv uzantılı değil veya bozuk
**Çözüm:** 
- Dosyanın .csv uzantılı olduğundan emin olun
- Excel'den "CSV (Comma delimited)" olarak kaydedin
- Dosya boyutunun 16MB'dan küçük olduğunu kontrol edin

## 💡 İpuçları

### Veri Hazırlama
- Excel'de çalışıyorsanız "Farklı Kaydet" > "CSV (Comma delimited)" seçin
- Türkçe karakterler sorun çıkarabilir, mümkünse İngilizce kullanın
- Tarih sütunlarında boş değer olmamasına dikkat edin

### Performans
- Büyük dosyalar (>1000 satır) yükleme süresi alabilir
- Tarayıcı sekmesini kapatmayın, işlem tamamlanana kadar bekleyin

### Görselleştirme
- Grafiklerde zoom yapabilir, pan edebilirsiniz
- Grafikler üzerinde hover yaparak detay bilgi alabilirsiniz
- Grafikleri PNG olarak indirebilirsiniz

## 🔧 Teknik Detaylar

### Desteklenen Tarayıcılar
- Chrome (önerilen)
- Firefox
- Safari
- Edge

### Sistem Gereksinimleri
- Python 3.7+
- 4GB RAM (önerilen)
- 100MB disk alanı

### Port Bilgisi
Uygulama varsayılan olarak `5000` portunda çalışır. Eğer bu port kullanımdaysa, `app.py` dosyasında farklı bir port belirleyebilirsiniz.

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Terminal/komut satırındaki hata mesajlarını kontrol edin
2. CSV dosyanızın format gereksinimlerini karşıladığından emin olun
3. Tarayıcı konsolunu (F12) kontrol edin

---

**Mini Süreç Madenciliği Uygulaması v1.0**  
*Süreç Madenciliği Dersi Projesi*
