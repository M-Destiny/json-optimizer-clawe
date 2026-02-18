import json
import random
import string

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Create a list with duplicates
data = []
for _ in range(500):
    item = {"id": random.randint(1, 100), "name": random_string()}
    data.append(item)

# Add some explicit duplicates
data.append(data[0])
data.append(data[10])
data.append({"id": 999, "tags": ["a", "b", "a"]}) # Nested duplicate

with open('test_input.json', 'w') as f:
    json.dump(data, f)

print("Created test_input.json")
