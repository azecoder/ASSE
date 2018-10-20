import poll as p
import unittest
 
class TestDoodle(unittest.TestCase):
 
    def test_vote(self, title, options):
        tested_poll = p.Poll(5, 'attempt', ['A', 'C', 'B'])

        result = tested_poll.vote('voleyball', ['C', 'A']);
        self.assertEqual(result.pollnumber, 3)
    
if __name__ == '__main__':
    unittest.main()