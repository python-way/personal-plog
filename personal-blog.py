from flask import Flask, request
import json
import datetime as dt

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
    titles_section = get_articles_for_home()
    return (

             """ <h1>Personal Blog</h1> """ + titles_section 
            )

@app.route("/article/<article_number>")
def get_article(article_number):
    articles = read_json()
    if articles:
        if articles.get(article_number):
            return articles.get(article_number).get('content')
        return "<p> No content yet </p>"
    return "<h1> No Articles yet </h1>"


def get_articles_for_home():
    articles = read_json()
    if articles:
        titles_section = " "

        for article_id, article in articles.items():
            if article_id == "count":
                continue
            title = article.get('title')
            titles_section += f"<a href=/article/{article_id}>{title}</a><br/><br/>"
        return titles_section
    return "<h1> No Articles yet </h1>"


@app.route("/admin")
def admin():
    titles_section = get_articles_for_admin()
    return ( """ <form action="/new"  method="get">
                    <input type="submit" value="Create Article">
                 </form>
             """ + titles_section

            )


def create_article(article_id, title, date, content):
    articles = read_json()
    return dict(id=article_id, content=content, title=title , date=date)


@app.route("/new")
def new_article():
    articles = read_json()

    title = request.args.get("title", "")
    date = request.args.get("date", "")
    content = request.args.get("content", "")
    
    if title and date and content:
        if not articles.get('count'):
            articles['count'] = 1
        new_article = create_article(articles['count'], title, date, content)
        articles[new_article.get('id')] = new_article
        articles['count'] += 1
        write_json(articles)




    return  (
         """ <form action="/admin" method="get">
                <input type="submit" value="admin">
             </form>
         """ 
            +
            """
            <form action="" method="get">
                <input type="text" name="title" placeholder="Article Title">
                <br/>
                <br/>
                <input type="text" name="date" placeholder="Publishing date">
                <br/>
                <br/>
                <label>Article Content</label>
                <br/>
                <textarea name="content"> </textarea>
                <br/>
                <br/>
                <input type="submit" value="Publish"></input>
            </form>
            """
            )

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

@app.route("/edit/<article_id>", methods=['GET'])
def update_article(article_id):
    articles = read_json()

    if articles:
        article = articles.get(article_id)
        if article:
            title = request.args.get("title", "")
            date = request.args.get("date", "")
            content = request.args.get("content", "")
            

            title = title if title else article['title']
            date = date if date else article['date']
            content = content if content else article['content']

            edit_article(article_id,title, date, content)


    return (
         """ <form action="/admin" method="get">
                <input type="submit" value="admin">
             </form>
         """ +
            """
            <form action="" method="get">
                <input type="text" name="title" placeholder="Article Title">
                <br/>
                <br/>
                <input type="text" name="date" placeholder="Publishing date">
                <br/>
                <br/>
                <label>Article Content</label>
                <br/>
                <textarea name="content"> </textarea>
                <br/>
                <br/>
                <input type="submit" value="Update"></input>
            </form>
            """
    )
    

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


def get_articles_for_admin():
    articles = read_json()
    titles_section = " "

    if articles: 
        for article_id, article in articles.items():
            if article_id == 'count':
                continue
            titles_section += f"""
                                 <div>
                                    <span>{article['title']}</span>
                                    <a href=/edit/{article['id']}>Edit</a>
                                    <form action="/delete/{article_id}" method="POST">
                                        <button type="submit">Delete</button>
                                    </form>
                                 </div>
                                 """
        return titles_section
    return "<h1> No Articles yet </h1>"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
