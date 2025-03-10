import os
import sys
import json
import logging
import traceback

from datetime import datetime
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("Main")
logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        prefix = "%d-%m-%Y"
        now = datetime.now()
        filename = f"{now.strftime(prefix)}_log.json"

        if os.path.isfile(f"backend/logs/{filename}"):
            with open(f"backend/logs/{filename}") as feedsjson:
                feeds = json.load(feedsjson)

            feeds.append(log_record)
            with open(f"backend/logs/{filename}", mode="w") as f:
                f.write(json.dumps(feeds, indent=4, ensure_ascii=False))
        else:
            with open(f"backend/logs/{filename}", mode="w") as f:
                f.write(json.dumps([log_record], indent=4, ensure_ascii=False))


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel("INFO")


def finchik_excepthook(ex_type, ex_value, ex_traceback):
    logger.info(
        "Не обработанная ошибка",
        extra={
            "exception_type": ex_type.__name__,
            "exception_message": str(ex_value),
            "traceback": "\n".join(traceback.format_tb(ex_traceback)),
            "stack_trace": traceback.format_stack(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "process_id": os.getpid(),
            "platform": sys.platform,
            "python_version": sys.version,
            "python_executable": sys.executable,
            "python_build": sys.version_info,
            "python_compiler": sys.getcompiler(),
            "python_implementation": sys.implementation.name,
            "python_executable_path": sys.executable,
            "python_prefix": sys.prefix,
            "python_suffix": sys.suffix,
        },
    )
