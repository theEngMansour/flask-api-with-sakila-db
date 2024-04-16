from flask import Flask, jsonify, abort, request
import mysql.connector;

# config
app = Flask(__name__)
db = mysql.connector.connect(user='root', password='mansour', host='localhost', database='sakila')

# Routes
@app.route('/actors')
def actors():
    query = 'SELECT * FROM actor'
    return get_results(query)

@app.route('/actors/<int:actor_id>')
def actor(actor_id):
    query = 'SELECT * FROM actor WHERE actor_id = %s'
    return get_one_result(query, (actor_id,))

@app.route('/film')
def get_film_by_rating():
    ratings = request.args['rating'].split(',')
    query_placeholders = ','.join(['%s'] * len(ratings))
    query = 'SELECT title, rating FROM film WHERE rating IN (%s)' %query_placeholders
    return get_results(query, ratings)

# Helper functions Mysql
def get_results(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results) if results else abort(404)

def get_one_result(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    result = cursor.fetchone()
    cursor.close()
    return jsonify(result) if result else abort(404)
    
if __name__ == "__main__":
    app.run(debug=True) 