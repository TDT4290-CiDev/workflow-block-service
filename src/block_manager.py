from blocks.example import Example
from blocks.send_mail import SendMail
from blocks.approval import Approval

blocks = {
    'example': Example(),
    'send_mail': SendMail(),
    'approval': Approval()
}

type_map = {
    'string': str,
    'str': str,
    'float': float,
    'double': float,
    'integer': int,
    'int': int,
    'boolean': bool,
    'bool': bool,
}
