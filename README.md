# 📚 Book Recommendation System

A **Book Recommendation System** built using **Python**, **Pandas**, and **Scikit-learn**, deployed through a simple **Flask web application**.  
This project suggests books to users based on **collaborative filtering** — finding similarities between users and books from their ratings and preferences.

---

## 🌟 Features

- 🔍 **Search and Recommend** – Type a book name and get the top recommendations instantly.  
- 📊 **Collaborative Filtering** – Uses cosine similarity on user-book ratings to find similar titles.  
- 🧠 **Pre-trained Models** – Quickly loads data and similarity scores from precomputed `.pkl` files.  
- ⚡ **Interactive Web Interface** – Clean and minimal UI for browsing recommendations.  
- 🧰 **Easy to Extend** – You can integrate additional algorithms like SVD or content-based filtering.

---

## 🖼️ Screenshots

| Showcase | Search Feature | Output |
|-----------|----------------|---------|
| ![Showcase](assets/showcase.png) | ![Search Feature](assets/search.png) | ![Output](assets/output.png) |

> 📷 Place your screenshots in an `assets/` folder (e.g., `Book-Recommendation-System/assets/`).  
> If hosted on GitHub, you can also use image URLs from your repo (e.g. `![Showcase](https://github.com/<username>/<repo>/blob/main/assets/showcase.png?raw=true)`).

---

## 🧩 Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| **Language** | Python 3.13 |
| **Libraries** | Pandas, NumPy, Scikit-learn, Flask, Pickle |
| **Frontend** | HTML, CSS, Jinja Templates |
| **Dataset** | Books.csv, Users.csv, Ratings.csv |
| **IDE** | Jupyter Notebook / VS Code |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/RohanMishra101/Book-Recommendation-System.git
cd Book-Recommendation-System
