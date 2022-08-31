import requests
import pandas as pd
import datetime

def request_activities(access_token, page_limit):
    activities = []
    for page in range(1, page_limit + 1):
        req_ans = requests.get("https://www.strava.com/api/v3/athlete/activities", 
            params={
                "access_token": access_token,
                "per_page": "200"
            }
        ).json()
        if len(req_ans) == 0:
            break
        activities.extend(req_ans)
    
    df = pd.Series(
        [x["distance"] for x in activities], 
        index=[datetime.datetime.fromisoformat(x["start_date_local"][0:-1]) for x in activities]
    )
    return df