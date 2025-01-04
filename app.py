from flask import Flask,render_template, request
import pickle
import numpy as np
import pandas as pd

try:
    popular_df = pd.read_pickle('popular.pkl')
except Exception as e:
    print(f"Error loading pickle file: {e}")

try:
    pt = pd.read_pickle('pt.pkl')
except Exception as e:
    print(f"Error loading pickle file: {e}")

try:
    books = pd.read_pickle('books.pkl')
except Exception as e:
    print(f"Error loading pickle file: {e}")

try:
    similarity_score = pd.read_pickle('similarity_score.pkl')
except Exception as e:
    print(f"Error loading pickle file: {e}")

#popular_df = pickle.load(open('popular.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Create a list of dictionaries, each representing a book
    books = [
        {
            'title': popular_df['Book-Title'].iloc[i],
            'author': popular_df['Book-Author'].iloc[i],
            'image_url': popular_df['Image-URL-M'].iloc[i],
            'votes': round(popular_df['num_ratings'].iloc[i]),  # Round the number of votes to the nearest integer
            'rating': round(popular_df['avg_rating'].iloc[i], 1)  # Round the average rating to 1 decimal place
        }
        for i in range(len(popular_df))
    ]

    # Pass the list of books to the template
    return render_template('index.html', books=books)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
   
    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)