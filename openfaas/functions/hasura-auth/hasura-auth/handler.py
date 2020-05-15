API_ID_MAP = {
    "muaQ6NXyzYvXn33n4MJXKJRadVzLdW": {"id": 2, "role": "user"},
    "DY8PQSaY7KC6AXKuN9RWJ3GvpmPY5H": {"id": 3, "role": "user"}
}

def handle(event, context):
    print(event)

    api_key = event.headers.get("X-Api-Key")

    if api_key and api_key in API_ID_MAP:
        res = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": {
                "X-Hasura-User-Id": str(API_ID_MAP[api_key]["id"]),
                "X-Hasura-Role": API_ID_MAP[api_key]["role"],
                "X-Hasura-Is-Owner": "true",
            }
        }
    else:
        res = {
            "statusCode": 401,
        }

    return res