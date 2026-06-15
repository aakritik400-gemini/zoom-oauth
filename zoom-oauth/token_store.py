USER_TOKENS = {}

def save_token(user_id: str, token_data: dict):
    USER_TOKENS[user_id] = token_data


def get_token(user_id: str):
    return USER_TOKENS.get(user_id)
