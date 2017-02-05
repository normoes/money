import unittest
import utils.input_client as input_client
# from utils.inputClient import NoValidDateException, NotEmptyException, NumberOfMinusException, TooManyDigtsAfterDotException, NumberOfDotsException

class Input(unittest.TestCase):
    # preparing to test
    def setUp(self):
        pass
    # ending the test
    def tearDown(self):
        pass

    def test_dates(self):
        try:
            self.assertEqual(input_client.check_date('2016')), 'no date'
        except ValueError as e:
            print e
        with self.assertRaises(ValueError) as contexts:
            input_client.check_date('2016')
        self.assertRaises(ValueError, lambda: input_client.check_date('2016'))
        # self.assertRaises(ValueError, input_client.check_date('2016'))


    def test_moneyValue(self):
        assert(type(input_client.check_value('123')) == float), 'not float'
        self.assertEqual(input_client.check_value('123'), 123.0), 'not float'
        assert(type(input_client.check_value('123.0')) == float), 'not float'
        assert(input_client.check_value('123.0') == 123.0), 'not float'
        assert(type(input_client.check_value('123.')) == float), 'not float'
        assert(input_client.check_value('123.') == 123.0), 'not float'
        assert(type(input_client.check_value('-123.')) == float), 'not float'
        assert(input_client.check_value('-123.') == -123.0), 'not float'
        assert(type(input_client.check_value('-12.4')) == float), 'not float'
        assert(input_client.check_value('-12.4') == -12.4), 'not float'
        assert(type(input_client.check_value('-12,3')) == float), 'comma'
        assert(input_client.check_value('-12,3') == -12.3), 'comma'
        assert(type(input_client.check_value('-.3')) == float), 'not float'
        assert(input_client.check_value('-.3') == -.3), 'not float'

        try:
            input_client.check_value('')
        except ValueError as e:
            print e
        try:
            input_client.check_value('--123.')
        except ValueError as e:
            print e
        try:
            input_client.check_value('-.312')
        except ValueError as e:
            print e
        try:
            input_client.check_value('123..')
        except ValueError as e:
            print e
        try:
            input_client.check_value('.123.')
        except ValueError as e:
            print e
        try:
            input_client.check_value(',123,')
        except ValueError as e:
            print e

if __name__ == '__main__':
    unittest.main()
