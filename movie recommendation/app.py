import pickle
from flask import Flask,render_template,request
import numpy as np
import tensorflow as tf

#open pickle file
movies = pickle.load(open('movies.pkl','rb'))
similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))
sparse_matrix = pickle.load(open('sparse_mat.pkl','rb'))
popular_df = pickle.load(open('popular.pkl','rb'))

#app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           movie_name = list(popular_df['movie_name'].values),
                           movie_id=list(popular_df['movie_id'].values),
                           popularity_index=list(popular_df['popularity_index'].values),
                           votes=list(popular_df['ratingcount'].values),
                           rating=list(popular_df['ratingmean'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(movies.title== user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_matrix[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = movies.iloc[i[0]]
        item.append(temp_df['title'])
        item.append(temp_df['release_date'])
        item.append(temp_df['imdb_url'])
        item.append(temp_df['all_genres'])
        item.append(i[1])
        item.append(popular_df.iloc[i[0]]['popularity_index'])
        item.append(popular_df.iloc[i[0]]['ratingmean'])
        item.append(popular_df.iloc[i[0]]['ratingcount'])

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)