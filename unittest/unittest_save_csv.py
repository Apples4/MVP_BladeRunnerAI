#!/usr/bin/python3

import unittest
import os
import pandas as pd


class TestSaveInfo(unittest.TestCase):
    """
    A unittest TestCase class for testing the save_info function.
    """

    def test_save_info(self):
        """
        The actual test method. It calls the save_info function and then checks
        if the output file was created and has the expected columns.
        """
        save_info("sample_video.mp4")

        self.assertTrue(os.path.exists("output.csv"))

        df = pd.read_csv("output.csv")

        self.assertIn("time", df.columns)
        self.assertIn("class_name", df.columns)
        self.assertIn("confidence", df.columns)

        os.remove("output.csv")

if __name__ == '__main__':
    unittest.main()
