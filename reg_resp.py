import re

class RegexResponder:
    def __init__(self):
        self.patterns = []

    def add_pattern(self, regex, response):
        """Add a regex pattern and its associated response."""
        self.patterns.append({'regex': regex, 'response': response})

    def find_response(self, text):
        """Find a response based on the first matching regex pattern."""
        for pattern in self.patterns:
            if re.search(pattern['regex'], text):
                return pattern['response']
        return None

# Example usage
responder = RegexResponder()
responder.add_pattern(r'hello', 
                      {'msg': 'Hello there!', 
                       'url': 'https://example.com/hello'})
responder.add_pattern(r'bye', 
                      {'msg': 'Goodbye!', 
                       'url': 'https://example.com/bye'})

# Testing the find_response method
print(responder.find_response('hello, how are you?'))  # {'txt': 'Hello there!', 'url': 'https://example.com/hello'}
print(responder.find_response('it\'s time to say bye'))  # {'txt': 'Goodbye!', 'url': 'https://example.com/bye'}
print(responder.find_response('no match here'))  # None
