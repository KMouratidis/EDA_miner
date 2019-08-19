"""
TBW...
"""

from flask import Flask, jsonify, request
from flask_caching import Cache
import googleanalytics as ga
import redis
import json


app = Flask(__name__)

# Use the network Redis server for storage
r = redis.Redis()
# As well as for the cache backend
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


def ganalytics_connect(client_email, private_key):
    """
    Connect to a Google Analytics account. Doesn't seem to be \
    memoizable. Google throws `googleapiclient.errors.HttpError: 401`.
    """

    # Redis/Python/I is/am stupid and backslashes are not interpreted as
    # escape characters (which supposedly is bad) so we must fix it.
    accounts = ga.authenticate(client_email=client_email,
                               private_key=private_key.replace("\\n", "\n"))

    # Queries are handled per profile, and we only need one (for now)
    profile = accounts[0].webproperties[0].profile

    return profile


@app.route("/<string:user_id>/<string:metrics>", methods=["GET"])
@cache.memoize(timeout=5*60)
def get(user_id, metrics):

    # Check if user has given us their credentials
    profile_info = r.get(f"{user_id}_profile_info")
    if profile_info is None:
        return jsonify({
            "success": "false",
            "message": "Profile credentials not found. Please connect "
                       "via a POST request first."
        }), 401  # Unauthorized

    else:
        # Remember: Redis returns bytes so we need to decode them
        profile_info = json.loads(profile_info)
        profile = ganalytics_connect(profile_info["client_email"],
                                     profile_info["private_key"])

        if metrics is None:
            return jsonify({
                "success": "false",
                "message": "No metrics provided."
            }), 400  # Bad Request

        # This also converts it into a list if there is only 1 metric
        metrics = metrics.split(",")

        # Get the results as a list of rows (named tuples)
        results = profile.core.query.metrics(*metrics).range("today").rows

        data = {}
        for metric in metrics:
            data[metric] = [getattr(result, metric)
                            for result in results]

        return jsonify({
            "success": "true",
            "data": data,
            "metrics": metrics,
        }), 200  # OK


# Verifies credentials and connects
@app.route("/", methods=["POST"])
def post():

    # Parse given data
    user_id = request.json["user_id"]
    private_key = request.json["private_key"]
    client_email = request.json["client_email"]

    # Store credentials as json in Redis
    profile_info = {"client_email": client_email,
                    "private_key": private_key}
    r.set(f"{user_id}_profile_info", json.dumps(profile_info))

    return jsonify({
        "success": "true"
    }), 201  # Created


if __name__ == "__main__":
    app.run(debug=True)
