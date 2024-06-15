import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())

def create_user(username:str) -> dict:
    return {
        "user_id": generate_uuid(),
        "username": username
    }