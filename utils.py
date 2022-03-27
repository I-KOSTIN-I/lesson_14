import json
import sqlite3


def get_value_from_db(sql):
    with sqlite3.connect('netflix.db') as connect:
        connect.row_factory = sqlite3.Row
        result = connect.execute(sql).fetchall()

    return result


def search_by_title(title):
    for i in get_value_from_db(sql=f'''
    SELECT *
    FROM netflix
    WHERE title = '{title}'
    ORDER BY release_year
    '''):
        return dict(i)


def search_cast(name_1, name_2):
    response = get_value_from_db(sql=f'''
    SELECT *
    FROM netflix
    WHERE "cast" LIKE '%{name_1}%' AND "cast" LIKE '%{name_2}%'
    ORDER BY release_year
    ''')

    names = []
    results = []

    for i in response:
        actrs = (dict(i).get('cast').split(', '))
        for k in actrs:
            names.append(k)

    names = set(names) - set([name_1, name_2])

    for name in names:
        count = 0
        for i in response:
            if name in dict(i).get('cast'):
                count += 1

        if count > 2:
            results.append(name)

    return results


def search_film_or_tv_show(type_video, year, genre):
    response = get_value_from_db(sql=f'''
    SELECT *
    FROM netflix
    WHERE "type" = '{type_video}'
    AND release_year = '{year}'
    AND listed_in LIKE '%{genre}%'
    ''')

    results = []
    for i in response:
        results.append(dict(i))
    return json.dumps(results, indent=4)


# print(search_cast('Rose McIver', 'Ben Lamb'))
# print(search_film_or_tv_show('TV Show', '2019', 'TV'))
