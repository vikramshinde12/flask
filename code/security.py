from resources.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    print(f'I am calling in authentication of {username}')
    print(user)
    if user and user.password == password:
        return user


def identity(payload):
    print(f'payload for identity : {payload}')
    user_id = payload['identity']
    print(f'I am calling for identify {user_id}')
    return UserModel.find_by_id(user_id)
