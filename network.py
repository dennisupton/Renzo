import file
import threading
from flask import Flask
app = Flask(__name__)

@app.route("/")
async def index():
    return file.currentFile

threading.Thread(target=app.run, kwargs={"port": 8080}, daemon=True).start()
