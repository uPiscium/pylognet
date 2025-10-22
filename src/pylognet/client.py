from typing import Optional
import requests
import datetime

from .settings import LogLevel, APISettings, LogEntry

RequestResponse = bool | requests.Response


class Client:
    def __init__(
        self, logger_id: str, endpoint: str, api_settings: APISettings = APISettings()
    ):
        """
        Initializes the Logger with the given service ID and endpoint.

        Args:
            logger_id (str): The unique identifier for the logging service.
            endpoint (str): The base URL of the logging service.

        Raises:
            ConnectionError: If the logging service is not reachable.
        """
        self.__id = logger_id
        self.__endpoint = endpoint
        self.__api_settings = api_settings

        if self.__endpoint.endswith("/"):
            self.__endpoint = self.__endpoint[:-1]  # Remove trailing slash

        if self.ping() is not True:
            raise ConnectionError(
                f"Unable to reach logging service at {self.__endpoint}"
            )

    def __create_url(self, path: str) -> str:
        """
        Creates a full URL by combining the base endpoint with the given path.

        Args:
            path (str): The API path to append to the endpoint.

        Returns:
            str: The full URL.
        """
        return f"{self.__endpoint}/{path}"

    def __check_response(self, response: requests.Response) -> RequestResponse:
        """
        Checks the response status code.

        Args:
            response (requests.Response): The response object to check.

        Returns:
            bool | requests.Response: True if status code is 200-299, else the response object.
        """
        if 200 <= response.status_code < 300:
            return True
        return response

    def ping(self, api: Optional[str] = None) -> RequestResponse:
        """
        Pings the logging service to check if it's reachable.
        Returns True if the service responds with status code 200-299,
        otherwise returns the full response object.

        Args:
            api (Optional[str]): The API endpoint for pinging. Defaults to APISettings.PING_PATH.

        Returns:
            bool | requests.Response: True if status code is 200-299, else the response object.
        """
        if api is None:
            api = self.__api_settings.PING_PATH

        url = self.__create_url(api)
        response = requests.get(url)
        return self.__check_response(response)

    def log(
        self, message: str, level: str = LogLevel.INFO, api: Optional[str] = None
    ) -> RequestResponse:
        """
        Sends a log message to the logging service with the specified log level.

        Args:
            message (str): The log message to send.
            level (str): The log level (e.g., "INFO", "ERROR"). Defaults to "INFO".
            api (Optional[str]): The API endpoint for logging. Defaults to APISettings.LOG_PATH.

        Returns:
            bool | requests.Response: The response from the logging request.
        """
        if api is None:
            api = self.__api_settings.LOG_PATH

        now = datetime.datetime.now()
        timestamp = now.isoformat()
        payload = LogEntry(
            id=self.__id,
            timestamp=timestamp,
            level=level,
            message=message,
        ).model_dump()
        url = self.__create_url(api)
        response = requests.post(url, json=payload)
        return self.__check_response(response)
