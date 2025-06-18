Ziyaretçi Kayıt Sistemi
Ad Soyad: Fatma Balcı
Öğrenci No: 2311081054
Demo: final-projesi-e1km.onrender.com
GitHub: github.com/balcifatma/final_projesi

1. Projenin Amacı
Bu proje, ofisler, kurumlar veya etkinliklerde ziyaretçi kayıtlarını dijital olarak tutmak, yönetmek ve erişilebilir hale getirmek amacıyla geliştirildi.

Çözülen Problemler:

Kayıtların dağınıklığı ve kaybolma riski

Giriş-çıkış takibinde zorluklar

Kullanıcı bazlı veri ayrımı eksikliği

Gerçek Dünya Kullanım Alanları:

Okullar, ofisler, etkinlikler, fabrikalar, kamu kurumları

2. Projenin Özellikleri ve Kapsamı
Neler Yapabiliyor?
Kullanıcı kayıt ve giriş işlemleri

Ziyaretçi ekleme, listeleme, silme

Giriş-çıkış saatlerinin kaydı

Arama ve filtreleme

JSON dışa aktarım

Dashboard 

Yapamadıkları
Anlık bildirimler

Detaylı kullanıcı rolleri

Gelişmiş grafiksel raporlama

İki faktörlü kimlik doğrulama

3. Kullanılan Teknolojiler
Teknoloji	Açıklama
Python	Flask framework ile backend
HTML5/CSS3	Web arayüzü ve sayfa yapısı
Bootstrap 5	Responsive tasarım
SQLite	Hafif ve yerel veritabanı
Jinja2	Dinamik HTML şablon motoru
Werkzeug	Şifreleme ve güvenlik

4. Proje Yapısı

ziyaretci-kayit-sistemi/
├── app.py                  
├── requirements.txt        
├── veritabani.db           
├── final_versiyon.md
├── rapor.pdf
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── ziyaretci_ekle.html
│   ├── giris_kayitlari.html
│   ├── ziyaretci_listesi.html
│   └── ziyaretci_duzenle.html
├── static/
│   ├── css/
│       └── style.css
└── veritabani_json.json   

5. Kurulum ve Çalıştırma

git clone https://github.com/balcifatma/final_projesi.git
cd ziyaretci-kayit-sistemi
pip install -r requirements.txt
python app.py
Uygulama Adresi
http://localhost:5000

6. Veritabanı Yapısı
users tablosu
Alan	Tür	Açıklama
id	INTEGER	Primary Key
email	TEXT	Benzersiz e-posta
password	TEXT	Hashlenmiş şifre

ziyaretciler tablosu
Alan        Tür	        Açıklama
id	        INTEGER	    "Primary Key
ad_soyad	TEXT	    Ziyaretçi adı
tarih	    TEXT	    Tarih
giris_saati	TEXT	    Giriş saati
cikis_saati	TEXT	    Çıkış saati (nullable)
user_id	    INTEGER	    Foreign Key (users.id)

7. Dashboard Özellikleri
Kullanıcıya özel hoş geldin mesajı

Kartlarla:

Toplam ziyaretçi sayısı

Bu ayın kayıtları

Son kayıt

Ortalama giriş süresi

8. Zorluklar ve Öğrenilenler
Yaşanan Sorunlar
Kullanıcıya özel veri filtreleme

Şifre güvenliği ve oturum yönetimi

JSON dışa aktarım senkronizasyonu

Bootstrap ile arayüz tutarlılığı

Çözümler
user_id ile ilişkili veri modeli

generate_password_hash ve check_password_hash kullanımı

JSON dosyasına sadece şifresiz veri ekleme

base.html ile tek tip şablon tasarımı

Öğrenilenler
Flask ile tam işlevli web uygulaması geliştirme

Session ve kullanıcı doğrulama sistemi

SQL ve JSON veri yönetimi

HTML/CSS/Bootstrap ile UI geliştirme

Proje organizasyonu ve hata ayıklama

9. Geliştirme Fikirleri
Admin ve kullanıcı rollerinin ayrılması

Grafik tabanlı ziyaretçi analizleri

Mobil uyumlu arayüz 

API desteği ile entegrasyon

Şifre sıfırlama ve OTP desteği

Gerçek zamanlı bildirim sistemi

Çoklu dil desteği 

Otomatik veritabanı yedekleme sistemi
