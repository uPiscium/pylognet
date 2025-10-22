import requests

if __name__ == "__main__":
    server = "http://0.0.0.0:8000"

    # Test logging messages
    print(requests.get(f"{server}/get-all").json())
    print(requests.get(f"{server}/get-log-queue").json())
