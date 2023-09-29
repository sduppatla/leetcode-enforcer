import json
import requests
import time

class LeetcodeSubmissionRetriever:
    def __init__(self):
        # leetcode graphql url
        self.url = "https://leetcode.com/graphql"
        self.max_submission_gap_secs = 86400 # 60 secs * 60 mins * 24 hrs 

        self.body = """
        {{     
            recentSubmissionList(username: "{0}") 
            {{
                title
                titleSlug
                timestamp
                statusDisplay
                lang
                __typename
            }}
        }} 
        """

    def should_enforce(self, user):
        body = self.body.format(user)
        response = requests.post(url=self.url, json={"query": body})
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve leetcode submissions for user: {user}")

        submissions = json.loads(response.content)
        submissions = submissions["data"]["recentSubmissionList"]

        # Assume that submissions are shorted with decreasing timestamps
        latest_submission = submissions[0]
        latest_submission_ts = float(latest_submission["timestamp"])
        current_ts = float(time.time())
        time_since_last_submission_secs = int(current_ts - latest_submission_ts)
        if time_since_last_submission_secs > self.max_submission_gap_secs:
            print(f"User must be removed, latest submission was over {time_since_last_submission_secs // 86400} days ago")
            return True
        return False

lsr = LeetcodeSubmissionRetriever()