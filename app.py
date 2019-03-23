from flask import Flask, render_template
from TopTen import output, movies, you_tube_top_ten_url, top_ten_movies, youtube_urls

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    output(movies)
    output(you_tube_top_ten_url)
    return render_template("about.html", out1=top_ten_movies,out2=youtube_urls)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
