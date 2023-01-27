from flask import Flask, render_template, redirect, url_for, request                                                    # Hier importieren wir verschiedene Flask-Module, die für die Erstellung der Web-Anwendung verwendet werden.
from flask_bootstrap import Bootstrap                                                                                   # Hier importieren wir das Bootstrap-Modul, das für die Gestaltung der Webseiten verwendet wird.
from flask_sqlalchemy import SQLAlchemy                                                                                 # Hier importieren wir das SQLAlchemy-Modul, das für die Verwaltung der Datenbank verwendet wird.
from flask_wtf import FlaskForm                                                                                         # Hier wird das FlaskForm-Modul importiert, das für die Erstellung von Formularen verwendet wird.
from wtforms import StringField, SubmitField                                                                            # Hier werden verschiedene Form-Felder importiert, die für die Erstellung von Formularen verwendet werden.
from wtforms.validators import DataRequired                                                                             # Hier wird der DataRequired-Validator importiert, der verwendet wird, um sicherzustellen, dass ein Form-Feld ausgefüllt ist.
import requests                                                                                                         # Hier wird die requests-Bibliothek importiert, welche für die für HTTP-Anfragen verwendet wird.

MOVIE_DB_API_KEY = "573d804effcd053399965b8a41a78675"                                                                   # Hier wird der API-Schlüssel für die Verwendung der Movie DB-API definiert.
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"                                                       # Hier wird die URL für die Suche nach Filmen in der Movie DB-API definiert.
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"                                                                # Hier wird die URL für die Abfrage von Film-Informationen in der Movie DB-API definiert.
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"                                                                  # Hier wird die URL für das Abrufen von Film-Bildern in der Movie DB-API definiert.

app = Flask(__name__)                                                                                                   # Hier erstellen wir eine neue Flask-Anwendung.
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'                                                           # Dann haben wir einen geheimen Schlüssel für die Anwendung festgelegt.
Bootstrap(app)                                                                                                          # Des weiteren haben wir die Bootstrap-Erweiterung für Flask importiert und der Anwendung zugewiesen.

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'                                                           # Dann haben wir die SQLAlchemy-Erweiterung konfiguriert, indem wir die Datenbank-URI festgelegt haben. In diesem Fall haben wir eine SQLite-Datenbank verwendet.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                                                    # Hier wird die automatische Überwachung von Änderungen durch SQLAlchemy deaktiviert.
db = SQLAlchemy(app)                                                                                                    # Hier wird die SQLAlchemy-Erweiterung der Anwendung zugewiesen.

##CREATE TABLE
class Movie(db.Model):                                                                                                  # Hier wird eine neue Klasse "Movie" erstellt, die von der db.Model-Klasse von SQLAlchemy erbt.
    id = db.Column(db.Integer, primary_key=True)                                                                        # Hier wird eine ID-Spalte als primären Schlüssel des Films erstellt, die eine Ganzzahl enthält.
    title = db.Column(db.String(250), unique=True, nullable=False)                                                      # Hier haben wir eine Spalte für den Titel des Films erstellt, die einen eindeutigen, nicht leeren Text enthält.
    year = db.Column(db.Integer, nullable=False)                                                                        # Hier wird eine Spalte für das Erscheinungsjahr des Films erstellt, die eine Ganzzahl enthält.
    description = db.Column(db.String(500), nullable=False)                                                             # Hier wird eine Spalte für die Beschreibung des Films erstellt, die einen nicht leeren Text enthält.
    rating = db.Column(db.Float, nullable=True)                                                                         # Hier wird eine Spalte für die Bewertung des Films erstellt, die eine Fließkommazahl enthält.
    ranking = db.Column(db.Integer, nullable=True)                                                                      # Hier wird eine Spalte für die Rangfolge des Films erstellt, die eine Ganzzahl enthält.
    review = db.Column(db.String(250), nullable=True)                                                                   # Hier wird eine Spalte für die Bewertung des Films erstellt, die einen String mit einer Länge von 250 Zeichen enthält.
    img_url = db.Column(db.String(250), nullable=False)                                                                 # Hier wird eine Spalte für die URL des Film-Posters erstellt, die einen String mit einer Länge von 250 Zeichen enthält.

with app.app_context():                                                                                                 # Hier wird der Kontext der Anwendung aktiviert.
    db.create_all()                                                                                                     # Hier werden alle Tabellen in der Datenbank erstellt.

class FindMovieForm(FlaskForm):                                                                                         # Hier wird eine Klasse für das Formular zum Suchen von Filmen erstellt.
    title = StringField("Movie Title", validators=[DataRequired()])                                                     # Hier wird ein String-Feld für den Titel des Films erstellt, das eine "DataRequired"-Validierung hat.
    submit = SubmitField("Add Movie")                                                                                   # Hier wird ein Submit-Feld erstellt, das die Beschriftung "Add Movie" hat.

class RateMovieForm(FlaskForm):                                                                                         # Hier wird eine Klasse für das Formular zum Bewerten von Filmen erstellt.
    rating = StringField("Your Rating Out of 10 e.g. 7.5")                                                              # Hier wird ein String-Feld für die Bewertung des Films erstellt.
    review = StringField("Your Review")                                                                                 # Und auch hier wird ein String-Feld für die Bewertung des Films erstellt.
    submit = SubmitField("Done")                                                                                        # Hier wird ein Submit-Feld erstellt, das die Beschriftung "Done" hat.

@app.route("/")                                                                                                         # Hier definieren wir einen Pfad für die Hauptseite unserer Anwendung.
def home():                                                                                                             # Hier definieren wir eine Funktion, die aufgerufen wird, wenn auf den Pfad "/" zugegriffen wird.
    all_movies = Movie.query.order_by(Movie.rating).all()                                                               # Hier werden alle Filme aus der Datenbank abgerufen und nach ihrer Bewertung sortiert.
    for i in range(len(all_movies)):                                                                                    # Hier wird eine Schleife gestartet, die durch alle Filme iteriert.
        all_movies[i].ranking = len(all_movies) - i                                                                     # Hier wird für jeden Film die Rangfolge berechnet, indem die Länge der Liste aller Filme abgezogen wird von der aktuellen Iteration.
    db.session.commit()                                                                                                 # Hier werden die Änderungen an der Datenbank bestätigt.
    return render_template("index.html", movies=all_movies)                                                             # Hier wird die HTML-Vorlage "index.html" aufgerufen und die Liste aller Filme als Argument übergeben, damit sie in der Vorlage verwendet werden kann.

@app.route("/add", methods=["GET", "POST"])                                                                             # Hier wird ein Pfad für die Seite zum Hinzufügen von Filmen definiert. Es erwartet sowohl GET- als auch POST-Anfragen.
def add_movie():                                                                                                        # Hier beginnt die Funktion add_movie().
    form = FindMovieForm()                                                                                              # Hiier wird eine Instanz der Klasse FindMovieForm erstellt, die zuvor definiert wurde.
    if form.validate_on_submit():                                                                                       # Hier wird überprüft, ob das Formular erfolgreich validiert wurde, bevor es gesendet wurde.
        movie_title = form.title.data                                                                                   # Hier wird der Wert des Titel-Eingabefelds des Formulars in eine Variable gespeichert.

        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})        # Hier wird eine GET-Anfrage an die API-URL gesendet, um Filme mit dem entsprechenden Titel zu suchen. Der API-Schlüssel und der Suchbegriff werden als Parameter übergeben.
        data = response.json()["results"]                                                                               # Die Antwort wird in ein JSON-Format umgewandelt und die Ergebnisse als "data" gespeichert.
        return render_template("select.html", options=data)                                                             # Das Template "select.html" wird gerendert und die gefundenen Filme in "options" übergeben.
    return render_template("add.html", form=form)                                                                       # Das Template "add.html" wird gerendert und das Formular in "form" übergeben.

@app.route("/find")                                                                                                     # Hier wird die Route für die Funktion find_movie() definiert.
def find_movie():                                                                                                       # Hier beginnt die Funktion find_movie().
    movie_api_id = request.args.get("id")                                                                               # Hier wird die ID des ausgewählten Films aus den Argumenten der Anfrage abgerufen
    if movie_api_id:                                                                                                    # Prüfung, ob der Wert der "id" vorhanden ist.
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"                                                           # Erstellung der URL für die Abfrage der Movie-Informationen anhand der "id".
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})               # Hier wird eine Anfrage an die angelegte URL gesendet und die Antwort als "response" gespeichert.
        data = response.json()                                                                                          # Die Antwort wird in ein JSON-Format umgewandelt und als "data" gespeichert.
        new_movie = Movie(                                                                                              # Eine neue Instanz der Klasse "Movie" wird erstellt und mit den Daten aus "data" befüllt.
            title=data["title"],                                                                                        #
            year=data["release_date"].split("-")[0],                                                                    #
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",                                                       #
            description=data["overview"]                                                                                #
        )
        db.session.add(new_movie)                                                                                       # Die neue Instanz von "Movie" wird der Datenbank hinzugefügt.


        db.session.commit()                                                                                             # Die Änderungen in der Datenbank werden gespeichert.
        return redirect(url_for("rate_movie", id=new_movie.id))                                                         # Der Nutzer wird auf die Route "rate_movie" weitergeleitet und die "id" des gerade hinzugefügten Films wird übergeben.

@app.route("/edit", methods=["GET", "POST"])                                                                            # Mit dieser Anweisung wird eine neue Route für die URL "/edit" erstellt und es werden sowohl GET- als auch POST-Anfragen erlaubt.
def rate_movie():                                                                                                       # Beginn der Funktion "rate_movie".
    form = RateMovieForm()                                                                                              # Eine Instanz der Klasse "RateMovieForm" wird erstellt.
    movie_id = request.args.get("id")                                                                                   # Hier wird der Wert der "id" aus den Argumenten des Requests abgerufen.
    movie = Movie.query.get(movie_id)                                                                                   # Ein Film mit der entsprechenden "id" wird aus der Datenbank abgefragt.
    if form.validate_on_submit():                                                                                       # Prüfung, ob das Formular erfolgreich abgesendet wurde und valide ist.
        movie.rating = float(form.rating.data)                                                                          # Der Bewertungswert des Films wird auf den Wert aus dem Formular gesetzt.
        movie.review = form.review.data                                                                                 # Der Review-Text des Films wird auf den Wert aus dem Formular gesetzt.
        db.session.commit()                                                                                             # Die Änderungen in der Datenbank werden gespeichert.
        return redirect(url_for('home'))                                                                                # Der Nutzer wird auf die Startseite weitergeleitet.
    return render_template("edit.html", movie=movie, form=form)                                                         # Das Template "edit.html" wird mit den Variablen "movie" und "form" gerendert.


@app.route("/delete")                                                                                                   # Mit dieser Anweisung wird eine neue Route für die URL "/delete" erstellt.
def delete_movie():                                                                                                     # Beginn der Funktion "delete_movie".
    movie_id = request.args.get("id")                                                                                   # Hier wird der Wert der "id" aus den Argumenten des Requests abgerufen.
    movie = Movie.query.get(movie_id)                                                                                   # Ein Film mit der entsprechenden "id" wird aus der Datenbank abgefragt.
    db.session.delete(movie)                                                                                            # Der Film wird aus der Datenbank gelöscht.
    db.session.commit()                                                                                                 # Die Änderungen in der Datenbank werden gespeichert.
    return redirect(url_for("home"))                                                                                    # Der Nutzer wird auf die Startseite weitergeleitet.


if __name__ == '__main__':                                                                                              # Prüfung, ob das Script als Hauptscript ausgeführt wird.
    app.run(debug=True)                                                                                                 # Der Server wird gestartet und im debug-Modus ausgeführt.
