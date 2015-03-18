from anarcho import app, db
from anarcho.models.track import Track
from flask import request, jsonify


@app.route('/api/track/list', methods=['GET'])
def tracks_list():
    result = Track.query.all()
    return jsonify(data=[i.to_dict() for i in result])


@app.route('/api/track', methods=['POST'])
def track_post():
    track_log = request.values.get("log", "").encode("utf-8")
    track_time = request.values.get("time", "")

    track = Track(track_log, track_time)
    db.session.add(track)
    db.session.commit()

    return track.to_json()
