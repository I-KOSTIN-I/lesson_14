import flask
import json
from utils import search_by_title, get_value_from_db

app = flask.Flask(__name__)


@app.route('/movie/<title>')
def search_title_view(title):
    response = search_by_title(title=title)
    data = {}
    for key in response.keys():
        if key in ['title', 'country', 'release_year', 'genre', 'description']:
            data[key] = response[key]

    return app.response_class(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/movie/<int:year_1>/to/<int:year_2>/')
def search_release_year_view(year_1, year_2):
    response = get_value_from_db(
        sql=f'''
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN '{year_1}' AND '{year_2}'
        LIMIT 100
        ''')
    data = []
    for i in response:
        data.append(dict(i))

    return app.response_class(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/rating/<rating>')
def search_rating_view(rating):
    rating_dictionary = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    if rating in rating_dictionary:
        response = get_value_from_db(
            sql=f'''
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN {set(rating_dictionary[rating])}
            ''')
    else:
        response = {'description': 'Category not found'}

    data = []
    for i in response:
        data.append(dict(i))

    return app.response_class(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/genre/<genre>')
def search_genre_view(genre):
    response = get_value_from_db(
        sql=f'''
           SELECT *
           FROM netflix
           WHERE listed_in LIKE '%{genre}%'
           ORDER BY release_year
           LIMIT 10
           ''')
    data = []
    for i in response:
        data.append(dict(i))

    return app.response_class(response=json.dumps(data), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
