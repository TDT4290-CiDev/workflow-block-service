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
        response = self.app.post('/example', json=example_input)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)
        self.assertIn(b'world', response.data)

    def test_missing_param(self):
        data = {'params': {'param1': 'test missing param2'}}
        response = self.app.post('/example', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing parameter param2', response.data)

    def test_wrong_param_type(self):
        data = copy.deepcopy(example_input)
        data['params']['param1'] = 5
        response = self.app.post('/example', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid type for parameter param1', response.data)

        data = copy.deepcopy(example_input)
        data['params']['param2'] = 'string, not integer'
        response = self.app.post('/example', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid type for parameter param2', response.data)

    def test_example_suspension(self):
        response = self.app.post('/example', json=example_suspend)
        resp_data = response.get_json()
        susp_count = resp_data['state']['suspend_count']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(susp_count, 1)
        self.assertIn(b'state', response.data)
        self.assertIn(b'requested_params', response.data)
        self.assertIn(b'"type":"suspend"', response.data)

    def test_example_resuming(self):
        suspend_response = self.app.post('/example', json=example_suspend)
        self.assertEqual(suspend_response.status_code, 200)
        data = suspend_response.get_json()
        data['params'] = {'param1': 'test_resume'}
        resume_response = self.app.post('/example/resume', json=data)
        self.assertEqual(resume_response.status_code, 200)
        print(resume_response.data)




