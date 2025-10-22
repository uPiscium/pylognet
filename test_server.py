from src import server

if __name__ == "__main__":
    # Start the logging server
    server = server.LoggingService()
    server.run()
