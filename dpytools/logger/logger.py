from typing import Dict, List, Optional, Union
import structlog
import traceback
import json
from datetime import datetime, timezone


def level_to_severity(level: int) -> int:
    """
    Helper to convert logging level to severity, please
    see: https://github.com/ONSdigital/dp-standards/blob/main/LOGGING_STANDARDS.md#severity-levels
    """
    if level > 40:
        return 0
    elif level > 30:
        return 1
    elif level > 20:
        return 2
    else:
        return 3


def create_error_dict(error: Exception) -> List[Dict]:
    """
    Take a python Exception and create a sub dict/document
    matching DP logging standards.
    """

    # Note: "stack trace" guidance is very go orientated,
    # this will be fine for now.
    error_dict = {
        "message": str(error),
        "stack_trace": traceback.format_exc().split("\n"),
    }

    # Listify in keeping with expected DP logging structures
    return [error_dict]


def dp_serializer(event_log, **kw) -> Dict:
    """
    Simple serialiser to align structlog defaults
    with output expected by:
    https://github.com/ONSdigital/dp-standards/blob/main/LOGGING_STANDARDS.md
    """

    # Note: literally just avoiding also logging the superfluous top level
    # "event" key - we just want its contents
    return json.dumps(event_log["event"], **kw)


class DpLogger:
    def __init__(self, namespace: str, test_mode: bool = False):
        """
        Simple python logger to create structured logs in keeping
        with https://github.com/ONSdigital/dp-standards/blob/main/LOGGING_STANDARDS.md

        namespace: (required) the namespace for the app in question
        test_mode: FOR USAGE DURING TESTING ONLY, makes logging statements return their structured logs.
        """
        structlog.configure(
            processors=[structlog.processors.JSONRenderer(dp_serializer)]
        )
        self._logger = structlog.stdlib.get_logger()
        self.namespace = namespace
        self.test_mode = test_mode

    def _log(
        self,
        event,
        level,
        error: Optional[List] = None,
        data: Optional[Dict] = None,
        raw: str = None,
    ):
        log_entry = self._create_log_entry(event, level, data, error, raw)
        self._logger.log(level, log_entry)

        if self.test_mode:
            return log_entry

    def _create_log_entry(self, event, level, data, error, raw) -> Dict:
        log_entry = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "namespace": self.namespace,
            "event": event,
            "trace_id": "not-implemented",
            "span_id": "not-implemented",
            "severity": level_to_severity(level),
            "data": data if data is not None else {},
        }

        if error:
            log_entry["errors"] = create_error_dict(error)

        if raw:
            log_entry["raw"] = raw

        return log_entry

    def debug(self, event: str, raw: str = None, data: Dict = None):
        """
        Log at the debug level.

        event: the thing that's happened, a simple short english statement
        raw  : a raw string of any log messages captured for a third party library
        data : arbitrary key values pairs that may be of use in providing context
        """
        self._log(event, 10, raw=raw, data=data)

    def info(self, event: str, raw: str = None, data: Dict = None):
        """
        Log at the info level.

        event: the thing that's happened, a simple short english statement
        raw  : a raw string of any log messages captured for a third paty library
        data : arbitrary key values pairs that may be of use in providing context
        """
        self._log(event, 20, raw=raw, data=data)

    def warning(self, event: str, raw: str = None, data: Dict = None):
        """
        Log at the warning level.

        event: the thing that's happened, a simple short english statement
        raw  : a raw string of any log messages captured for a third paty library
        data : arbitrary key values pairs that may be of use in providing context
        """
        self._log(event, 30, raw=raw, data=data)

    def error(self, event: str, error: Exception, raw: str = None, data: Dict = None):
        """
        Log at the error level.

        event: the thing that's happened, a simple short english statement
        error: a caught python Exceotion
        raw  : a raw string of any log messages captured for a third paty library
        data : arbitrary key values pairs that may be of use in providing context
        """
        self._log(event, 40, error=error, raw=raw, data=data)

    def critical(
        self, event: str, error: Exception, raw: str = None, data: Dict = None
    ):
        """
        IMPORTANT: You should only be logging at the critical level during
        application failure, i.e if you're app is not in this process of falling
        over you should not be logging a critical.

        Log at the critical level.

        event: the thing that's happened, a simple short english statement
        error: a caught python Exceotion
        raw  : a raw string of any log messages captured for a third paty library
        data : arbitrary key values pairs that may be of use in providing context
        """
        self._log(event, 50, error=error, raw=raw, data=data)
