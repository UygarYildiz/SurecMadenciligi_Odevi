# Mini Süreç Madenciliği Uygulaması

Bu proje, süreç madenciliği dersi için geliştirilmiş kapsamlı bir web uygulamasıdır. CSV formatındaki süreç verilerini analiz ederek çeşitli görselleştirmeler ve istatistikler sunar.

## 🚀 Özellikler

### ✅ Temel Gereksinimler
- **Veri Yükleme**: CSV dosyası yükleme (drag & drop destekli)
- **Case Süre Analizi**: Her Case ID'nin toplam süresini hesaplama
- **Aktivite Frekans Analizi**: En sık gerçekleşen adımları bulma
- **Ortalama Süreç Süresi**: Tüm case'lerin ortalama tamamlanma süresi
- **Geçiş Analizi**: Aktiviteler arası en sık geçişleri analiz etme

### 🎨 Gelişmiş Özellikler
- **İnteraktif Grafikler**: Plotly ile dinamik görselleştirmeler
- **Süreç Akış Diyagramı**: BPMN tarzı network grafiği
- **Responsive Web Arayüzü**: Modern Bootstrap tasarımı
- **Özet İstatistikler**: Kapsamlı veri özetleri
- **Detaylı Raporlama**: Tablo formatında sonuçlar

## 📋 Gerekli Sütunlar

CSV dosyanızda şu sütunlar bulunmalıdır:
- `Case ID`: Süreç örneği kimliği
- `Activity Name`: Aktivite/adım adı
- `Start Time`: Başlangıç tarihi/saati (YYYY-MM-DD HH:MM:SS formatında)
- `End Time`: Bitiş tarihi/saati (YYYY-MM-DD HH:MM:SS formatında)

## 🛠️ Kurulum

### 1. Gereksinimler
- Python 3.7 veya üzeri
- pip (Python paket yöneticisi)

### 2. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Çalıştırma
```bash
python app.py
```

### 4. Tarayıcıda Açma
Uygulama başlatıldıktan sonra tarayıcınızda şu adresi açın:
```
http://localhost:5000
```

**Not:** Uygulama başarıyla çalıştırıldı ve test edildi! ✅

## 📊 Kullanım

### 1. Veri Yükleme
- Ana sayfada "CSV dosyanızı buraya sürükleyin" alanına dosyanızı sürükleyin
- Veya alana tıklayarak dosya seçici ile dosyanızı seçin
- Örnek veri için "Örnek Dosya İndir" butonunu kullanabilirsiniz

### 2. Analiz Sonuçları
Dosya yüklendikten sonra otomatik olarak şu analizler yapılır:
- **Özet İstatistikler**: Toplam case, aktivite sayıları
- **Case Süre Analizi**: Ortalama, minimum, maksimum süreler
- **Aktivite Frekansları**: En sık kullanılan aktiviteler
- **Geçiş Analizi**: Aktiviteler arası geçiş matrisi
- **Görselleştirmeler**: İnteraktif grafikler ve süreç akış diyagramı

## 📁 Proje Yapısı

```
Süreç_Ödev2/
├── app.py                 # Ana Flask uygulaması
├── process_analyzer.py    # Süreç analizi mantığı
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Bu dosya
├── sample_data.csv       # Örnek veri dosyası
├── templates/
│   └── index.html        # Ana web sayfası
├── static/
│   ├── style.css         # CSS stilleri
│   └── script.js         # JavaScript mantığı
└── uploads/              # Yüklenen dosyalar (otomatik oluşur)
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Veri İşleme**: pandas, numpy
- **Görselleştirme**: matplotlib, plotly
- **UI Bileşenleri**: Font Awesome icons

### Analiz Algoritmaları
1. **Süre Hesaplama**: End Time - Start Time farkı (dakika cinsinden)
2. **Frekans Analizi**: pandas value_counts() kullanımı
3. **Geçiş Matrisi**: Her case için sıralı aktivite çiftlerini sayma
4. **Süreç Akışı**: Network grafiği ile aktivite bağlantılarını gösterme

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: İş Süreci Analizi
- Müşteri başvuru süreçlerini analiz etme
- Hangi adımların en uzun sürdüğünü bulma
- Süreç darboğazlarını tespit etme

### Senaryo 2: Sistem Log Analizi
- Yazılım süreçlerinin performans analizi
- Hata noktalarını belirleme
- Optimizasyon fırsatlarını keşfetme

## 🚨 Hata Giderme

### Yaygın Hatalar
1. **"Eksik sütunlar" hatası**: CSV dosyanızda gerekli sütunların bulunduğundan emin olun
2. **Tarih formatı hatası**: Tarih sütunlarının YYYY-MM-DD HH:MM:SS formatında olduğunu kontrol edin
3. **Port hatası**: 5000 portu kullanımda ise app.py'de farklı bir port belirleyin

### Destek
Herhangi bir sorun yaşarsanız:
1. Terminal/komut satırındaki hata mesajlarını kontrol edin
2. CSV dosyanızın format gereksinimlerini karşıladığından emin olun
3. Python ve pip sürümlerinizi kontrol edin

## 📈 Gelecek Geliştirmeler

- [ ] Excel dosyası desteği
- [ ] Daha gelişmiş BPMN diyagramları
- [ ] Süreç performans metrikleri
- [ ] Veri filtreleme özellikleri
- [ ] PDF rapor çıktısı
- [ ] Veritabanı entegrasyonu

## 👨‍💻 Geliştirici Notları

Bu uygulama eğitim amaçlı geliştirilmiştir ve süreç madenciliği temel kavramlarını öğretmeyi hedefler. Gerçek üretim ortamında kullanım için ek güvenlik ve performans optimizasyonları gerekebilir.

---

**Süreç Madenciliği Dersi Projesi**  
*Mini Süreç Madenciliği Uygulaması v1.0*
