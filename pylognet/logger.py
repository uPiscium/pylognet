import datetime
import os
import queue
import time

from .settings import LogEntry


class Log:
    def __init__(self, message: str, level: str = "INFO", timestamp: str = ""):
        self.__message = message
        self.__level = level
        self.__timestamp = (
            timestamp
            if timestamp
            else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

    def __str__(self):
        return f"[{self.__timestamp}] [{self.__level}] {self.__message}"


class Logger:
    def __init__(self, queue_size: int = 1000):
        self.__log_queue = queue.Queue(maxsize=queue_size)
        self.__logs: dict[str, list[Log]] = {}

    def record(self, entry: LogEntry) -> str:
        """
        Records a log entry.

        Args:
            entry (LogEntry): The log entry containing the message and log level.

        Returns:
            str: The recorded log entry in string format.
        """
        self.__log_queue.put(entry)

        log = Log(entry.message, entry.level)
        if entry.id not in self.__logs:
            self.__logs[entry.id] = []

        self.__logs[entry.id].append(log)
        return str(log)

    def retrieve(self, id: str) -> list[Log]:
        """
        Retrieves all log entries for a given ID.

        Args:
            id (str): The identifier for which to retrieve log entries.

        Returns:
            list[Log]: A list of log entries associated with the given ID.
        """
        return self.__logs.get(id, [])

    def get_services(self) -> list[str]:
        """
        Retrieves all unique IDs that have log entries.

        Returns:
            list[str]: A list of unique IDs.
        """
        return list(self.__logs.keys())

    def get_all(self) -> dict[str, list[Log]]:
        """
        Retrieves all log entries for all IDs.

        Returns:
            dict[str, list[Log]]: A dictionary mapping IDs to their respective log entries.
        """
        return self.__logs

    def get_log_queue(self) -> list[str]:
        """
        Return all log entries from the log queue without removing them.

        Returns:
            list[str]: A list of log entries in string format.
        """
        logs = []
        return logs

    def clear_logs(self) -> None:
        """
        Clears all stored log entries.
        """
        self.__logs.clear()

    def clear_service_logs(self, id: str) -> None:
        """
        Clears all log entries for a specific service ID.

        Args:
            id (str): The identifier for which to clear log entries.
        """
        if id in self.__logs:
            del self.__logs[id]

    def clear_log_queue(self) -> None:
        """
        Clears all entries from the log queue.
        """
        self.__log_queue.queue.clear()

    def export(self, folder_path: str):
        """
        Saves all log entries to files in the specified folder.

        Args:
            folder_path (str): The path to the folder where log files will be saved.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for id, logs in self.__logs.items():
            file_path = os.path.join(folder_path, f"{id}_{now}.log")
            with open(file_path, "w") as f:
                for log in logs:
                    f.write(str(log) + "\n")
