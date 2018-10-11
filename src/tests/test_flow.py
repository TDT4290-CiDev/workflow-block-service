import unittest

import flow, trigger, block, action

class FlowtestCase(unittest.TestCase):

    def setUp(self):
        self.trigger = trigger.Trigger()
        self.block = block.Block('Dummy')

    def test_action_is_performed_when_event_is_triggered(self):
        self.flow = flow.Flow('test name', 'test description', self.trigger, [self.block])
        self.trigger.trigger()
        self.assertEqual(self.flow.status, flow.FlowStatus.COMPLETED)
        self.assertTrue(self.block.activated)


    def test_flow_updates_all_values(self):
        square_action = action.UpdateAction(lambda x: x**2)
        self.foreach_square = block.ForEachBlock('Square the input number', square_action)
        input_dict = {'en':1, 'to':2, 'tre':3}
        self.flow = flow.Flow('test_update_each_value', 'Description', self.trigger, [self.foreach_square], **input_dict)
        self.trigger.trigger()
        self.assertEqual(input_dict['en']**2, self.flow.output['en'])
        self.assertEqual(input_dict['to']**2, self.flow.output['to'])
        self.assertEqual(input_dict['tre']**2, self.flow.output['tre'])
