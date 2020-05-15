import requests

BACKEND_URL = "http://hasura-service.backend:8080/v1/graphql"
API_KEY = "muaQ6NXyzYvXn33n4MJXKJRadVzLdW"
UID = 2
INSERT_QUERY = """mutation {
  insert_events(objects: {data: "%(data)s", uid: %(uid)s}) {
    returning {
      data
      ts
    }
  }
}
"""

def handle(req):
    headers = {
        "X-Api-Key": API_KEY
    }
    print(INSERT_QUERY % {"uid": UID, "data": req})
    res = requests.post(
        url=BACKEND_URL,
        json={
            "query": INSERT_QUERY % {
                "uid": UID,
                "data": req
            }},
        headers=headers)
    print(res.content.decode("utf-8"))