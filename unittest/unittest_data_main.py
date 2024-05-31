#!/usr/bin/python3

import unittest
import pandas as pd
import os

class TestUpdateMainCSV(unittest.TestCase):
    def setUp(self):
        "Create a sample main_data.csv file"
        df_main = pd.DataFrame({'class_name': ['class1', 'class2'], 'counts': [5, 10]})
        df_main.to_csv('main_data.csv', index=False)

        "Create a sample new_data.csv file"
        df_new = pd.DataFrame({'class_name': ['class2', 'class3', 'class3']})
        df_new.to_csv('new_data.csv', index=False)

    def test_update_main_csv(self):
        update_main_csv('new_data.csv')

        "Read the updated main_data.csv file"
        df_main_updated = pd.read_csv('main_data.csv')

        "Check the counts of each class"
        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class1', 'counts'].values[0], 5)
        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class2', 'counts'].values[0], 11)
        self.assertEqual(df_main_updated.loc[df_main_updated['class_name'] == 'class3', 'counts'].values[0], 2)

    def tearDown(self):
        "Delete the CSV files after the test"
        os.remove('main_data.csv')
        os.remove('new_data.csv')

if __name__ == '__main__':
    unittest.main()
