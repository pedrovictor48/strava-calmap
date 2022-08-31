from asyncio import events
import mimetypes
from flask import Flask, request, send_file
import requests
from functions import request_activities
import calplot

import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    args = request.args
    code = args.get("code")
    oauth_res = requests.post("https://www.strava.com/oauth/token",
        params={
            "client_id": "92961",
            "client_secret": "505bc92b4ca50b1413cf97188d2b29c9f9a5e20e",
            "code": code,
            "grant_type": "authorization_code" 
        }
    ).json()
    print(oauth_res)
    access_token = oauth_res['access_token']

    activities = request_activities(access_token, 1)
    print(activities)
    fig, _ = calplot.calplot(activities, cmap='YlGn', colorbar=False)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"