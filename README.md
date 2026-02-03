# 🎬 Movie Recommendation System

A **Netflix-style Movie Recommendation System** built using **Python**, **Streamlit**, and the **TMDB API**, implementing **content-based filtering** to recommend similar movies with rich details.

🔗 **Live App**:  
https://movie-recommender-wlaesuatfq2nzttgq4ussw.streamlit.app/

---

## 🚀 Features

- 🎥 Content-based movie recommendations
- 🖼️ Movie posters fetched from TMDB
- 🎭 Genre, Director & Top Cast details
- 🔗 Direct links to watch movies (TMDB page)
- ⚡ Fast similarity-based recommendations
- 🌐 Deployed on Streamlit Community Cloud

---

## 🧠 How It Works

1. Movies are represented using textual features
2. Similarity between movies is computed using **cosine similarity**
3. When a user selects a movie:
   - The most similar movies are identified
   - Movie metadata is fetched from **TMDB API**
4. Results are displayed with posters and details

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Machine Learning**: Scikit-learn  
- **Data Handling**: Pandas, NumPy  
- **API**: TMDB (The Movie Database)  
- **Deployment**: Streamlit Community Cloud  

---

## 📁 Project Structure

```
movie-recommender/
│
├── app.py              # Streamlit application
├── movies.pkl          # Movie metadata
├── requirements.txt    # Project dependencies
├── .gitignore          # Ignored files
└── README.md           # Project documentation
```

> ⚠️ `similarity.pkl` is intentionally excluded due to GitHub size limits.

---

## 🔐 TMDB API Setup

### 1️⃣ Get TMDB API Key
- Visit: https://www.themoviedb.org/
- Create an account
- Generate an API key

### 2️⃣ Add API Key to Streamlit Secrets

```toml
TMDB_API_KEY = "your_api_key_here"
```

### 3️⃣ Access in Code

```python
API_KEY = st.secrets["TMDB_API_KEY"]
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/Anto-211205/movie-recommender.git
cd movie-recommender

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

---

## 📈 Future Improvements

- Collaborative filtering
- Hybrid recommender system
- User profiles & history
- Advanced UI animations

---

## 👤 Author

**Anto**  
AI / ML Enthusiast  
Python & Data Science Developer
