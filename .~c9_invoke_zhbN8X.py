"""
    app.py
    This file launches the flask server for the app
"""
import os
from datetime import datetime
import flask
import flask_socketio
import sqlalchemy
from dotenv import load_dotenv
from pytz import timezone
import tables
from tables import BASE

load_dotenv()

APP = flask.Flask(__name__)
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

# ENGINE = sqlalchemy.create_engine(database_url)
ENGINE = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
BASE.metadata.create_all(ENGINE, checkfirst=True)

SESSION_MAKER = sqlalchemy.orm.sessionmaker(bind=ENGINE)
SESSION = SESSION_MAKER()

LOGGEDIN_CLIENTS = []

EST = timezone("EST")


@APP.route("/")
def hello():
    """When someone opens the app, send them the page"""
    return flask.render_template("index.html")


@SOCKETIO.on("log in")
def on_user_login():
    """Recieve OAuth information when sent by the client"""
    if flask.request.sid not in LOGGEDIN_CLIENTS:
        LOGGEDIN_CLIENTS.append(flask.request.sid)


@SOCKETIO.on("disconnect")
def on_user_disconnect():
    """Recieve OAuth information when sent by the client"""
    if flask.request.sid in LOGGEDIN_CLIENTS:
        LOGGEDIN_CLIENTS.remove(flask.request.sid)


@SOCKETIO.on("get comments")
def on_get_comments(data):
    """Process a new comment"""
    try:
        which_tab = data["tab"]
        all_comments_tab = [
            {
                "text": comment.text,
                "name": comment.name,
                "time": comment.time.astimezone(EST).strftime("%m/%d/%Y, %H:%M:%S"),
            }
            for comment in SESSION.query(tables.Comment)
            .filter(tables.Comment.tab == which_tab)
            .all()
        ]
        all_comments_tab.reverse()
        flask_socketio.emit("old comments", {"comments": all_comments_tab})
    except KeyError:
        return


@SOCKETIO.on("new comment")
def on_new_comment(data):
    """Process a new comment"""
    if flask.request.sid not in LOGGEDIN_CLIENTS:
        return
    try:
        new_text = data["text"]
        which_tab = data["tab"]
        who_sent = data["name"]
        time = datetime.now()
        SESSION.add(tables.Comment(new_text, who_sent, which_tab, time))
        SESSION.commit()
        time_str = time.astimezone(EST).strftime("%m/%d/%Y, %H:%M:%S")
        SOCKETIO.emit(
            "new comment",
            {"text": new_text, "name": who_sent, "tab": which_tab, "time": time_str},
        )
    except KeyError:
        return


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )































































































