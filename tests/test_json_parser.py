import unittest
import json
import re

def parse_action_block(text: str):
    pattern = re.compile(r"^.*?`{3}(?:json)?\n?(.*?)`{3}.*?$", re.DOTALL)
    found = pattern.search(text)
    if not found:
        raise ValueError("Action not found")
    action = found.group(1)
    try:
        return json.loads(action.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON action block: {e}")

class TestParseJsonAction(unittest.TestCase):

    def test_valid_action(self):
        text = """
        Thought: I will query the orders table and group by status.
        Action: 
        ```json
        {
            "action": "execute_sql",
            "action_input": "SELECT status, COUNT(id) AS count FROM orders GROUP BY status;"
        }
        ```
        PAUSE
        """
        expected = {
            "action": "execute_sql",
            "action_input": "SELECT status, COUNT(id) AS count FROM orders GROUP BY status;"
        }
        result = parse_action_block(text)
        self.assertEqual(result, expected)

    def test_no_action_block(self):
        text = "Thought: just thinking...\nNo action block here."
        with self.assertRaises(ValueError) as context:
            parse_action_block(text)
        self.assertIn("Action not found", str(context.exception))

    def test_invalid_json(self):
        text = """
        Action:
        ```json
        { invalid json here }
        ```
        """
        with self.assertRaises(ValueError) as context:
            parse_action_block(text)
        self.assertIn("Failed to decode JSON", str(context.exception))

if __name__ == "__main__":
    unittest.main()