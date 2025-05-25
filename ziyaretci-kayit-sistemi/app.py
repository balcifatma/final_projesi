from flask import Flask, render_template, redirect, url_for, request, g, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import session
from flask import jsonify 
import json
from flask import Response

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Flash mesajlar için gereklidir

DATABASE = "veritabani.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session.clear()
            session['user_id'] = user['id']  # Burada user_id sessiona kaydediliyor
            flash("Giriş başarılı!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Hatalı e-posta veya şifre.", "danger")
            return render_template("login.html")
    return render_template("login.html")


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            db.commit()
            flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Bu e-posta zaten kayıtlı.", "danger")
            return render_template("register.html")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Öncelikle giriş yapmalısınız.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    toplam_ziyaretci = db.execute(
        "SELECT COUNT(*) FROM ziyaretciler WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    son_ziyaretci = db.execute(
        "SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)
    ).fetchone()

    return render_template("dashboard.html",
                           toplam_ziyaretci=toplam_ziyaretci,
                           son_ziyaretci=son_ziyaretci)



@app.route('/ziyaretci_ekle', methods=['GET', 'POST'])
def ziyaretci_ekle():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        giris_saati = request.form.get('giris_saati')
        cikis_saati = request.form.get('cikis_saati')

        from datetime import date
        tarih = date.today().strftime('%Y-%m-%d')

        user_id = session.get('user_id', 1)  # Burada session'dan user_id alıyoruz, yoksa 1 olarak default

        db = get_db()
        db.execute(
            "INSERT INTO ziyaretciler (ad_soyad, tarih, giris_saati, cikis_saati, user_id) VALUES (?, ?, ?, ?, ?)",
            (ad_soyad, tarih, giris_saati, cikis_saati or '', user_id)
        )
        db.commit()

        flash("Ziyaretçi başarıyla eklendi.", "success")
        return redirect(url_for('ziyaretci_listesi'))

    return render_template('ziyaretci_ekle.html')


@app.route('/ziyaretci_listesi')
def ziyaretci_listesi():
    user_id = session.get('user_id', 1)  # sessiondan alıyoruz
    db = get_db()
    ziyaretciler = db.execute("SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    return render_template('ziyaretci_listesi.html', ziyaretciler=ziyaretciler)

@app.route('/ziyaretci_sil/<int:ziyaretci_id>')
def ziyaretci_sil(ziyaretci_id):
    db = get_db()
    cursor = db.execute("DELETE FROM ziyaretciler WHERE id = ?", (ziyaretci_id,))
    db.commit()

    if cursor.rowcount == 0:
        flash("Silinecek ziyaretçi bulunamadı.", "warning")
    else:
        flash("Ziyaretçi kaydı silindi.", "success")

    return redirect(url_for('ziyaretci_listesi'))


@app.route("/giris_kayitlari")
def giris_kayitlari():
    user_id = session.get('user_id')
    if not user_id:
        flash("Öncelikle giriş yapmalısınız.", "warning")
        return redirect(url_for("login"))

    query = request.args.get('query', '').strip()
    db = get_db()
    
    if query:
        kayitlar = db.execute(
            "SELECT * FROM ziyaretciler WHERE user_id = ? AND ad_soyad LIKE ? ORDER BY tarih DESC, giris_saati DESC",
            (user_id, f"%{query}%")
        ).fetchall()
    else:
        kayitlar = db.execute(
            "SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY tarih DESC, giris_saati DESC",
            (user_id,)
        ).fetchall()

    return render_template("giris_kayitlari.html", kayitlar=kayitlar)



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Eğer session kullanıyorsan, temizle
    flash("Başarıyla çıkış yapıldı.", "success")
    return redirect(url_for('login'))



def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tarih TEXT NOT NULL,
            giris_saati TEXT NOT NULL,
            cikis_saati TEXT
        )
        """)
        conn.commit()

@app.route('/veritabani_json')
def veritabani_json():
    db = get_db()
    
    users = db.execute("SELECT id, email FROM users").fetchall()
    ziyaretciler = db.execute("SELECT * FROM ziyaretciler").fetchall()

    data = {
        "users": [dict(user) for user in users],
        "ziyaretciler": [dict(z) for z in ziyaretciler]
    }
    
    # JSON string oluştur
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    
    # Dosyaya kaydet
    with open("veritabani_json.json", "w", encoding="utf-8") as f:
        f.write(json_data)
    
    # JSON olarak yanıt dön
    return Response(json_data, mimetype='application/json')

def migrate_add_user_id():
    db = get_db()
    # Sütun var mı kontrol etmek için basit bir sorgu deneyelim
    cursor = db.execute("PRAGMA table_info(ziyaretciler)")
    columns = [col['name'] for col in cursor.fetchall()]
    if 'user_id' not in columns:
        db.execute("ALTER TABLE ziyaretciler ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
        db.commit()

def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tarih TEXT NOT NULL,
            giris_saati TEXT NOT NULL,
            cikis_saati TEXT,
            user_id INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.commit()
    # Bağlantı kapandıktan sonra migrasyonu çalıştır
    with app.app_context():
        migrate_add_user_id()




from flask import Flask, render_template, redirect, url_for, request, g, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import session
from flask import jsonify 
import json
from flask import Response

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Flash mesajlar için gereklidir

DATABASE = "veritabani.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session.clear()
            session['user_id'] = user['id']  # Burada user_id sessiona kaydediliyor
            flash("Giriş başarılı!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Hatalı e-posta veya şifre.", "danger")
            return render_template("login.html")
    return render_template("login.html")


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            db.commit()
            flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Bu e-posta zaten kayıtlı.", "danger")
            return render_template("register.html")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Öncelikle giriş yapmalısınız.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    toplam_ziyaretci = db.execute(
        "SELECT COUNT(*) FROM ziyaretciler WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    son_ziyaretci = db.execute(
        "SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)
    ).fetchone()

    return render_template("dashboard.html",
                           toplam_ziyaretci=toplam_ziyaretci,
                           son_ziyaretci=son_ziyaretci)



@app.route('/ziyaretci_ekle', methods=['GET', 'POST'])
def ziyaretci_ekle():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        giris_saati = request.form.get('giris_saati')
        cikis_saati = request.form.get('cikis_saati')

        from datetime import date
        tarih = date.today().strftime('%Y-%m-%d')

        user_id = session.get('user_id', 1)  # Burada session'dan user_id alıyoruz, yoksa 1 olarak default

        db = get_db()
        db.execute(
            "INSERT INTO ziyaretciler (ad_soyad, tarih, giris_saati, cikis_saati, user_id) VALUES (?, ?, ?, ?, ?)",
            (ad_soyad, tarih, giris_saati, cikis_saati or '', user_id)
        )
        db.commit()

        flash("Ziyaretçi başarıyla eklendi.", "success")
        return redirect(url_for('ziyaretci_listesi'))

    return render_template('ziyaretci_ekle.html')


@app.route('/ziyaretci_listesi')
def ziyaretci_listesi():
    user_id = session.get('user_id', 1)  # sessiondan alıyoruz
    db = get_db()
    ziyaretciler = db.execute("SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    return render_template('ziyaretci_listesi.html', ziyaretciler=ziyaretciler)

@app.route('/ziyaretci_sil/<int:ziyaretci_id>')
def ziyaretci_sil(ziyaretci_id):
    db = get_db()
    cursor = db.execute("DELETE FROM ziyaretciler WHERE id = ?", (ziyaretci_id,))
    db.commit()

    if cursor.rowcount == 0:
        flash("Silinecek ziyaretçi bulunamadı.", "warning")
    else:
        flash("Ziyaretçi kaydı silindi.", "success")

    return redirect(url_for('ziyaretci_listesi'))


@app.route("/giris_kayitlari")
def giris_kayitlari():
    user_id = session.get('user_id')
    if not user_id:
        flash("Öncelikle giriş yapmalısınız.", "warning")
        return redirect(url_for("login"))

    query = request.args.get('query', '').strip()
    db = get_db()
    
    if query:
        kayitlar = db.execute(
            "SELECT * FROM ziyaretciler WHERE user_id = ? AND ad_soyad LIKE ? ORDER BY tarih DESC, giris_saati DESC",
            (user_id, f"%{query}%")
        ).fetchall()
    else:
        kayitlar = db.execute(
            "SELECT * FROM ziyaretciler WHERE user_id = ? ORDER BY tarih DESC, giris_saati DESC",
            (user_id,)
        ).fetchall()

    return render_template("giris_kayitlari.html", kayitlar=kayitlar)



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Eğer session kullanıyorsan, temizle
    flash("Başarıyla çıkış yapıldı.", "success")
    return redirect(url_for('login'))



def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tarih TEXT NOT NULL,
            giris_saati TEXT NOT NULL,
            cikis_saati TEXT
        )
        """)
        conn.commit()

@app.route('/veritabani_json')
def veritabani_json():
    db = get_db()
    
    users = db.execute("SELECT id, email FROM users").fetchall()
    ziyaretciler = db.execute("SELECT * FROM ziyaretciler").fetchall()

    data = {
        "users": [dict(user) for user in users],
        "ziyaretciler": [dict(z) for z in ziyaretciler]
    }
    
    # JSON string oluştur
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    
    # Dosyaya kaydet
    with open("veritabani_json.json", "w", encoding="utf-8") as f:
        f.write(json_data)
    
    # JSON olarak yanıt dön
    return Response(json_data, mimetype='application/json')

def migrate_add_user_id():
    db = get_db()
    # Sütun var mı kontrol etmek için basit bir sorgu deneyelim
    cursor = db.execute("PRAGMA table_info(ziyaretciler)")
    columns = [col['name'] for col in cursor.fetchall()]
    if 'user_id' not in columns:
        db.execute("ALTER TABLE ziyaretciler ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1")
        db.commit()

def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            tarih TEXT NOT NULL,
            giris_saati TEXT NOT NULL,
            cikis_saati TEXT,
            user_id INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.commit()
    # Bağlantı kapandıktan sonra migrasyonu çalıştır
    with app.app_context():
        migrate_add_user_id()





if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
