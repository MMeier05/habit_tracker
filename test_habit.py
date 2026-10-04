import unittest
import habit
import datetime as dt

class TestHabit(unittest.TestCase):
    def test_is_due1(self):
        habit1 = habit.Habit("name", 2)
        habit1.last_completed -= dt.timedelta(3)
        self.assertEqual(habit1.is_due(), True)

    def test_is_due2(self):
        habit1 = habit.Habit("name", 2)
        habit1.last_completed -= dt.timedelta(1)
        self.assertEqual(habit1.is_due(), False)

    def test_is_due3(self):
        habit1 = habit.Habit("name", 2)
        habit1.last_completed -= dt.timedelta(2)
        self.assertEqual(habit1.is_due(), True)

    def test_is_due3(self):
        habit1 = habit.Habit("name", 1)
        habit1.last_completed -= dt.timedelta(1)
        self.assertEqual(habit1.is_due(), True)

if __name__ == "__main__":
    unittest.main()
