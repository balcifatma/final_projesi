Ziyaretçi Kayıt ve Yönetim Sistemi
Proje Özeti
Bu proje, Flask tabanlı bir web uygulaması olarak ziyaretçilerin kayıt altına alınması, giriş-çıkış saatlerinin takibi ve yönetimi için geliştirilmiştir. 
Proje aynı zamanda kullanıcı bazlı erişim ve yönetim imkanı sağlamaktadır.

Özellikler
Kullanıcı Kaydı ve Girişi: Kullanıcılar sisteme kayıt olabilir ve güvenli şekilde giriş yapabilir.

Ziyaretçi Kaydı: Her kullanıcı kendi ziyaretçilerini ekleyebilir, giriş ve çıkış saatlerini takip edebilir.

Ziyaretçi Listesi: Kullanıcılar kendi ziyaretçi kayıtlarını listeleyebilir ve yönetebilir.

Giriş Kayıtları: Ziyaretçilerin giriş ve çıkış bilgileri detaylı olarak görüntülenebilir.

Yetkilendirme: Her kullanıcının kendi verilerine erişimi sağlanır; kullanıcılar birbirinin verilerine erişemez.

JSON Veri Dışa Aktarımı: Veritabanındaki kullanıcı ve ziyaretçi verileri şifreler gizli tutularak JSON formatında dışa aktarılabilir.

Bootstrap Entegrasyonu: Kullanıcı arayüzü Bootstrap ile modern ve kullanıcı dostu olarak tasarlanmıştır.

Güvenlik: Şifreler Werkzeug kütüphanesi ile hashlenerek güvenli saklanmaktadır.

Çıkış Fonksiyonu: Kullanıcılar sistemden güvenli şekilde çıkış yapabilir.

Teknik Detaylar
Backend: Python, Flask

Veritabanı: SQLite

Şifreleme: Werkzeug güvenli şifreleme (hash)

Frontend: HTML, Bootstrap 5

JSON Export: Veritabanındaki tüm veriler veritabani_json.json dosyasına aktarılır.

Kurulum ve Çalıştırma
Gerekli paketlerin yüklenmesi:

pip install -r requirements.txt
Veritabanı oluşturma:

Uygulama başlatıldığında gerekli tablolar otomatik oluşturulur.

Uygulamanın çalıştırılması:

python app.py
Web tarayıcısında açma:

http://127.0.0.1:5000 adresinden erişilebilir.

Kullanım
Kayıt olarak kullanıcı oluşturun.

Giriş yaptıktan sonra ziyaretçi ekleyebilir ve yönetebilirsiniz.

Yönetim panelinde ziyaretçi sayısı ve son kayıt görüntülenebilir.

Giriş kayıtları sayfasında arama yaparak ziyaretçi kayıtlarını filtreleyebilirsiniz.

"Çıkış Yap" butonu ile güvenli çıkış yapabilirsiniz.

Dosya Yapısı
app.py: Flask uygulama ana dosyası.

templates/: HTML şablonları.

static/: CSS, JS ve diğer statik dosyalar.

veritabani_json.json: Veritabanı verilerinin JSON formatındaki yedeği.

requirements.txt: Proje bağımlılıkları.
