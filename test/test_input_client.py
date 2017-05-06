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
        import datetime
        current_year = datetime.datetime.today().strftime('%Y')
        # print repr(current_year+'0101')
        compare_date = datetime.date(int(current_year),int('01'),int('01'))
        # print repr(input_client.check_date('01').strftime('%Y%m%d'))
        self.assertEqual(input_client.check_date('01'), compare_date), 'only month given, day=01 and current year'
        self.assertEqual(input_client.check_date('1'), compare_date), 'only month given, day=01 and current year'
        with self.assertRaises(ValueError) as context:
            input_client.check_date('13')
        with self.assertRaises(ValueError) as context:
            input_client.check_date('0')
        # try:
        #     self.assertEqual(input_client.check_date('2016')), 'no date'
        # except ValueError as e:
        #     print e
        with self.assertRaises(ValueError) as context:
            input_client.check_date('2016')
        # self.assertRaises(ValueError, lambda: input_client.check_date('2016'))


    def test_money_value(self):
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

        # try:
        #     input_client.check_value('')
        # except ValueError as e:
        #     print e
        with self.assertRaises(ValueError) as context:
            input_client.check_value('')
        with self.assertRaises(ValueError) as context:
            input_client.check_value('--123.')
        with self.assertRaises(ValueError) as context:
            input_client.check_value('123..')
        with self.assertRaises(ValueError) as context:
            input_client.check_value('.123.')
        with self.assertRaises(ValueError) as context:
            input_client.check_value(',123,')

if __name__ == '__main__':
    unittest.main()
