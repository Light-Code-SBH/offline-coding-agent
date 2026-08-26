# Sample Python code with errors — for testing error detection
# File: test_data/python/sample_with_errors.py

def calculate_average(numbers):
    total = 0
    for num in numbers
        total += num
    average = total / len(numbers)
    return average

result = calculate_average([])
print("Average:", reuslt)

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b)
        result = a + b
        self.history.append(result)
        return result
    
    def divide(self, a, b):
        return a / b  # No zero division check
