import io
import os
import sys
import unittest

# import ps_updater from the ../ps_updater folder
curr_dir = os.path.realpath(os.path.dirname(__file__))
ps_updater_path = os.path.join(curr_dir, "..", "ps_updater")
sys.path.insert(1, os.path.realpath(ps_updater_path))
import ps_updater


class TestPsUPdater(unittest.TestCase):
    """
    Tests ps_updater.py
    """

    def test_production(self):
        """
        Makes sure that we are in production mode.
        """
        self.assertFalse(ps_updater.boold, "boold should be False in production mode")
    
    def test_show_error_msg(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            raise Exception("My test exception")
        except Exception as e:
            ps_updater.show_error_msg(e)
            output = new_stdout.getvalue()
            self.assertIn("My test exception", output)
            self.assertIn("Exception", output)
            new_stdout.truncate(0)
        
        try:
            raise TypeError("This is a another type of exception")
        except Exception as e:
            ps_updater.show_error_msg(e)
            output = new_stdout.getvalue()
            self.assertIn("This is a another type of exception", output)
            self.assertIn("TypeError", output)
            new_stdout.truncate(0)
        
        sys.stdout = old_stdout
    
    def test_seconds_between(self):
        import datetime

        for n in range(100):
            start_date = datetime.datetime.now().astimezone().isoformat()
            end_date = datetime.datetime.now() + datetime.timedelta(seconds=n)
            end_date = end_date.astimezone().isoformat()

            start = str(start_date)
            end = str(end_date)
            difference = ps_updater.seconds_between(start, end)

            self.assertAlmostEqual(difference, n, 2)


if __name__ == "__main__":
    unittest.main()