# Discord Bot - Python Başlangıç Rehberi

Bu basit ama tamamen fonksiyonel bir Discord botu. Adım adım kurulum yapalım!

## 📋 Ön Koşullar
- Python 3.8+ yüklü olmalı
- Discord sunucunuz olmalı (test için)

## 🚀 Kurulum Adımları

### 1. Adım: Discord Bot Token Alma

1. [Discord Developer Portal](https://discord.com/developers/applications)'a gidin
2. "New Application" butonuna tıklayın
3. Bot'a bir isim verin
4. Sol menüden "Bot" seçeneğine tıklayın
5. "Add Bot" butonuna tıklayın
6. "TOKEN" altındaki "Copy" butonuna tıklayın ve token'ı kaydedin

### 2. Adım: Bot İzinlerini Ayarlama

1. Hala Developer Portal'da, "OAuth2" → "URL Generator" seçin
2. **Scopes:**
   - `bot` seçin

3. **Permissions:**
   - Send Messages
   - Ban Members
   - Kick Members
   - Manage Roles
   - Read Message History

4. Alttaki URL'yi kopyalayın ve tarayıcıda açın
5. Botunuzu sunucuya davet edin

### 3. Adım: Kodu Çalıştırma

**Terminal/PowerShell'de:**

```powershell
# Proje klasörüne gidin
cd discord-bot

# Virtual environment oluşturun (ilk seferinde)
python -m venv venv

# Virtual environment'ı etkinleştirin
# Windows için:
venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyası oluşturun
# .env.example'ı kopyalayıp .env olarak yapıştırın
# DISCORD_TOKEN=YOUR_TOKEN_HERE şeklinde değiştirin

# Botu çalıştırın
python bot.py
```

## 📝 Komutlar

### Temel Komutlar
- `!ping` - Bot'un cevap verip vermediğini kontrol edin
- `!merhaba` - Bot size merhaba desin
- `!bilgi [@kullanıcı]` - Kullanıcı bilgisini göster

### Moderasyon Komutları (Admin gerekir)
- `!ban @kullanıcı [sebep]` - Kullanıcıyı banlayın
- `!kick @kullanıcı [sebep]` - Kullanıcıyı sunucudan çıkarın
- `!mute @kullanıcı [sebep]` - Kullanıcıyı susturun
- `!unmute @kullanıcı` - Kullanıcının susturmasını kaldırın

## 🔧 Bot Özellikleri
✅ Komut sistemi
✅ Moderasyon araçları
✅ Hata yönetimi
✅ Embed mesajlar
✅ Kullanıcı izinleri kontrolü

## 💡 İpuçları

1. **Token güvenliği:** Token'ı asla paylaşmayın veya GitHub'a yüklemeyin!
2. **Virtual Environment:** Her zaman virtual environment kullanın
3. **Komut öneki:** `!` ile başlayan komutlar kullanılır, değiştirmek için `bot.py`'da `command_prefix` değişkeni değiştirin

## 🐛 Sorun Giderme

**"Token geçersiz" hatası:**
- `.env` dosyasının doğru olup olmadığını kontrol edin
- Token'ı yeniden kopyalayıp yapıştırın

**Bot sunucuda görünmüyor:**
- Developer Portal'dan tekrar davet edin
- Doğru izinleri seçtiğinizden emin olun

**Komutlar çalışmıyor:**
- Bot'u restart edin
- Konsoldaki hataları kontrol edin

## 📚 Sonraki Adımlar
- Kendi komutlarınızı ekleyin
- Veritabanı entegrasyonu yapın
- Daha gelişmiş moderasyon özellikleri ekleyin

**İyi kodlamalar!** 🎉
