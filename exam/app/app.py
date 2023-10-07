from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from mysql_db import MySQL
import math
import bleach
import os
import hashlib
import mimetypes
from werkzeug.utils import secure_filename
import markdown

app = Flask(__name__)
application = app

PER_PAGE = 10
PERMITTED_PARAMS = ["title", "description", "year", "publisher", "author", "size"]
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
DIRECTORY_PATH = os.path.join(os.getcwd(), 'static', 'images')

app.config.from_pyfile('config.py')
db = MySQL(app)

from auth import bp as bp_auth, init_login_manager, check_rights

init_login_manager(app)
app.register_blueprint(bp_auth)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getParams(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None 
    return result

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = """ SELECT 
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

class Book:
    def __init__(self):
        self.title = None
        self.description = None
        self.year = None
        self.publisher = None
        self.author = None
        self.size = None

class Review():
    def __init__(self,grade, text, book_id, users_id, created_At):
        self.grade = grade
        self.text = text
        self.book_id= book_id
        self.users_id = users_id
        self.created_At = created_At
def getBook(book_id):
    query = """
            SELECT * FROM book WHERE id = %s
    """
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()
    return book

def set_params(book_obj, params):
    for param in params:
        if params[param]!=None:
            setattr(book_obj, param, params[param])

def getGenres(book_id):
    edited_genres = {}
    if book_id!=-1:
        query = """
                    SELECT genres.id, genres.name FROM book
                    JOIN book_has_genres ON book.id = book_has_genres.book_id
                    JOIN genres ON book_has_genres.genres_id = genres.id
                    WHERE book.id = %s
        """
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(query, (book_id,))
            genres = cursor.fetchall()
        edited_genres = [ str(genre.id) for genre in genres]
    query = """
                SELECT * FROM genres
    """
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        allgenres = cursor.fetchall()
    return allgenres, edited_genres

@app.route('/books/<int:book_id>/edit', methods=['GET'])
@login_required
@check_rights("edit")    
def edit(book_id):
    book = getBook(book_id=book_id)
    allgenres, edited_genres = getGenres(book_id=book_id)
    return render_template("books/edit.html", genres = allgenres, book=book, new_genres=edited_genres)

@app.route('/add', methods=['GET'])
@login_required
@check_rights("create")    
def add():
    allGenres,_ = getGenres(-1)
    return render_template("books/new.html", genres = allGenres,  book={})

@app.route('/create_book', methods=['POST'])
@login_required
@check_rights("create")    
def create_book():
    allGenres,_ = getGenres(-1)
    new_genres = request.form.getlist('genre_id')
    cur_params = getParams(PERMITTED_PARAMS)
    book = Book()
    set_params(book,cur_params)
    file = request.files["cover_img"]
    for param in cur_params:
        if cur_params[param]==None or (file.filename=="") or len(new_genres)==0:
            flash("Указаны не все параметры", "danger")
            return render_template("books/new.html", genres = allGenres, book=book, new_genres=new_genres)
        cur_params[param] = bleach.clean(cur_params[param])
    md5_hex = hashlib.md5(file.read()).hexdigest()
    file.seek(0)
    try:
        query = """
                SELECT * FROM covers WHERE MD5_hash = %s
        """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(md5_hex,)) 
                    cover = cursor.fetchone()            
        if cover==None:
             if allowed_file(file.filename):
                  filename = secure_filename(file.filename)
                  mime_type, _ = mimetypes.guess_type(file.filename)
                  query = """
                    INSERT INTO covers (file_name, MIME_type, MD5_hash) VALUES (%s, %s, %s);
                    """
                  with db.connection.cursor(named_tuple = True) as cursor:
                        cursor.execute(query,(filename,mime_type,md5_hex)) 
                        db.connection.commit()  
                        coverLastId = cursor.lastrowid
             else:
                  flash('Недопустимое расширение файла', 'danger')  
                  return render_template("books/new.html", genres = allGenres, book=book,  new_genres=new_genres)
        else:
             coverLastId = cover.id               
        query = """
                INSERT INTO book (title, description, author, year, size, publisher, covers_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(query,(cur_params['title'],cur_params['description'],cur_params['author'],cur_params['year'],cur_params['size'],cur_params['publisher'], coverLastId)) 
            db.connection.commit() 
            book_id = cursor.lastrowid     
            for genre in new_genres:
                query = """
                        INSERT INTO book_has_genres (book_id, genres_id) VALUES (%s, %s);
                        """
                with db.connection.cursor(named_tuple = True) as cursor:
                        cursor.execute(query,(book_id,genre)) 
                        db.connection.commit()     
        if cover==None:
             file.save(os.path.join(DIRECTORY_PATH, filename))           
            
    except:
        db.connection.rollback()
        flash('Ошибка при добавлении', 'danger')  
        return render_template("books/new.html", genres = allGenres, book=book,  new_genres=new_genres)  
    return redirect(url_for('show', book_id=book_id))


@app.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def delete(book_id):
   
    book = getBook(book_id=book_id)
    try:
        query = """
               SELECT COUNT(*) AS count_books_with_same_covers_id
               FROM book
               WHERE covers_id = (SELECT covers_id FROM book WHERE id = %s);
        """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,)) 
                    cover_num = cursor.fetchone().count_books_with_same_covers_id
        if cover_num==1:         
            query = """
                    SELECT covers.file_name FROM book JOIN covers ON book.covers_id = covers.id WHERE book.id = %s
            """
            with db.connection.cursor(named_tuple = True) as cursor:
                        cursor.execute(query,(book_id,)) 
                        cover_name = cursor.fetchone().file_name
                        file_path = os.path.join(DIRECTORY_PATH, cover_name)
            query = """
                   DELETE FROM covers
                   WHERE id = (SELECT covers_id FROM book WHERE id = %s);
            """
            with db.connection.cursor(named_tuple = True) as cursor:
                        cursor.execute(query,(book_id,)) 
                        db.connection.commit()        
        query ="""
                DELETE FROM book
                WHERE id = %s;
        """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,)) 
                    db.connection.commit()
        if cover_num==1:
             os.remove(file_path) 
        flash(f'Книга {book.title} успешно удалена', 'success')
    except:
        db.connection.rollback()
        flash('Ошибка при удалении', 'danger')    
    return redirect(url_for('index'))   
   

@app.route('/books/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights("edit")
def update_book(book_id):
    book = getBook(book_id=book_id)
    allgenres, edited_genres = getGenres(book_id=book_id)
    cur_params = getParams(PERMITTED_PARAMS)
    new_genres = request.form.getlist('genre_id')
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
                    cursor.execute(query,(cur_params['title'],cur_params['description'],cur_params['author'],cur_params['year'],cur_params['size'],cur_params['publisher'],book_id)) 
                    db.connection.commit()
        query = """
                DELETE FROM book_has_genres WHERE book_id = %s;
                """
        with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,)) 
                    db.connection.commit()
        for genre in new_genres:
            query = """
                INSERT INTO book_has_genres (book_id, genres_id) VALUES (%s, %s);
                """
            with db.connection.cursor(named_tuple = True) as cursor:
                    cursor.execute(query,(book_id,genre)) 
                    db.connection.commit()    
        flash(f"Книга '{cur_params['title']}' успешно обновлена", "success")
    except:
        db.connection.rollback() 
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
            "text": request.form.get('description'),
            "users_id": current_user.id,
            "book_id": book_id
        }
        if params["text"]==None:
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
        if your_review!=None:
            your_review = Review(grade = your_review.grade, text = markdown.markdown(your_review.text), created_At = your_review.created_At, book_id = your_review.book_id, users_id = your_review.users_id)
        for review in all_reviews:
             index = all_reviews.index(review)
             if review!=None:
                all_reviews[index]= Review(grade = review.grade, text = markdown.markdown(review.text), created_At = review.created_At, book_id = review.book_id, users_id = review.users_id)
                
        return your_review,all_reviews

@app.route('/books/<int:book_id>')
def show(book_id):
        query = """ 
                    SELECT 
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
            if db_book!=None:
                new_book = Book()
                new_book.author = db_book.author
                new_book.description = markdown.markdown(db_book.description)
                new_book.publisher = db_book.publisher
                new_book.size = db_book.size
                new_book.title = db_book.title
                new_book.year = db_book.year
                new_book.file_name = db_book.file_name
                new_book.id = db_book.id
                db_book = new_book
        your_review, all_reviews = getReviews(book_id=book_id)   
        return render_template('books/show.html', book=db_book, your_review=your_review, all_reviews=all_reviews)
