# 🎬 Cineflix — Movie Recommender System

Cineflix is a professional content-based movie recommendation system designed to help users discover their next favorite movies. It leverages NLP techniques like TF-IDF and cosine similarity to recommend movies based on metadata content such as titles, overviews, and genres.

🌐 Live App: https://movierecommendationsystem-n5gnzhmlbsgmi38huet8n8.streamlit.app/

---



## ✨ Key Features

* 🔍 Smart movie search with dropdown
* 🎤 Voice search support
* 🎬 Beautiful Netflix-style UI
* ⭐ Movie ratings from TMDB
* 🖼️ Dynamic hero banner for selected movie
* 🔥 Trending movies section
* 🎯 Top similar movie recommendations
* ▶ Watch Trailer button
* 🍿 Where to Watch link
* ⚡ Fast parallel API fetching
* 🔽 Load more recommendations

---

## 🧠 How It Works

1. User selects or speaks a movie name
2. System finds the closest matching movie
3. Cosine similarity is used to compute similar movies
4. Movie details are fetched from TMDB API
5. Recommendations are displayed in a Netflix-style layout

---

## 🏗️ Tech Stack

**Frontend & App**

* Streamlit
* HTML/CSS (custom styling)

**Backend & ML**

* Python
* Pandas
* Scikit-learn
* Pickle

**APIs**

* TMDB API (movie data & posters)
* SpeechRecognition (voice input)

**Performance**

* ThreadPoolExecutor (fast parallel fetching)
* Streamlit caching

---

## 📁 Project Structure

```
movie_recommender_system/
│
├── artifacts/
│   ├── movies.pkl
│   └── similarity.pkl
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/cineflix.git
cd cineflix
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🔑 Environment Requirement

Make sure you have:

* Python 3.9+
* Working microphone (for voice search)
* Internet connection (for TMDB API)

---

## 🚀 Future Enhancements

* ❤️ User watchlist
* 🎬 Real-time TMDB trending API
* 🔐 User authentication
* 🌐 Multi-language support
* 📱 Mobile UI optimization
* ☁️ Cloud deployment improvements

---

## 🙌 Acknowledgements

* TMDB for movie data
* Streamlit for the amazing framework
* Open-source community

---

## 👩‍💻 Author

**Navya**

If you like this project, consider giving it a ⭐ on GitHub!

---

## 📜 License

This project is for educational purposes.
