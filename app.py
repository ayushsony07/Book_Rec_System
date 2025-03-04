from flask import Flask,render_template,request
import pandas

import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
Books = pickle.load(open('Books.pkl','rb'))
Similarity_Score = pickle.load(open('Similarity_Score.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                       book_name = list(popular_df['Book-Title'].values),
                           author= list(popular_df['Book-Author'].values),
                          image= list(popular_df['Image-URL-M'].values),
                           votes= list(popular_df['Number of Rating'].values),
                           rating= list(popular_df['Book-Rating'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input )[0][0]
    Similar_item = sorted(list(enumerate(Similarity_Score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in Similar_item:
        item = []
        temp_df = Books[Books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data = data)

if __name__ ==  '__main__':
    app.run(debug=True)

