Bài tâp

## 1. OpenWeather API

OpenWeather API cho phép lấy dữ liệu thời tiết (hiện tại, dự báo, chất lượng không khí...) thông qua HTTP request. 

Một số endpoint:
- `GET /data/2.5/weather?q={city}` : lấy thời tiết hiện tại
- `GET /data/2.5/forecast?q={city}` : dự báo 5 ngày
- `GET /geo/1.0/direct?q={city}` : đổi tên thành phố ra tọa độ

Ví dụ:

GET https://api.openweathermap.org/data/2.5/weather?q=Hanoi&appid=xxx&units=metric&lang=vi

json
{
  "weather": [{ "description": "mây rải rác" }],
  "main": { "temp": 28.5, "humidity": 70 },
  "name": "Hà Nội",
  "cod": 200
}

## 2. TMDB API (The Movie Database)

TMDB là cơ sở dữ liệu phim và TV show, API cho phép tìm kiếm phim, xem chi tiết, lấy danh sách trending, diễn viên... 

**Một số endpoint:**
- `GET /3/movie/popular` – phim đang hot
- `GET /3/movie/{id}` – chi tiết 1 phim
- `GET /3/search/movie?query={tên phim}` – tìm phim
- `GET /3/trending/movie/week` – trending tuần

Ví dụ:

GET https://api.themoviedb.org/3/movie/popular?api_key=xxx&language=vi-VN&page=1

json
{
  "page": 1,
  "results": [
    {
      "id": 912649,
      "title": "Venom: The Last Dance",
      "release_date": "2024-10-22",
      "vote_average": 6.8,
      "poster_path": "/aosm8NMQ3UyoBVpSxyimorCQykC.jpg"
    }
  ],
  "total_pages": 500
}

## 3. Google Maps API

Google Maps Platform gồm nhiều service: bản đồ, tìm đường, geocoding, tìm địa điểm... 
Một số endpoint:
- `GET /maps/api/geocode/json?address={địa chỉ}` – đổi địa chỉ ra tọa độ
- `GET /maps/api/directions/json?origin=A&destination=B` – tìm đường
- `GET /maps/api/place/nearbysearch/json?location={lat,lng}` – tìm địa điểm gần

Ví dụ:
GET https://maps.googleapis.com/maps/api/geocode/json?address=Ho+Chi+Minh+City&key=xxx&language=vi

json
{
  "results": [
    {
      "formatted_address": "Thành phố Hồ Chí Minh, Việt Nam",
      "geometry": {
        "location": { "lat": 10.8230989, "lng": 106.6296638 }
      }
    }
  ],
  "status": "OK"
}


