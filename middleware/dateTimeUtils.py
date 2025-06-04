from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

class dateTimeUtils():
    def __init__(self):
        self.expires_recovery_code = int(os.getenv("EXPIRES_RECOVERY_CODE"))

    def getTime(self, timeDb):
        timeDbFormat = datetime.strptime(timeDb, "%Y-%m-%dT%H:%M:%S.%f")
        if not isinstance(timeDbFormat, datetime):
            raise ValueError("timeDbFormat must be a datetime object")

        time_now = datetime.now()
        time_diff = time_now - timeDbFormat
        elapsed_time = time_diff.total_seconds() / 60

        return elapsed_time > self.expires_recovery_code

    def getCalculateDates(self):
        today = datetime.now()
        return {
            "current_date": today.strftime('%Y-%m-%d'),
            "date_3_months_ago": (today - relativedelta(months=3)).strftime('%Y-%m-%d')
        }