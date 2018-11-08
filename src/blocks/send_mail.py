import os
import smtplib

from blocks.block import WorkflowBlock
from block_exception import BlockError
from email.message import EmailMessage

server_name = 'smtp.stud.ntnu.no'
server_port = '587'

username = os.environ.get('BLOCK_MAIL_USER', '')
password = os.environ.get('BLOCK_MAIL_PASS', '')

class SendMail(WorkflowBlock):

    def get_info(self):
        return {
            'description': 'Send an email.',
            'params': {
                'from': {
                    'type': 'string',
                    'description': 'Address the email is sent from.'
                },
                'to': {
                    'type': 'list',
                    'description': 'Addresses to send email to.'
                },
                'subject': {
                    'type': 'string',
                    'description': 'Mail subject'
                },
                'message': {
                    'type': 'string',
                    'description': 'Mail message'
                }
            },
            'outputs': {
                'email_sent': {
                    'type': 'boolean',
                    'description': 'True if sent, False if something went wrong.'
                }
            },
            'can_suspend_execution': False
        }

    def execute(self, params):
        msg = EmailMessage()
        try:
            msg['Subject'] = params['subject']
            msg['From'] = params['from']
            msg['To'] = params['to']
            msg.set_content(params['message'])
        except KeyError as e:
            raise BlockError(str(e))
        try:
            with smtplib.SMTP(server_name, server_port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(username, password)
                smtp.send_message(msg)
            return {'email_sent': True}
        except smtplib.SMTPConnectError:
            raise BlockError("Unable to connect to the SMTP server {}".format(server_name))
        except smtplib.SMTPAuthenticationError:
            raise BlockError('Username and password not accepted to {}'.format(server_name))
        except smtplib.SMTPException:
            raise BlockError('An error occured while connecting to the SMTP server {}'.format(server_name))
