import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

ratings_dict = {
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'movie_id': [1, 2, 3, 1, 2, 4, 2, 3, 4],
    'rating': [5, 4, 3, 4, 5, 2, 2, 5, 4]
}

ratings_df = pd.DataFrame(ratings_dict)

user_item_matrix = ratings_df.pivot_table(index='user_id', columns='movie_id', values='rating')

user_item_matrix = user_item_matrix.fillna(0)

user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def get_collaborative_recommendations(user_id, num_recommendations=3):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]
    similar_user_ratings = user_item_matrix.loc[similar_users]
    user_ratings = user_item_matrix.loc[user_id]
    
    recommendations = {}
    for movie_id in user_item_matrix.columns:
        if user_ratings[movie_id] == 0: 
            weighted_sum = 0
            similarity_sum = 0
            for similar_user in similar_users:
                if similar_user_ratings.loc[similar_user, movie_id] > 0:
                    weighted_sum += user_similarity_df.loc[user_id, similar_user] * similar_user_ratings.loc[similar_user, movie_id]
                    similarity_sum += user_similarity_df.loc[user_id, similar_user]
            if similarity_sum > 0:
                recommendations[movie_id] = weighted_sum / similarity_sum

    recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    return [movie_id for movie_id, score in recommendations][:num_recommendations]

movies_dict = {
    'movie_id': [1, 2, 3, 4],
    'title': ["Movie A", "Movie B", "Movie C", "Movie D"],
    'description': ["Action adventure", "Romantic comedy", "Sci-fi thriller", "Action comedy"]
}

movies_df = pd.DataFrame(movies_dict)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['description'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

movie_indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

def get_content_based_recommendations(title, num_recommendations=3):
    idx = movie_indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df['title'].iloc[movie_indices]

if __name__ == "__main__":
    user_id = 1
    print(f"Collaborative Filtering Recommendations for User {user_id}: {get_collaborative_recommendations(user_id)}")

    title = "Movie A"
    print(f"Content-Based Filtering Recommendations for '{title}': {get_content_based_recommendations(title)}")
