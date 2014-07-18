import time

from app import app
from flask import request


@app.route('/track', methods=['POST', 'GET'])
def track():
    if request.method == 'POST':
        track_text = request.values.get("text", "").encode("utf-8")
        track_time = time.strftime("%d/%m/%Y %H:%M:%S")
        log_line = track_time + " : " + track_text + "<br>"

        track_log = open("tracks", "a")
        track_log.write(log_line)
        track_log.close()
        return '{"track_time":"' + track_time + '","track_text":"' + track_text + '"}'
    track_log = open("tracks", "r")
    log = track_log.read()
    track_log.close()
    return log

