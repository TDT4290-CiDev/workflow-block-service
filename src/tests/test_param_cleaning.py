import unittest

from block_manager import blocks
from main import clean_params, get_requested_params


class CleanParamTests(unittest.TestCase):

    def setUp(self):
        self.example = blocks['example']
        self.send_mail = blocks['send_mail']
        self.approval = blocks['approval']

    def test_example_execute_correct_params(self):
        body = {'params': {'param1': 'test', 'param2': 1}}
        cleaned_params = clean_params(self.example, body, False)
        self.assertEqual(cleaned_params, body['params'])

    def test_example_resume_correct_params(self):
        body = {'params': {'param1': 'suspend', 'param2': 1}}
        body['state'] = self.example.execute(body['params'])[0]
        cleaned_params = clean_params(self.example, body, True)
        self.assertEqual(cleaned_params, {'param1': body['params']['param1']})

    def test_example_execute_incorrect_params(self):
        body = {'params': {'wrong_name':1}}
        with self.assertRaises(ValueError):
            clean_params(self.example, body, False)

    def test_example_resume_incorrect_params(self):
        body = {'params': {'param1': 'suspend', 'param2': 1}}
        body['state'] = self.example.execute(body['params'])[0]
        body['params'] = {'wrong_name': 1}
        with self.assertRaises(ValueError):
            clean_params(self.example, body, True)


class RequestedParamTests(unittest.TestCase):

    def setUp(self):
        self.example = blocks['example']
        self.send_mail = blocks['send_mail']
        self.approval = blocks['approval']

    def test_example_execute(self):
        body = {'params': {'param1': 'test', 'param2': 1}}
        req_params = get_requested_params(self.example, body, False)
        self.assertEqual(req_params, self.example.get_info()['params'])

    def test_example_resuming(self):
        body = {'params': {'param1': 'suspend', 'param2': 1}}
        body['state'] = self.example.execute(body['params'])[0]
        req_params = get_requested_params(self.example, body, True)
        self.assertEqual(req_params, {'param1': self.example.get_info()['params']['param1']})


