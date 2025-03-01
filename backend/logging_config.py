import atexit
import datetime
import json
import logging
import logging.config
import logging.handlers
import pathlib
from typing import cast
from typing import override

CONFIG_FILE = pathlib.Path(__file__).parent / "logging_config.json"
logger = logging.getLogger("app")

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
    "fmt_keys",
    "_style",
    "_fmt",
    "datefmt",
}


class JSONFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_message(record)
        return json.dumps(message, default=str)

    def _prepare_message(self, record: logging.LogRecord) -> dict[str, str]:
        always_fields = {
            "message": record.getMessage(),
            "timestamp": datetime.datetime.fromtimestamp(record.created, tz=datetime.UTC).isoformat(),
        }
        if record.exc_info:
            always_fields["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_value if (msg_value := always_fields.pop(val, None)) is not None else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        # Ensure always fields are included
        message |= always_fields
        # Include extra fields
        message |= {k: v for k, v in record.__dict__.items() if k not in LOG_RECORD_BUILTIN_ATTRS}
        return message


def setup_logging() -> None:
    with CONFIG_FILE.open("r") as file:
        config = json.load(file)

    for handler in config["handlers"].values():
        if filepath := handler.get("filename"):
            pathlib.Path(filepath).parent.mkdir(exist_ok=True)

    logging.config.dictConfig(config=config)

    queue_handler = cast(logging.handlers.QueueHandler | None, logging.getHandlerByName("queue_handler"))
    if queue_handler is not None and queue_handler.listener is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


if __name__ == "__main__":
    setup_logging()
    logger.debug("Hello, World!")
    logger.info("Hello, World!")
    logger.warning("Hello, World!", extra={"foo": "extra_value"})
    logger.error("Hello, World!")
    logger.critical("Hello, World!")

    try:
        _ = 1 / 0
    except Exception:
        logger.exception("An error occurred")
