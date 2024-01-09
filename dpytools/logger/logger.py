import logging
import os
import sys

import structlog

from utils import str_to_bool

logger = structlog.stdlib.get_logger()
HUMAN_FRIENDLY_LOGS = str_to_bool(os.environ.get("HUMAN_FRIENDLY_LOGS", "false"))

# #4 TODO Add some testing - see https://www.structlog.org/en/stable/testing.html for guidance


# #4 QUESTION What does this class actually do? If I comment it out, everything still works... (I think)
class DpLogger:
    def __init__(self, namespace: str):
        self.namespace = namespace

    def log(self, event, level, data=None):
        trace_id = generate_trace_id()
        span_id = generate_span_id()

        severity = {
            "debug": 3,  # INFO
            "warning": 2,  # WARNING
            "error": 1,  # ERROR
        }.get(
            level, 3
        )  # Default to INFO

        log_entry = {
            "namespace": self.namespace,
            "event": event,
            "trace_id": trace_id,
            "span_id": span_id,
            "severity": severity,
            "data": data if data is not None else {},
        }

        logger.log(level, **{"event_dict": log_entry})

    def debug(self, event, data=None):
        self.log(event, "debug", data)

    def warning(self, event, data=None):
        self.log(event, "warning", data)

    def error(self, event, data=None):
        self.log(event, "error", data)


def generate_trace_id():
    # TODO Implement this (https://opencensus.io/tracing/span/traceid/)
    return "your_trace_id"


def generate_span_id():
    # TODO Implement this (https://opencensus.io/tracing/span/spanid/)
    return "your_span_id"


# #4 TODO Output formatting (https://github.com/ONSdigital/dp-standards/blob/main/LOGGING_STANDARDS.md#output-formatting)
# #4 UTF-8 encoding is done (structlog.processors.UnicodeEncoder())
# #4 Still need to work out how to format JSON logs as JSON Lines (may need to create a callable to pass to structlog.processors.JSONRenderer())
# #4 TODO Add namespace to output - using an env var?
def configure_logger(enable_console_logs: bool = HUMAN_FRIENDLY_LOGS):
    shared_processors = [
        structlog.processors.TimeStamper(fmt="iso", key="created_at"),
        structlog.processors.UnicodeEncoder(),
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            }
        ),
        structlog.stdlib.ExtraAdder(),
    ]

    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    # TODO Pass a callable to JSONRenderer to format logs as JSON Lines
    logs_render = (
        structlog.dev.ConsoleRenderer(colors=True)
        if enable_console_logs
        else structlog.processors.JSONRenderer()
    )

    _configure_default_logging_by_custom(shared_processors, logs_render)


def _configure_default_logging_by_custom(shared_processors, logs_render):
    handler = logging.StreamHandler()
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            _extract_from_record,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            logs_render,
        ],
    )
    handler.setFormatter(formatter)
    root_uvicorn_logger = logging.getLogger()
    root_uvicorn_logger.addHandler(handler)
    root_uvicorn_logger.setLevel(logging.INFO)


def _extract_from_record(_, __, event_dict):
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    return event_dict


# #4 TODO Add namespace to create_log_event function arguments?
# #4 Do we need to specify a format for, e.g., http_data? The DP logging standards include a list of fields for HTTP events (https://github.com/ONSdigital/dp-standards/blob/main/LOGGING_STANDARDS.md#http-event-data), as well as auth events and errors
# Define a function to create a log event with the specified structure
def create_log_event(
    event: str,
    severity: str,
    http_data: dict = None,
    auth_data: dict = None,
    errors: list = None,
    raw: str = None,
    data: dict = None,
):
    # Create a log event following the specified structure
    log_event = {
        "namespace": "your-service-name",
        "event": event,
        "severity": severity,
    }

    if http_data:
        log_event["http"] = http_data
    if auth_data:
        log_event["auth"] = auth_data
    if errors:
        log_event["errors"] = errors
    if raw:
        log_event["raw"] = raw
    if data:
        log_event["data"] = data

    logger.info(**log_event)


# Handle uncaught exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Log any uncaught exception instead of letting it be printed by Python
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.RootLogger.error(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )

    create_log_event(
        event="Uncaught exception",
        severity="ERROR",
        errors=[{"message": str(exc_value)}],
    )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception
