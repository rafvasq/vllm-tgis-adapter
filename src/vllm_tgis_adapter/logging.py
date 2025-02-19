import json
import logging
import os

from vllm.logger import (
    DEFAULT_LOGGING_CONFIG,
    init_logger,  # noqa: F401
)

DEFAULT_LOGGER_NAME = __name__.split(".")[0]

config = {**DEFAULT_LOGGING_CONFIG}

config["formatters"][DEFAULT_LOGGER_NAME] = DEFAULT_LOGGING_CONFIG["formatters"]["vllm"]
config["filters"][DEFAULT_LOGGER_NAME] = DEFAULT_LOGGING_CONFIG["filters"][
    "vllm_redact"
]

handler_config = DEFAULT_LOGGING_CONFIG["handlers"]["vllm"]
handler_config["formatter"] = DEFAULT_LOGGER_NAME
handler_config["filters"] = [DEFAULT_LOGGER_NAME]
config["handlers"][DEFAULT_LOGGER_NAME] = handler_config

logger_config = DEFAULT_LOGGING_CONFIG["loggers"]["vllm"]
logger_config["handlers"] = [DEFAULT_LOGGER_NAME]
config["loggers"][DEFAULT_LOGGER_NAME] = logger_config

# Extract log filter patterns from the environment variable
patterns = []
vllm_log_filter_patterns = os.getenv("VLLM_LOG_FILTER_PATTERNS")
if vllm_log_filter_patterns:
    try:
        # Parse the patterns from JSON
        patterns = json.loads(vllm_log_filter_patterns)
    except json.JSONDecodeError:
        logging.warning("Invalid JSON format in VLLM_LOG_FILTER_PATTERNS")

DEFAULT_LOGGING_CONFIG["filters"]["vllm_redact"]["patterns"] = patterns

logging.config.dictConfig(config)
