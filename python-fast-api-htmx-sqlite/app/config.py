from dotenv import load_dotenv
import os
from typing import List


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value


class Secrets:

    def __init__(self):
        # Load the environment variables
        load_dotenv()

# TODO: getopt() for cmd line arguments
class Config:
    host_name: str
    listen_address: str
    listen_port: int
    database_path: str
    debug: bool
    log_path: str | None

    secrets: Secrets

    def __init__(self):
        # Load the environment variables
        load_dotenv()

        self.host_name = os.getenv("HOST_NAME", "http://localhost:9000")

        self.listen_address = os.getenv("listen_address", "0.0.0.0")

        self.listen_port = int(os.getenv("listen_port", 9000))

        self.database_path = os.getenv("DATABASE_PATH", ":memory:")

        # Set the log path
        self.log_path = empty_to_none("LOG_PATH")

        # Determine if the DEBUG mode is set
        debug = os.getenv("DEBUG", "True")
        self.debug = debug == "True"

        self.secrets = Secrets()
