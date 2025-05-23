# Pentest Yönetim Sistemi

Sızma testi projelerini, şirketleri ve bulguları yönetmek için tasarlanmış web tabanlı bir yönetim sistemi.

## Özellikler

- Şirket, proje ve bulgu yönetimi
- Adam-gün havuz takibi
- Proje ekstra adam-gün takibi ve raporlaması
- Otomatik pentest tarihi hatırlatıcıları
- Raporlama özellikleri
- CSV export

## E-posta Bildirimleri

Sistem, aşağıdaki durumlarda e-posta bildirimleri gönderir:

1. **Otomatik Pentest Hatırlatmaları**: Ertesi gün için planlanan pentest projelerinin hatırlatma e-postaları her gün sabah otomatik olarak gönderilir.
2. **Manuel Hatırlatmalar**: Proje görünümünden "Hatırlat" butonuna tıklayarak istediğiniz zaman manuel olarak hatırlatma e-postaları gönderebilirsiniz.

## E-posta Yapılandırması

E-posta göndermek için aşağıdaki ortam değişkenleri yapılandırılmalıdır:

```
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_username
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=noreply@example.com
ADMIN_EMAIL=admin@example.com
APP_URL=http://your-app-url
```

Bu ortam değişkenleri `docker-compose.yml` dosyasında belirtilebilir:

```yaml
services:
  app:
    environment:
      - MAIL_SERVER=smtp.example.com
      - MAIL_PORT=587
      - MAIL_USERNAME=your_username
      - MAIL_PASSWORD=your_password
      - MAIL_DEFAULT_SENDER=noreply@example.com
      - ADMIN_EMAIL=admin@example.com
      - APP_URL=http://your-app-url
```

## Komut Satırı Araçları

Projede kullanılabilecek komut satırı araçları:

```bash
# Pentest hatırlatma e-postalarını manuel olarak göndermek için
flask send-pentest-reminders
```

## Kurulum

```bash
# Depoyu klonla
git clone https://github.com/user/pentest-management.git
cd pentest-management

# Docker Compose ile başlat
docker-compose up -d
```

## Geliştirme

```bash
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Geliştirme sunucusunu başlat
flask run
```

## Technology Stack

- **Backend**: Python with Flask
- **Database**: PostgreSQL (or SQLite for development)
- **Frontend**: Bootstrap 5 for responsive design
- **Containerization**: Docker and Docker Compose

## Application Structure

- `app/`: Main application package  
  - `models/`: Database models  
  - `views/`: View functions and routes  
  - `forms/`: Form classes  
  - `templates/`: HTML templates  
  - `static/`: Static files (CSS, JS, etc.)
- `app.py`: Application entry point
- `Dockerfile`: Docker configuration
- `docker-compose.yml`: Docker Compose configuration

## License

This project is licensed under the MIT License.
