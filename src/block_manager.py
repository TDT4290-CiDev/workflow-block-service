from blocks.example import Example
from blocks.send_mail import SendMail

blocks = {
    'example': Example(),
    'send_mail': SendMail()
}

type_map = {
    'string': str,
    'str': str,
    'float': float,
    'double': float,
    'integer': int,
    'int': int,
    'boolean': bool,
    'bool': bool
}