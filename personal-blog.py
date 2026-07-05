from flask import Flask, request, render_template, redirect, url_for
from markupsafe import escape
import json
import datetime as dt
import os

### TODO apply escape

app = Flask(__name__)

def write_json(articles):
    with open("json_articles.json", mode="w", encoding="utf-8") as file:
        json.dump(articles, file)
def read_json():
    try:
        with open("json_articles.json", mode="r", encoding="utf-8") as file:
            articles = json.load(file)
        return articles
    except FileNotFoundError:
        return {} 

@app.route("/home")
def index():
    articles = read_json()
    return render_template("home.html", posts=articles)

@app.route("/article/<article_number>")
def get_content(article_number):
    articles = read_json()
    if articles:
        if articles.get(article_number):
            return escape(articles.get(article_number).get('content'))
        return "<p> No content yet </p>"
    return "<h1> No Articles yet </h1>"


@app.route("/admin")
def admin():
    articles = read_json()
    return render_template("admin_dashboard.html", posts=articles)

def create_article(article_id, title, date, content):
    articles = read_json()
    return dict(id=article_id, content=content, title=title , date=date)

@app.route("/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        articles = read_json()

        title = request.form.get("title")
        date = request.form.get("date")
        content = request.form.get("content")
        
        if not articles.get('count'):
            articles['count'] = 1
        new_article = create_article(articles['count'], title, date, content)
        articles[new_article.get('id')] = new_article
        articles['count'] += 1
        write_json(articles)
        return redirect(url_for("admin"))
    return render_template("new_article.html")

def edit_article(article_id, title, date, content):
    articles = read_json()
    
    if articles:
        article = articles.get(article_id)

        if article:
            article['content'] = content
            article['title'] = title 
            if article.get('date'):
                article['date'] = date
            write_json(articles)

            return True

@app.route("/edit/<article_id>", methods=['GET', 'POST'])
def update_article(article_id):
    articles = read_json()
    article = articles.get(article_id)

    if request.method == "POST":
        if articles:
            title = request.form.get("title")
            date = request.form.get("date")
            content = request.form.get("content")
            

            title = title if title else article['title']
            date = date if date else article['date']
            content = content if content else article['content']

            edit_article(article_id,title, date, content) 
            return redirect(url_for("admin"))

    return render_template("edit.html", post=article)


    

@app.route('/delete/<article_id>', methods=['POST'])
def delete_article(article_id):
    articles = read_json()

    if articles:
        article = articles.get(article_id)
        if article:
            del articles[article_id]
            articles['count'] -= 1
            write_json(articles)
            return ("""<p> Article Deleted Successfully </p>""" + 
                     """ <form action="/admin" method="get">
                            <input type="submit" value="admin">
                         </form>
                     """ 
 
                    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
