from blocks.block import WorkflowBlock
import smtplib

from email.message import EmailMessage

class SendMail(WorkflowBlock):

    def get_info(self):
        return {
            'description': 'A block used for sending an email',
            'params': {
                'from': {
                    'type': 'string',
                    'description': 'Address the email is sent from.'
                },
                'to': {
                    'type': 'string',
                    'description': 'Address to send email to.'
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
                    'description': 'True if sent, False isf something went wrong.'
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
            with smtplib.SMTP('172.17.0.1', 12000) as smtp:
                smtp.send_message(msg)
            return {'email_sent': True}
        #TODO::Fix error handling to better know what went wrong
        except:
            return {'email_sent': False}

    def resume(self, state, params):
        pass