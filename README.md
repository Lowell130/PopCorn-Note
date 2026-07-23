# PopCornNote 🎬

PopCornNote is a web application to manage your movie and TV show collection, track progress, and fetch metadata directly from **TMDb API**.  
It also integrates with the **VixSrc API** to provide streaming links for TV show episodes.

---

## 🚀 Features

- User authentication (JWT-based)
- Add movies/TV shows manually or via **TMDb API**
- Track statuses: `to_watch`, `watching`, `watched`, `upcoming`
- **Release Calendar**: Tracking and precise countdowns for upcoming titles from your collection (excluding already released titles)
- **PopcornBot (AI Assistant)**: Receive personalized recommendations, trivia, and collection advice from an integrated smart chatbot
- Rate and add notes
- Dashboard with user statistics
- **Admin Dashboard**: Manage registered users, configure the AI Assistant, simulate community activities (fake users/activities), and sync TMDb metadata in the background (votes, runtimes, overviews, cast, directors, and poster URLs)
- Streaming integration via **VixSrc API**

---

## 🛠 Tech Stack

- **Backend**: FastAPI + MongoDB
- **Frontend**: Nuxt 3 + Vue 3 + TailwindCSS
- **Database**: MongoDB (Atlas or local instance)
- **External APIs**:
  - [TMDb API](https://developers.themoviedb.org/) – for metadata (posters, cast, episodes, etc.)
  - [VixSrc API](https://vixsrc.to/) – for video streaming

---

## 📂 Project Structure

```
backend/   → FastAPI app (routes, schemas, DB connection)
frontend/  → Nuxt 3 app (Vue components, pages, layouts)
```

---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-repo/popcornnote.git
cd popcornnote
```

### 2. Backend setup
```bash
cd backend
pip install -r requirements.txt
```

Configure your `.env` file:
```env
MONGO_URI=your-mongodb-uri
MONGO_DB=popcornnote
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
TMDB_API_KEY=your-tmdb-api-key
```

Run the backend:
```bash
uvicorn app.main:app --reload
```

### 3. Frontend setup
```bash
cd frontend
npm install
```

Configure your `.env` file:
```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
NUXT_PUBLIC_TMDB_API_KEY=your-tmdb-api-key
```

Run the frontend:
```bash
npm run dev
```

### ⚡ Quick Start (Windows)
You can run both the backend and frontend concurrently using the helper script in the root directory:
```powershell
./start.ps1
```

---

## 🔑 Admin Access

To grant admin access, add `"is_admin": true` to a user document in your MongoDB collection.  
Admins can access the `/admin/users` page to view and manage registered users, simulate community activity, configure PopcornBot AI, and trigger background metadata sync.

---

## 📌 Notes

- Make sure MongoDB is running (Atlas or local instance).
- Requires valid **TMDb API Key** and access to **VixSrc API**.
- Default frontend runs at [http://localhost:3000](http://localhost:3000)  
  Backend runs at [http://127.0.0.1:8000](http://127.0.0.1:8000)
