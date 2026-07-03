from flask import Flask, request
import datetime as dt

app = Flask(__name__)

articles  = {
        1:{'content':"<div> <h1> my first article </h1> <p> file one </p> </div>", 'title':"my first article", id:1},
        2:{'content':"<div> <h1> my second article </h1> <p> file two </p> </div>", 'title':"my second article", id:2}
        }
articles_count = len(articles) + 1


def get_articles():
    titles_section = " "
    for article_id, article in articles.items():
        title = article.get('title')
        titles_section += f"<a href=/article/{article_id}>{title}</a><br/><br/>"
    return titles_section

@app.route("/home")
def index():
    titles_section = get_articles()
    return ( """ <h1>Personal Blog</h1> """ + titles_section )


@app.route("/article/<int:article_number>")
def get_article(article_number):
    return articles.get(int(article_number)).get('content')


def create_article(title, date, content):
    return dict(content=content, title=title, id=articles_count, date=date)


@app.route("/new")
def new_article():
    title = request.args.get("title", "")
    date = request.args.get("date", "")
    content = request.args.get("content", "")

    try:
        new_article = create_article(title, date, content)
        articles[articles_count] = new_article

        return """
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
    except Exception:
        return "An error occured"

def edit_article(article_id, title, date, content):
    article = articles.get(int(article_id))

    if article:
        article['content'] = content
        article['title'] = title 
        if article.get('date'):
            article['date'] = date

        return True
    else:
        return False

@app.route("/edit/<article_id>", methods=['POST', 'GET'])
def update_article(article_id):
    title = request.args.get("title", "")
    date = request.args.get("date", "")
    content = request.args.get("content", "")

    try:
        if edit_article(article_id,title, date, content):
            message = "<p> Article's been edited successfully </p>"
        else:
            message = "<p> An error occured </p>"


        return ( 
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
    except Exception:
        return "An error occured"






if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
