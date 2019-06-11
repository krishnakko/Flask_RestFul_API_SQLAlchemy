from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):  # safe_str_cmp will helps to compare strings safely
        return user


# payload is the content of the jwt token
def identity(payload):
    user_id = payload['identity']  # extracting user_id from payload
    return UserModel.find_by_id(user_id)


