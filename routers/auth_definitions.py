from apis.schemas.token_model import Token
from apis.schemas.user_input_model import User
from apis.auth_apis import sign_up, sign_in, get_current_user


class SingUpDefinition:
    URI = '/sign-up'
    API = sign_up
    METHODS = ["POST"]
    RESPONSE_MODEL = Token


class SingInDefinition:
    URI = '/sign-in'
    API = sign_in
    METHODS = ["POST"]
    RESPONSE_MODEL = Token

class GetUserDefinition:
    URI = '/user'
    NAME = 'get_user'
    API = get_current_user
    METHODS = ["GET"]
    RESPONSE_MODEL = User