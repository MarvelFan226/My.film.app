from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()Конечно, давай по шагам и максимально просто, без сложных терминов. Представь, что мы собираем небольшой конструктор прямо через телефон.

Вот пошаговый план, как запустить свой собственный онлайн-сервер для регистрации и общих отзывов **абсолютно бесплатно**:

---

### Шаг 1. Создаем аккаунт на GitHub
GitHub — это бесплатный сайт, где будут храниться файлы твоего сервера.
1. Зайди в браузере на телефон на сайт [github.com](https://github.com/).
2. Если нет аккаунта, зарегистрируйся (нужна просто почта и пароль). Если уже есть — войди в него.

---

### Шаг 2. Создаем «хранилище» для проекта (Репозиторий)
1. Нажми на плюсик (`+`) в верхнем правом углу экрана телефона и выбери **New repository** (Новый репозиторий).
2. В поле **Repository name** напиши любое английское название, например: `my-movie-server`.
3. Обязательно выбери точку рядом со словом **Public** (чтобы сервер был доступен в интернете).
4. Прокрути страницу вниз и нажми зеленую кнопку **Create repository**.

---

### Шаг 3. Создаем файлы сервера прямо на сайте
Теперь нужно добавить в этот проект код нашего сервера. Мы сделаем это прямо через браузер телефона.

1. На странице твоего созданного проекта нажми на ссылку **creating a new file** (создать новый файл).
2. В поле сверху введи название первого файла: `app.py`
3. Скопируй этот код и вставь его в большое поле для текста:

```python
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


# Функция для подключения к базе данных
def init_db():
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  # Таблица пользователей
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,"
      " username TEXT UNIQUE, password TEXT)"
  )
  # Таблица отзывов
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, movie TEXT, author TEXT, text TEXT)"
  )
  conn.commit()
  conn.close()


init_db()


@app.route("/")
def home():
  return "Сервер работает!"


# Регистрация
@app.route("/register", methods=["POST"])
def register():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Успешно!"})
  except:
    return jsonify(
        {"status": "error", "message": "Такое имя уже занято!"}
    ), 400


# Вход
@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT * FROM users WHERE username = ? AND password = ?",
      (username, password),
  )
  user = cursor.fetchone()
  conn.close()
  if user:
    return jsonify({"status": "success", "message": "Вход выполнен!"})
  return jsonify({"status": "error", "message": "Неверный логин или пароль!"}), 400


# Получить отзывы для фильма
@app.route("/reviews/<movie_title>", methods=["GET"])
def get_reviews(movie_title):
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT author, text FROM reviews WHERE movie = ? ORDER BY id DESC",
      (movie_title,),
  )
  rows = cursor.fetchall()
  conn.close()
  reviews_list = [{"author": r[0], "text": r[1]} for r in rows]
  return jsonify(reviews_list)


# Добавить отзыв
@app.route("/reviews", methods=["POST"])
def add_review():
  data = request.json
  movie = data.get("movie")
  author = data.get("author")
  text = data.get("text")
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO reviews (movie, author, text) VALUES (?, ?, ?)",
      (movie, author, text),
  )
  conn.commit()
  conn.close()
  return jsonify({"status": "success"})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)