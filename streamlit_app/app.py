
import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler



# Load game dictionary safely
with open('games_dict.pkl', 'rb') as file:
    games_dict = pickle.load(file)
    new_df = pd.DataFrame(games_dict)


with open('cosine_sim.pkl', 'rb') as f:
     cosine_sim = pickle.load(f)
with open('cosine_cf_sim.pkl', 'rb') as f:
    cosine_cf_sim = pickle.load(f)
pivot_table = pd.read_pickle('pivot_table.pkl')

# Placeholder for similarity matrices (replace with your actual data loading)
#cosine_sim = cosine_similarity(np.random.rand(len(new_df), 10))  # Example placeholder
#cosine_cf_sim = cosine_similarity(np.random.rand(len(new_df), 10))  # Example placeholder
#pivot_table = pd.DataFrame(index=new_df['name'])  # Example placeholder


def cbf_recommend_games(game_name):
    # Get the index of the game that matches the name
    idx = new_df[new_df['name'].str.lower() == game_name.lower()].index[0]

    # Get the cosine similarity scores for the target game
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on similarity scores (exclude the target game itself)
    sorted_sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

    # Get the indices of the recommended games
    game_indices = [score[0] for score in sorted_sim_scores]
    cbf_scores = [score[1] for score in sorted_sim_scores]

    # Prepare the recommended games DataFrame
    recommended_games = pd.DataFrame({
        "game_id": new_df.iloc[game_indices].game_id.values,
        "name": new_df.iloc[game_indices].name.values,
        "cbf_score": cbf_scores
    })
    return recommended_games


def cf_recommend_games(game):
    # Fetch the index of the target game
    index = np.where(pivot_table.index == game)[0][0]

    # Get similarity scores and sort them in descending order
    cf_sim_scores = sorted(list(enumerate(cosine_cf_sim[index])), key=lambda x: x[1], reverse=True)

    # Exclude the target game itself and get the top 10 recommendations
    cf_sim_scores = cf_sim_scores[1:11]

    # Prepare the recommended games DataFrame
    recommended_games = pd.DataFrame(
        [{"game_id": new_df.iloc[i[0]].game_id, "name": pivot_table.index[i[0]], "cf_score": i[1]} for i in
         cf_sim_scores]
    )
    return recommended_games


def hybrid_recommend_games(game_name, cbf_weight=0.7, cf_weight=0.3):
    """
    Generates hybrid game recommendations using a weighted combination of
    content-based filtering (CBF) and collaborative filtering (CF).

    Args:
        game_name: Name of the game to get recommendations for
        cbf_weight: Weight for CBF scores (default 0.7)
        cf_weight: Weight for CF scores (default 0.3)

    Returns:
        DataFrame with top 10 hybrid recommendations
    """
    try:
        # Get content-based recommendations
        cbf_rec = cbf_recommend_games(game_name)

        # Get collaborative filtering recommendations
        try:
            cf_rec = cf_recommend_games(game_name)
            cf_available = True
        except (IndexError, KeyError):
            print(f"No CF recommendations found for '{game_name}'. Using CBF only.")
            cf_rec = cbf_rec[['game_id', 'name']].copy()  # Retain all CBF games
            cf_rec['cf_score'] = 0  # Set CF score to 0
            cf_available = False

        # Merge recommendations
        hybrid_df = pd.merge(
            cbf_rec,
            cf_rec,
            on=['game_id', 'name'],
            how='outer'  # Keep all CBF results even if no CF match
        ).fillna(0)

        # Normalize scores using MinMaxScaler only if more than one unique value
        scaler = MinMaxScaler()

        if hybrid_df['cbf_score'].nunique() > 1:
            hybrid_df['cbf_score'] = scaler.fit_transform(hybrid_df[['cbf_score']])

        if cf_available and hybrid_df['cf_score'].nunique() > 1:
            hybrid_df['cf_score'] = scaler.fit_transform(hybrid_df[['cf_score']])

        # Compute hybrid score
        hybrid_df['hybrid_score'] = (cbf_weight * hybrid_df['cbf_score']) + (cf_weight * hybrid_df['cf_score'])

        # If CF is unavailable, return only CBF results
        if not cf_available:
            return cbf_rec[['game_id', 'name', 'cbf_score']].rename(columns={'cbf_score': 'hybrid_score'}).head(10)

        # Sort and return top 10
        return hybrid_df.sort_values('hybrid_score', ascending=False)[['game_id', 'name', 'hybrid_score']].head(10)

    except Exception as e:
        print(f"Error in hybrid recommendations: {str(e)}")
        return pd.DataFrame()


def get_recommendations(game_name):
    """Wrapper function to get recommendations in the required format"""
    recommendations = hybrid_recommend_games(game_name)

    if recommendations.empty:
        return []

    # Convert to list of dicts with additional game info
    result = []
    for _, row in recommendations.iterrows():
        game_info = new_df[new_df['game_id'] == row['game_id']].iloc[0].to_dict()
        result.append({
            'name': row['name'],
            'cover_image': game_info.get('cover_image', ''),
            'genres': game_info.get('genres', ''),
            'platforms': game_info.get('platforms', ''),
            'rating': game_info.get('rating', ''),
            'game_link': game_info.get('game_link', '')
        })

    return result


# Streamlit UI
st.title("Game Recommender System")

# Dropdown to select a game
selected_game = st.selectbox("Select a game:", new_df["name"].values)

# Button to get recommendations
if st.button("Get Recommendations"):
    recommendations = get_recommendations(selected_game)

    if recommendations:
        for game in recommendations:
            with st.container():
                st.subheader(game["name"])

                # Create two columns
                col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

                # Left Column - Game Image (Fixed size)
                with col1:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; justify-content: center;">
                            <img src="{game['cover_image']}" style="width:100%; height: 200px; object-fit: cover; border-radius: 10px;">
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Right Column - Game Details
                with col2:
                    st.write(f"**Genres:** {game['genres']}")
                    st.write(f"**Platforms:** {game['platforms']}")
                    st.write(f"**Rating:** {game['rating']}/5")
                    st.markdown(f"[🔗 Game Link]({game['game_link']})")

                # Divider
                st.write("-" * 50)

    else:
        st.write("No recommendations found.")