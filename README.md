# 🍿 PopCornNote

PopCornNote is a full-stack application for managing movies and TV shows.  
You can add titles, organize them by status (to watch, watching, watched, upcoming), fetch details from **TMDb API**, keep track of the last watched episode, and (if you are an administrator) manage registered users.

---

## 🚀 Tech Stack

- **Backend**
  - [FastAPI](https://fastapi.tiangolo.com/) (API server)
  - [MongoDB](https://www.mongodb.com/) (database)
  - [Motor](https://motor.readthedocs.io/) (async MongoDB driver)
  - JWT authentication (`SECRET_KEY`, `HS256`)
  - [python-jose](https://python-jose.readthedocs.io/) for JWT

- **Frontend**
  - [Nuxt 3](https://nuxt.com/) + [Vue 3](https://vuejs.org/) + [Vite](https://vitejs.dev/)
  - [Tailwind CSS](https://tailwindcss.com/) (UI styling)
  - Custom composables (`useAuth`, `useApi`, etc.)
  - Client-side route protection (`auth`, `admin-only` middleware)

- **Third-party API**
  - [TMDb API](https://developer.themoviedb.org/) (movies/TV metadata, posters, cast)

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/
MONGO_DB=popcornnote
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
TMDB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Frontend (`frontend/.env`)

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
NUXT_PUBLIC_TMDB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-repo>/popcornnote.git
cd popcornnote
```

---

### 2. Backend (FastAPI)

1. Navigate into the backend folder:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

   👉 Backend available at: `http://127.0.0.1:8000`

---

### 3. Frontend (Nuxt)

1. Navigate into the frontend folder:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm run dev
   ```

   👉 Frontend available at: `http://localhost:3000`

---

## 👤 Authentication

- **Register:** `POST /auth/register`
- **Login:** `POST /auth/login` → returns a JWT token
- **Profile:** `GET /auth/me` (requires header `Authorization: Bearer <token>`)

---

## 🔑 Roles

- **User** → manage personal movies and TV shows
- **Admin** → access `/admin/users` to:
  - View registered users
  - Check user statistics
  - Delete users (removes their movies/series as well)

To promote a user to **admin**, update their MongoDB document:

```json
"is_admin": true
```

---

## 📊 Main Features

- ✅ Dashboard with search, filters, and personal statistics
- ✅ Add movies/TV shows from TMDb
- ✅ Manage statuses (to_watch, watching, watched, upcoming)
- ✅ Movie/TV detail page with poster background
- ✅ TV shows: season/episode selector + save last watched episode
- ✅ Admin panel: manage users and view global statistics

---

## 🛠 Development Notes

- Backend runs with:

  ```bash
  python -m uvicorn app.main:app --reload
  ```

- Frontend runs with:

  ```bash
  npm run dev
  ```

- Requires a valid **MongoDB Atlas cluster** and **TMDb API Key**.

---
