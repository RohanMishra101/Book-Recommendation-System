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

    if not book_name:  # Check if the input is empty
        return render_template('index.html', error_message="Please enter a book name to search for recommendations.")

    data = []
    searched_book_name = book_name  # Capture the searched book name

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

    if not data:  # Check if no related books were found
        return render_template('index.html', 
                               searched_book_name=searched_book_name,
                                no_results=True,
                                data=data,
                                book_name=list(popular_df['Book-Title'].values),
                                author=list(popular_df['Book-Author_x'].values),
                                image=list(popular_df['Image-URL-M_x'].values),
                                votes=list(popular_df['num-ratings'].values),
                                rating=list(popular_df['avg-rating'].values))

    # Pass the searched book name along with the data
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
    query = request.args.get('query', '').strip().lower()  # Convert query to lowercase for case-insensitive comparison
    if query:
        # Filter the books DataFrame to find any books whose title matches the current input
        matching_books = books[books['Book-Title'].str.lower().str.contains(query, na=False)].drop_duplicates('Book-Title')

        results = []
        for book_name in matching_books['Book-Title'].head(10):  # Limit to 10 matching books
            try:
                index = np.where(pt.index == book_name)[0][0]
                similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]  # Limit to top 5 similar books

                for i in similar_items:
                    temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                    result = {
                        "Book-Title": temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
                        "Book-Author": temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
                        "Image-URL-M": temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
                    }
                    results.append(result)
            except IndexError:
                continue

        return jsonify(results)
    else:
        return jsonify([])  # Return an empty list if no query is provided


if __name__ == '__main__':
    app.run(debug=True)
