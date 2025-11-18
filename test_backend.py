import requests
import json

# Test the backend
def test_backend():
    # Test UI texts endpoint
    print("Testing UI texts endpoint...")
    try:
        response = requests.get('http://localhost:5000/ui-texts/en')
        print(f"UI Texts Status: {response.status_code}")
        print(f"UI Texts Response: {response.json()}")
    except Exception as e:
        print(f"UI Texts Error: {e}")
    
    print("\nTesting chat endpoint...")
    try:
        response = requests.post('http://localhost:5000/send', 
                               json={'message': 'hello', 'language': 'en'})
        print(f"Chat Status: {response.status_code}")
        print(f"Chat Response: {response.json()}")
    except Exception as e:
        print(f"Chat Error: {e}")

if __name__ == '__main__':
    test_backend()