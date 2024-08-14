from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

# Load the data from pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Pass popular books data to the template
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author_x'].values),
                           image=list(popular_df['Image-URL-M_x'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg-rating'].values))

@app.route("/recommend_book", methods=["POST"])
def recommend_book():
    book_name = request.form.get('book_name')
    data = []
    searched_book_name = book_name
    try:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:20]

        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.append(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.append(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.append(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
    except IndexError:
        # If the book is not found in the index, data remains empty
        pass

    # Always pass popular books data along with search results (if any)
    return render_template('index.html',
                           searched_book_name=searched_book_name,
                           data=data,
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author_x'].values),
                           image=list(popular_df['Image-URL-M_x'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg-rating'].values))

# New route for real-time search recommendations
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query', '')
    if query:
        # Filter the books DataFrame based on the search query
        recommendations = books[books['Book-Title'].str.contains(query, case=False, na=False) |
                                books['Book-Author'].str.contains(query, case=False, na=False)]
        
        # Prepare the results to be sent as JSON
        results = recommendations[['Book-Title', 'Book-Author', 'Image-URL-M']].drop_duplicates().head(10).to_dict(orient='records')
        print(results)  # Print the results to check the structure
        return jsonify(results)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
