from blocks.block import WorkflowBlock
import smtplib

from email.message import EmailMessage

server_name = 'smtp.stud.ntnu.no'
server_port = '587'

with open('mail_user.txt') as usr:
    username = usr.read()

with open('mail_pass.txt') as pw:
    password = pw.read()

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
        msg['Subject'] = params['subject']
        msg['From'] = params['from']
        msg['To'] = params['to']
        msg.set_content(params['message'])

        # Switch to appropriate mail server address.
        try:
            with smtplib.SMTP(server_name, server_port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(username, password)
                smtp.send_message(msg)
            return {'email_sent': True}
        # TODO::Fix error handling to better know what went wrong
        except smtplib.SMTPConnectError as connect_e:
            print('Unable to connect to SMTP server.\n' + connect_e.message())
            return {'email_sent': False}
        except smtplib.SMTPAuthenticationError as auth_e:
            print('Username and password not accepted.\n' + auth_e.message())
            return {'email_sent': False}
        except smtplib.SMPTException as e:
            print('An error occured: ' + e.message())
