#!/usr/bin/python3

import unittest
import pandas as pd
import os


class TestUpdateMain(unittest.TestCase):
    """
    A unittest TestCase class for testing the update_main function.
    """

    def setUp(self):
        """
        Set up the test environment. This method is run before each test.
        It creates a sample main_data.csv file and a sample output.csv file.
        """
        df_main = pd.DataFrame({'class_name': ['class1', 'class2'], 'counts': [5, 10]})
        df_main.to_csv('data_base/main_dectection_data.csv', index=False)

        df_new = pd.DataFrame({'class_name': ['class2', 'class3', 'class3']})
        df_new.to_csv('output.csv', index=False)

    def test_update_main(self):
        """
        The actual test method. It calls the update_main function and checks
        if the 'counts' column in the updated main_data.csv file is as expected.
        """
        update_main("output.csv", "data_base/main_dectection_data.csv")

        df_main_updated = pd.read_csv('data_base/main_dectection_data.csv')

        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class1', 'counts'].values[0], 5)
        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class2', 'counts'].values[0], 6)
        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class3', 'counts'].values[0], 2)

    def tearDown(self):
        """
        Clean up the test environment. This method is run after each test.
        It deletes the CSV files created for the test.
        """
        os.remove('data_base/main_dectection_data.csv')
        os.remove('output.csv')

if __name__ == '__main__':
    unittest.main()
