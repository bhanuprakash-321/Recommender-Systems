# Game Recommendation System (Hybrid Model)
---

## Project Overview
A **powerful game recommender system** using a **hybrid approach** that combines **Content-Based Filtering (CBF)** and **Collaborative Filtering (CF)** to provide **personalized game recommendations**.

The system leverages **game metadata, user ratings, and cosine similarity** to generate high-quality recommendations.

### 🔹 **Recommendation Methods**
- **Content-Based Filtering (CBF)**: Recommends games similar to a given game based on **description, genres, and features**.
- **Collaborative Filtering (CF)**: Recommends games based on **user preferences and ratings**, **filtered for better accuracy**.
- **Hybrid Model**: Combines both approaches using a **weighted score** for improved recommendations.
- **Streamlit App**: A **user-friendly web interface** to search for games and get recommendations.

---

## **Features**
✅ **Game Search** – Search for any game and get recommendations.  
✅ **Hybrid Recommendations** – Uses **70% Content-Based Filtering + 30% Collaborative Filtering** (*default, adjustable*).  
✅ **Genre & Rating Filters** – Filter recommendations based on **genre and user ratings**.  
✅ **Game Metadata** – Fetches **game details** like title, description, genre, platforms, and images from the **RAWG API**.  
✅ **Filtered CF Data** – Includes only:  
   - **Users who have rated at least 20 games** (*ensuring they have a sufficient preference history*).  
   - **Games with at least 40 ratings** (*removing unpopular or obscure games*).  

---

## **Tech Stack**
🔹 **Python** – Core programming language  
🔹 **Pandas, NumPy** – Data processing  
🔹 **Scikit-learn** – Cosine similarity for recommendations  
🔹 **Streamlit** – Interactive web application  
🔹 **APIs Used**: **RAWG API (Game Metadata)**  

---

## **How It Works**
### 1️⃣ **Content-Based Filtering (CBF)**
- Uses **TF-IDF Vectorization** and **Cosine Similarity** to find similar games based on **game descriptions and genres**.  
- **Example:** If you like *Grand Theft Auto V*, you'll see recommendations like *GTA San Andreas* or *Red Dead Redemption*.

### 2️⃣ **Collaborative Filtering (CF)**
- Uses **user ratings and reviews** from **Steam and Metacritic**.
- **Filters users** who have rated **fewer than 20 games** to ensure meaningful recommendations.
- **Excludes games** with **fewer than 40 ratings** to focus on widely rated titles.
- Identifies **users with similar preferences** and recommends **games they liked**.

### 3️⃣ **Hybrid Model (CBF + CF)**
- Merges both models using **weighted scores**:
  ```python
  Hybrid Score = (0.7 * CBF Score) + (0.3 * CF Score)
---

<p>You can access the app using this link:</p>
<a href="https://your-streamlit-app-link" target="_blank">
    <button style="background-color:#4CAF50; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:5px; cursor:pointer;">
        Games Recommender System
    </button>
</a>

