from datetime import datetime
from zoneinfo import ZoneInfo

def logs(log):
    mst = ZoneInfo("America/Denver")
    timestamp = datetime.now(mst).strftime("%m/%d/%Y %H:%M:%S")
    print(f"{timestamp} || {log}")
