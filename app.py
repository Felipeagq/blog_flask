# flask_sqlalchemy = https://flask-sqlalchemy.palletsprojects.com/en/2.x/
import os
#os.system("pip3 install Flask-SQLAlchemy")
from flask import Flask
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template, request , redirect
from werkzeug.utils import redirect


app = Flask(__name__)  # creación de instancia de Flask


#path = r"/media/felo/Felipe/archivos/Cursos y Videos/Python/FLASK/"
path= r'D:\archivos\Cursos y Videos\Python\FLASK'
database = "blog.db"
path_db = os.path.join(path, database)
 # crear y definir la base de datos, la dirección
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path_db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app) # Nuestra DB la queremos ligar a nuestra aplicación


# Esta clase podria ir en un archivo diferente para tener más orden
class Post(db.Model): # modelo de de base de datos (tabla)
    # las columnas que queramos que tenga nuestra tabla
    __tablaname__= "posts"
    id = db.Column(db.Integer, primary_key=True) # creamos el ID
    titulo = db.Column(db.String, nullable=False) # el tittulo, no puede ir vacia
    fecha = db.Column(db.DateTime, default=datetime.now()) # la fecha, tiene un valor por defecto que es el datetime
    texto = db.Column(db.String, nullable=False) # texto o contenido del post, no puede ir vacio


def verificar_db(path_database):
    ''' Esta función verifica si la base de datos existe,
    si la base de datos existe, la crea.

    La base de datos debe ser suministrada de
    manera manual en el codigo '''
    if not os.path.exists(path_database):
        print("Base de datos no existe")
        db.create_all()
        print("Base de datos creada")
    else:
        print("La base de datos existe")


@app.route("/") #ruta principal
def index():
    posts = Post.query.order_by(Post.fecha.desc()).all() # select * from order by
    return render_template("index.html", posts = posts)


@app.route("/agregar")
def agregar():
    return render_template("agregar.html")


@app.route("/crear_post", methods=["POST"])
def crear_post():
	titulo = request.form.get("titulo")
	texto = request.form.get("texto")
	post = Post(titulo=titulo, texto=texto)
	db.session.add(post)
	db.session.commit()
	return redirect("/")


@app.route("/borrar_post", methods=['POST'])
def borrar_post():
    post_id = request.form.get("post_id")
    post = db.session.query(Post).filter(Post.id==post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/")    

if __name__ == '__main__':
    # verificar_db(path_db)
    
    # Ejecutar el servidor
    app.run(debug=True)