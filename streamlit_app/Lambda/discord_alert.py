import http.client
import json

def lambda_handler(event, context):
    url = "/api/webhooks/"
    conn = http.client.HTTPSConnection("discord.com")

    user_id = "12345"
    mention_string = f"<@{user_id}>"
    sns_message = event["Records"][0]["Sns"]["Message"]

    payload = {
        "content": "EC2 (Server) is down - check the AWS console! " + sns_message + " " + mention_string,
        "embeds": [],
        "username": "AWS Notifications",
        "attachments": []
    }

    headers = {"Content-Type": "application/json"}

    conn.request("POST", url, body=json.dumps(payload), headers=headers)

    res = conn.getresponse()

    conn.close()
