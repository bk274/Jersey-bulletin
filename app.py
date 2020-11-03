"""
    app.py
    This file launches the flask server for the app
"""
import os
import flask
import flask_socketio
import sqlalchemy
from dotenv import load_dotenv
import tables
from tables import BASE

load_dotenv()

APP = flask.Flask(__name__)
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

ENGINE = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
BASE.metadata.create_all(ENGINE, checkfirst=True)

SESSION_MAKER = sqlalchemy.orm.sessionmaker(bind=ENGINE)
SESSION = SESSION_MAKER()


@APP.route("/")
def hello():
    """When someone opens the app, send them the page"""
    return flask.render_template("index.html")


@SOCKETIO.on("new comment")
def on_new_comment(data):
    """Process a new comment"""
    try:
        new_text = data["text"]
        which_tab = data["tab"]
        SESSION.add(tables.Comment(new_text, which_tab))
        SESSION.commit()
        all_comments_tab = [
            {"text": comment.text}
            for comment in SESSION.query(tables.Comment)
            .filter(tables.Comment.tab == which_tab)
            .all()
        ]
        all_comments_tab.reverse()
        SOCKETIO.emit("new comment", {"comments": all_comments_tab})
    except KeyError:
        return


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
