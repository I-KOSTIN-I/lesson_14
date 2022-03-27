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
    for i in get_value_from_db(sql=f'''
    SELECT *
    FROM netflix
    WHERE "cast" LIKE '{name_1}' AND "cast" LIKE '{name_2}'
    ORDER BY release_year
    '''):
        return dict(i)