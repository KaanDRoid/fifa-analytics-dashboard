# FIFA Analytics Dashboard Sample Data

Bu klasör FIFA oyuncu verilerini içerir. Gerçek veri dosyaları boyut nedeniyle GitHub'a dahil edilmemiştir.

## Gerekli Veri Dosyaları

Projenin çalışması için aşağıdaki CSV dosyalarına ihtiyaç vardır:

- `male_players.csv` - Erkek oyuncu istatistikleri
- `female_players.csv` - Kadın oyuncu istatistikleri
- `male_teams.csv` - Erkek takım bilgileri (opsiyonel)
- `female_teams.csv` - Kadın takım bilgileri (opsiyonel)
- `male_coaches.csv` - Erkek antrenör bilgileri (opsiyonel)
- `female_coaches.csv` - Kadın antrenör bilgileri (opsiyonel)

## Veri Formatı

CSV dosyaları aşağıdaki sütunları içermelidir:

### Zorunlu Sütunlar
- `player_id`: Benzersiz oyuncu kimliği
- `long_name`: Oyuncu adı
- `overall`: Genel rating (0-100)
- `potential`: Potansiyel (0-100)
- `value_eur`: Piyasa değeri (Euro)
- `age`: Yaş
- `pace`, `shooting`, `passing`, `dribbling`, `defending`, `physic`: Beceri ratings
- `club_name`: Mevcut kulüp
- `player_positions`: Oynadığı pozisyonlar
- `nationality_name`: Uyruk
- `league_name`: Mevcut lig

### Opsiyonel Sütunlar
- `wage_eur`: Maaş
- `height_cm`: Boy
- `weight_kg`: Kilo
- `preferred_foot`: Tercih edilen ayak
- `weak_foot`: Zayıf ayak rating
- `skill_moves`: Beceri hamlesi rating

## Veri Kaynağı

Veri dosyalarını aşağıdaki kaynaklardan edinebilirsiniz:
- EA Sports FIFA veritabanları
- Kaggle FIFA datasets
- SoFIFA.com
