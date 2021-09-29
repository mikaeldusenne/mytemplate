from os import environ
import logging
import json

from dotenv import load_dotenv
from backend.src import MailSender

class AWSSESHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(AWSSESHandler, self).__init__(*args, **kwargs)

    def try_send_message(self, log_entry):
        try:
            return MailSender.send_email(
                environ["ADMIN_LOG_MAIL"],
                "Log Mail Event",
                log_entry,
            )
        except Exception as ex:
            logging.error("logger mail sending failed")
            raise ex

    def emit(self, record):
        log_entry = self.format(record)
        json_text = json.dumps({"text": log_entry})
        self.try_send_message(log_entry, 1)

