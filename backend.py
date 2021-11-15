"""Code for parsing the backend of the Pokedex program
Starter code by David Szeto. Implementation by the CSCA20 student.
"""


import sqlite3

import const


def get_con_cur(db_filename):
    """Returns an open connection and cursor associated with the sqlite
    database associated with db_filename.

    Args:
        db_filename: (str) the filename of the db to which to connect

    Returns: a tuple of:
        -an open connection to the sqlite database
        -an open cursor associated with the connection
    """
    # Enter your code here
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    return con, cur


def close_con_cur(con, cur):
    """Commits changes and closes the given cursor and connection to a sqlite
    database.

    Args:
        con: an open sqlite3 connection to a database
        cur: a cursor associated with con

    Returns:
        None
    """
    # Enter your code here
    cur.close()
    con.commit()
    con.close()


def table_exists(cur):
    """Returns whether the pokemon table already exists in the database and
    whether it is non-empty

    Args:
        cur: an open sqlite3 cursor created from a connection to the pokemon db
    """
    # This function has already been implemented for you. You don't need to do
    # anything with it except call it in the appropriate location!
    query = 'SELECT * FROM pokemon'
    try:
        cur.execute(query)
    except sqlite3.OperationalError:
        return False
    return cur.fetchone() is not None


def create_table(csv_filename, con, cur):
    """(Re-)creates the pokemon table in the database

    In the SQLite cursor cur, drops the pokemon table if it already exists, and
    re-creates it. Fills it with the information contained in the CSV file
    denoted by csv_filename. Afterwards, commits the changes through the given
    connection con.

    Implicitly converts all strs in the loaded data to lower-case before
    insertion into the database.

    Args:
        csv_filename: (str) the filename of the CSV file containing the pokemon
        information
        con: an open connection to the sqlite database
        cur: an open cursor associated with the connection

    Returns:
        None
    """
    # Drop and re-create the pokemon table
    # Enter your code here
    cur.execute('DROP TABLE IF EXISTS pokemon')

    # Build the table
    # Enter your code here
    cur.execute('CREATE TABLE pokemon(name TEXT, species_id INTEGER, '
                'height REAL, weight REAL, type_1 TEXT, type_2 TEXT, '
                'url_image TEXT,generation_id INTEGER, '
                'evolves_from_species_id TEXT)')
    with open(csv_filename) as f:
        idx = parse_header(f)
        for line in f:
            l = line.split(const.SEP)
            cur.execute('INSERT INTO pokemon VALUES (?,?,?,?,?,?,?,?,?)',
                        (l[idx['pokemon']],
                         int(l[idx['species_id']]), float(l[idx['height']]),
                         float(l[idx['weight']]), l[idx['type_1']],
                         l[idx['type_2']], l[idx['url_image']],
                         int(l[idx['generation_id']]),
                         l[idx['evolves_from_species_id']]))
    # Commit your changes
    # Enter your code here
    con.commit()


def get_pokemon_names(cur):
    """Returns a list of pokemon names in the database (as strs) sorted in
    alphabetical order

    Args:
        cur: an open sqlite3 cursor created from a connection to the pokemon db
    """
    # Enter your code here
    result = []
    cur.execute('SELECT name FROM pokemon')
    for row in cur:
        result += row
    return unique_and_sort(result)


def get_stats_by_name(name, cur):
    """Returns the stats of the pokemon with the given name as stored in the
    database.

    Args:
        name: the pokemon's name
        cur: an open sqlite3 cursor created from a connection to the pokemon db

    Returns: a tuple of
        -the pokemon's name (str)
        -the pokemon's species id (int)
        -the pokemon's height (float)
        -the pokemon's weight (float)
        -the pokemon's type 1 (str)
        -the pokemon's type 2 (str)
        -the pokemon's url image (str)
        -the pokemon's generation (int)
        -the species id from which the pokemon evolves (str)
    """
    # Enter your code here
    result = ()
    cur.execute('SELECT * FROM pokemon '
                'WHERE name = (?)', (name,))
    for row in cur:
        result += row
    return result


def get_pokemon_ids(cur):
    """Returns a list of pokemon (species) ids (as ints) sorted in increasing
    order as stored in the database.

    Args:
        cur: an open sqlite3 cursor created from a connection to a pokemon db
    """
    # Enter your code here
    result = []
    cur.execute('SELECT species_id FROM pokemon')
    for row in cur:
        result += row
    return unique_and_sort(result)


def get_stats_by_id(species_id, cur):
    """Returns the stats of the pokemon with the given species id as stored in
    the database.

    Args:
        species_id: the pokemon's species id (int)
        cur: an open sqlite3 cursor created from a connection to the pokemon db

    Returns: a tuple of
        -the pokemon's name (str)
        -the pokemon's species id (int)
        -the pokemon's height (float)
        -the pokemon's weight (float)
        -the pokemon's type 1 (str)
        -the pokemon's type 2 (str)
        -the pokemon's url image (str)
        -the pokemon's generation (int)
        -the species id from which the pokemon evolves (str)
    """
    # Enter your code here
    result = ()
    cur.execute('SELECT * FROM pokemon '
                'WHERE species_id = (?)', (species_id,))
    for row in cur:
        result += row
    return result


def unique_and_sort(ell):
    """Returns a copy of ell which contains all unique elements of ell sorted
    in ascending order.

    Args:
        ell: a list that can be sorted
    """
    # This function has already been implemented for you. You don't need to do
    # anything with it except call it in the appropriate location!
    return sorted(set(ell))


def get_pokemon_types(cur):
    """Returns a list of distinct pokemon types (strs) sorted in alphabetical
    order.

    Both type_1 and type_2 are treated as types.

    Args:
        cur: an open sqlite3 cursor created from a connection to the pokemon db
    """
    # Enter your code here
    result = []
    cur.execute('SELECT type_1, type_2 FROM pokemon')
    for row in cur:
        result += row
    return unique_and_sort(result)


def get_pokemon_by_type(pokemon_type, cur):
    """Returns a list of pokemon names (strs) of all pokemon of the given type,
    where the list is sorted in alphabetical order.

    Args:
        pokemon_type: the pokemon type (which may be a type_1 or type_2) (str)
        cur: an open sqlite3 cursor created from a connection to the pokemon db
    """
    # Enter your code here
    cur.execute('SELECT name '
                'FROM pokemon WHERE type_1 = (?)', (pokemon_type,))
    list_type1 = []
    for row in cur:
        list_type1 += row
    cur.execute('SELECT name '
                'FROM pokemon WHERE type_2 = (?)', (pokemon_type,))
    list_type2 = []
    for row in cur:
        list_type2 += row
    result = list_type1 + list_type2
    return unique_and_sort(result)


def parse_header(f):
    """Parses the header and builds a dict mapping column name to index

    Args:
        f: a freshly opened file in the format of pokemon.csv

    Returns:
        a dict where:
            -each key is one of:
                'pokemon', 'species_id', 'height', 'weight', 'type_1',
                'type_2', 'url_image', 'generation_id',
                'evolves_from_species_id'
            -each value is the index of the corresponding key in the CSV file
                starting from column 0.
                eg. If 'pokemon' is in the second column, then its index will
                be 1. If 'species_id' is the third column, then its index will
                be 2.
    """
    columns = ['pokemon', 'species_id', 'height', 'weight', 'type_1', 'type_2',
               'url_image', 'generation_id', 'evolves_from_species_id']
    # Enter your code here
    result = {}
    list_header = f.readline().split(const.SEP)
    for name in columns:
        result[name] = list_header.index(name)
    return result
