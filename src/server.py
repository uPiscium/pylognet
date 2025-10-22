from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
import uvicorn

from .logger import Logger
from .settings import APISettings, LogEntry


class LoggingService:
    def __init__(self, api_settings: APISettings = APISettings()):
        """
        Initializes the LoggingService with the given API settings.

        Args:
            api_settings (APISettings): Configuration settings for the API.
        """
        self.__logger = Logger()
        self.__api_settings = api_settings
        self.__app = FastAPI()
        self.__router = APIRouter()
        self.__setup_routes()

    def __setup_routes(self):
        self.__router.add_api_route(
            f"/{self.__api_settings.PING_PATH}",
            self.ping,
            methods=["GET"],
            response_class=JSONResponse,
        )
        self.__router.add_api_route(
            f"/{self.__api_settings.LOG_PATH}",
            self.log,
            methods=["POST"],
            response_class=JSONResponse,
        )
        self.__router.add_api_route(
            "/retrieve",
            self.retrieve_logs,
            methods=["GET"],
            response_class=JSONResponse,
        )
        self.__router.add_api_route(
            "/get-all",
            self.get_all,
            methods=["GET"],
            response_class=JSONResponse,
        )
        self.__router.add_api_route(
            "/get-log-queue",
            self.get_log_queue,
            methods=["GET"],
            response_class=JSONResponse,
        )

    def get_app(self) -> FastAPI:
        """
        Returns the FastAPI application instance.

        Returns:
            FastAPI: The FastAPI application.
        """
        self.__app.include_router(self.__router)
        return self.__app

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Runs the FastAPI application using Uvicorn.

        Args:
            host (str): The host address to bind the server to.
            port (int): The port number to bind the server to.
        """
        uvicorn.run(self.get_app(), host=host, port=port)

    async def ping(self) -> JSONResponse:
        """
        Health check endpoint to verify the service is running.

        Returns:
            JSONResponse: A JSON response indicating the service status.
        """
        return JSONResponse(content={"status": "ok"}, status_code=200)

    async def log(self, entry: LogEntry) -> JSONResponse:
        """
        Logs a message with the specified log level.

        Args:
            entry (LogEntry): The log entry containing the message and log level.

        Returns:
            JSONResponse: A JSON response indicating the logging status.
        """
        log = self.__logger.record(entry)
        return JSONResponse(content={"log": log}, status_code=201)

    async def retrieve_logs(self, id: str) -> JSONResponse:
        """
        Retrieves all log entries for a given ID.

        Args:
            id (str): The identifier for which to retrieve log entries.

        Returns:
            JSONResponse: A JSON response containing the log entries.
        """
        logs = self.__logger.retrieve(id)
        return JSONResponse(
            content={"logs": [str(log) for log in logs]}, status_code=200
        )

    async def get_all(self) -> JSONResponse:
        """
        Retrieves all log entries for all IDs.

        Returns:
            JSONResponse: A JSON response containing all log entries.
        """
        all_logs = self.__logger.get_all()
        formatted_logs = {
            id: [str(log) for log in logs] for id, logs in all_logs.items()
        }
        return JSONResponse(content={"all_logs": formatted_logs}, status_code=200)

    async def get_log_queue(self) -> JSONResponse:
        """
        Retrieves the log queue.

        Returns:
            JSONResponse: A JSON response containing the log queue.
        """
        log_queue = self.__logger.get_log_queue()
        return JSONResponse(content={"log_queue": log_queue}, status_code=200)
