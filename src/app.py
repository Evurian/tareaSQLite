import os
from flask import Flask, jsonify, request, send_from_directory
import sqlite3

app = Flask(__name__)

# Ruta de la base de datos
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imdb.db')

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = query_db('SELECT * FROM Movie')
    return jsonify([{'id': row[0], 'title': row[1], 'year': row[2], 'rating': row[3]} for row in movies])

@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = query_db('SELECT * FROM Movie WHERE id = ?', [movie_id], one=True)
    if movie:
        return jsonify({'id': movie[0], 'title': movie[1], 'year': movie[2], 'rating': movie[3]})
    else:
        return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

