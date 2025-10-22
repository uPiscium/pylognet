from src import client

import threading
import time
import random

if __name__ == "__main__":
    server = "http://localhost:8000"

    cli1 = client.Client("dummy1", server)
    cli2 = client.Client("dummy1", server)

    def log_messages(client_instance, messages):
        for msg in messages:
            response = client_instance.log(msg, level="INFO")
            print(f"Logged: {response}")
            time.sleep(random.uniform(1, 3))

    messages1 = [f"Message {i} from client 1" for i in range(5)]
    messages2 = [f"Message {i} from client 2" for i in range(5)]

    thread1 = threading.Thread(target=log_messages, args=(cli1, messages1))
    thread2 = threading.Thread(target=log_messages, args=(cli2, messages2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
