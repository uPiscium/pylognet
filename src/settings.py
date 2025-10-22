from pydantic import BaseModel


class APISettings:
    PING_PATH = "ping"
    LOG_PATH = "log"


class LogLevel:
    VERBOSE = "VERBOSE"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"


class LogEntry(BaseModel):
    id: str
    timestamp: str
    level: str
    message: str
