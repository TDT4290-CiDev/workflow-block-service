import unittest
import copy

from src import block_manager
from src.main import app

example_input = {'params': {'param1': 'test', 'param2': 1}}
example_suspend = {'params': {'param1': 'suspend', 'param2': 1}}



class ExampleTests(unittest.TestCase):

    def setUp(self):
        self.blocks = block_manager.blocks
        self.app = app.test_client()

    def execute_example(self, param1=None, param2=None):
        input = {'params': {}}
        if param1 is not None:
            input['params']['param1'] = param1
        if param2 is not None:
            input['params']['param2'] = param2
        return self.app.post('/example', json = input)


    def test_discovery(self):
        response = self.app.get('/discovery')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'An example block used for documentation', response.data)

    def test_all_blocks_are_discovered(self):
        response = self.app.get('/discovery')
        data = response.get_json()
        self.assertEqual(len(data['blocks']), len(self.blocks))
        self.assertEqual(response.status_code, 200)

    def test_example_execution(self):
        response = self.execute_example('test', 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)
        self.assertIn(b'world', response.data)

    def test_missing_param(self):
        response = self.execute_example('test_missing_param2')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing parameter param2', response.data)

    def test_wrong_param_type(self):
        response = self.execute_example(1, 1)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid type for parameter param1', response.data)

        response = self.execute_example('test', 'string_not_integer')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid type for parameter param2', response.data)

    def test_example_suspension(self):
        response = self.execute_example('suspend', 1)
        resp_data = response.get_json()
        susp_count = resp_data['state']['suspend_count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(susp_count, 1)
        self.assertIn(b'state', response.data)
        self.assertIn(b'requested_params', response.data)
        self.assertIn(b'"type":"suspend"', response.data)

    def test_example_resuming(self):
        suspend_response = self.execute_example('suspend', 1)
        self.assertEqual(suspend_response.status_code, 200)
        data = suspend_response.get_json()
        data['params'] = {'param1': 'test_resume'}
        resume_response = self.app.post('/example/resume', json=data)
        self.assertEqual(resume_response.status_code, 200)
        print(resume_response.data)

    def test_execute_fails_when_suspended(self):
        suspend_response = self.execute_example('suspend', 1)
        execute_response = self.execute_example('test_restart', 1)
        self.assertEqual(execute_response.status_code, 400)

