from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from mysql_db import MySQL
import math
import bleach
import os

app = Flask(__name__)
application = app

PER_PAGE = 10
PERMITTED_PARAMS = ["title", "short_desc", "year", "publisher", "author", "size"]

app.config.from_pyfile('config.py')
db = MySQL(app)

from auth import bp as bp_auth, init_login_manager, check_rights

init_login_manager(app)
app.register_blueprint(bp_auth)

def getParams(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None 
    return result

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = """SELECT 
                b.*, 
                GROUP_CONCAT(g.name SEPARATOR ', ') AS genres,
                c.file_name,
                COUNT(DISTINCT r.id) AS reviews_count,
                TRUNCATE(AVG(r.grade), 1) AS avg_review_grade
                FROM book b
                INNER JOIN book_has_genres bg ON b.id = bg.book_id
                INNER JOIN genres g ON bg.genres_id = g.id
                LEFT JOIN covers c ON b.covers_id = c.id
                LEFT JOIN reviews r ON b.id = r.book_id
                GROUP BY b.id, b.title, b.description, b.year, b.publisher, b.author, b.size, b.covers_id
                ORDER BY b.year DESC
                LIMIT %s
                OFFSET %s
                ;"""
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query,(PER_PAGE, PER_PAGE * (page - 1)))
        db_books = cursor.fetchall() 
    query = 'SELECT count(*) as page_count FROM book' 
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        db_counter = cursor.fetchone().page_count
    page_count = math.ceil(db_counter / PER_PAGE)
    return render_template('index.html',books = db_books, page = page,page_count = page_count)

def getBook(book_id):
    query = """
            SELECT * FROM book WHERE id = %s
    """
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()
    return book

def getGenres(book_id):
    query = """
                SELECT genres.id, genres.name FROM book
                JOIN book_has_genres ON book.id = book_has_genres.book_id
                JOIN genres ON book_has_genres.genres_id = genres.id
                WHERE book.id = %s
    """
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id,))
        genres = cursor.fetchall()
    query = """
                SELECT * FROM genres
    """
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        allgenres = cursor.fetchall()
    edited_genres = [ str(genre.id) for genre in genres]
    return allgenres, edited_genres

@app.route('/books/<int:book_id>/edit', methods=['GET'])
@login_required
@check_rights("edit")    
def edit(book_id):
    book = getBook(book_id=book_id)
    allgenres, edited_genres = getGenres(book_id=book_id)
    return render_template("books/edit.html", genres = allgenres, book=book, new_genres=edited_genres)

@app.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def delete(book_id):
   
    book = getBook(book_id=book_id)
    try:
        query = """
                SELECT covers.file_name FROM book JOIN covers ON book.covers_id = covers.id WHERE book.id = %s
        """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,)) 
                    cover_name = cursor.fetchone().file_name
        directory = os.getcwd()
        file_path = os.path.join(directory, 'static', 'images', cover_name)
        os.remove(file_path) 
        query ="""
                DELETE FROM book WHERE id=%s;
        """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,)) 
                    db.connection.commit()
        flash(f'Книга {book.title} успешно удалена', 'success')
    except:
        flash('Ошибка при удалении', 'danger')    
    return redirect(url_for('index'))   
   

@app.route('/books/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights("edit")
def update_book(book_id):
    book = getBook(book_id=book_id)
    allgenres, edited_genres = getGenres(book_id=book_id)
    cur_params = getParams(PERMITTED_PARAMS)
    for param in cur_params:
        if cur_params[param]==None:
            flash("Указаны не все параметры", "danger")
            return render_template("books/edit.html", genres = allgenres, book=book, new_genres=edited_genres)
        cur_params[param] = bleach.clean(cur_params[param])
   
    query = """
        UPDATE book SET title=%s, description=%s, author=%s, year=%s, size=%s, publisher=%s WHERE id=%s;
    """
    try:
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(cur_params['title'],cur_params['short_desc'],cur_params['author'],cur_params['year'],cur_params['size'],cur_params['publisher'],book_id)) 
                    db.connection.commit()
        flash(f"Книга '{cur_params['title']}' успешно обновлена", "success")
    except:
        flash("При сохранении возникла ошибка", "danger")
        return render_template("books/edit.html", genres = allgenres, book=book, new_genres=edited_genres)
    return redirect(url_for('show', book_id=book_id))

@app.route('/books/<int:book_id>/add_review', methods=['GET', 'POST'])
@login_required
def review_book(book_id):
    your_review, all_reviews = getReviews(book_id=book_id) 
    query = """
        INSERT INTO reviews (grade, text, users_id, book_id) 
        VALUES (%(grade)s, %(text)s, %(users_id)s, %(book_id)s);
    """
    if your_review!=None:
        flash("Можно добавить только одну рецензию", "warning")
        return redirect(url_for('show', book_id=book_id, all_reviews=all_reviews, your_review=your_review))
    if request.method == 'POST':
        grade = request.form.get('grade')
        params = {
            "grade": grade,
            "text": request.form.get('short_desc'),
            "users_id": current_user.id,
            "book_id": book_id
        }
        if len(params["text"])==0:
            flash("Тест рецензии не должен быть пустым", "warning")
            return redirect(url_for('review_book', book_id=book_id))
        for param in params:
            param = bleach.clean(param)
        try:
            with db.connection.cursor(named_tuple = True) as cursor:
                cursor.execute(query,params=params) 
                db.connection.commit()
            flash("Рецензия успешно добавлена", "success")
            return redirect(url_for('show', book_id=book_id,all_reviews=all_reviews, your_review=your_review))
        except:
            flash('Ошибка при добавлении рецензии', 'danger')
            return redirect(url_for('review_book', book_id=book_id))
    return render_template('add_review.html', book_id = book_id)

def getReviews(book_id):
        your_review = None
        if current_user.is_authenticated: 
            query = """SELECT * FROM reviews WHERE users_id = %s AND book_id = %s ;"""
            with db.connection.cursor(named_tuple = True) as cursor:
                cursor.execute(query,(current_user.id, book_id))
                your_review = cursor.fetchone() 
                query =  """SELECT reviews.*, CONCAT(users.last_name, ' ', users.first_name, ' ', users.middle_name) AS full_name
                            FROM reviews 
                            INNER JOIN users ON reviews.users_id = users.id 
                            WHERE  reviews.users_id != %s AND reviews.book_id = %s;"""
            with db.connection.cursor(named_tuple = True) as cursor:
                cursor.execute(query,(current_user.id, book_id))
                all_reviews = cursor.fetchall() 
        else:
            query =  """SELECT reviews.*, CONCAT(users.last_name, ' ', users.first_name, ' ', users.middle_name) AS full_name
                        FROM reviews 
                        INNER JOIN users ON reviews.users_id = users.id 
                        WHERE reviews.book_id = %s ;"""   
            with db.connection.cursor(named_tuple = True) as cursor:
                cursor.execute(query,(book_id,))
                all_reviews = cursor.fetchall()   
        return your_review,all_reviews

@app.route('/books/<int:book_id>')
def show(book_id):
        query = """SELECT 
                    b.*, 
                    GROUP_CONCAT(g.name SEPARATOR ', ') AS genres,
                    c.file_name,
                    COUNT(DISTINCT r.id) AS reviews_count,
                    TRUNCATE(AVG(r.grade), 1) AS avg_review_grade
                    FROM book b
                    INNER JOIN book_has_genres bg ON b.id = bg.book_id
                    INNER JOIN genres g ON bg.genres_id = g.id
                    LEFT JOIN covers c ON b.covers_id = c.id
                    LEFT JOIN reviews r ON b.id = r.book_id
                    WHERE b.id = %s
                    GROUP BY b.id, b.title, b.description, b.year, b.publisher, b.author, b.size, b.covers_id
                    ;"""
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(query,(book_id,))
            db_book = cursor.fetchone() 
        your_review, all_reviews = getReviews(book_id=book_id)   
        return render_template('books/show.html', book=db_book, your_review=your_review, all_reviews=all_reviews)
