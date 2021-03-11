from datetime import datetime
from typing import Any, Dict

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import Cfg
from src.dbbase import Db
from src.device_scraper import DeviceScraper

scraper = DeviceScraper()
db = Db()


def climate_logger(device_name: str):
    "Logging climate data based on device name"
    try:
        print(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " " + device_name)
        result: Dict[str, Any] = scraper._read_device_var(device_name)
        ext_device_id: str = Db().get_device_data_by_name(device_name)["ext_device_id"]
        timestamp: str = result["timestamp"]
        temperature: float = result["temperature"]
        humidity: float = result["humidity"]
        print(device_name + " " + str(temperature))
        print(device_name + " " + str(humidity))
        db.write_climate_logger_device_data(
            ext_device_id, timestamp, temperature, humidity
        )
    except:
        print(
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            + " Failed to load from climate-logger-01"
        )


scheduler = BlockingScheduler()
scheduler.add_job(
    climate_logger, CronTrigger.from_crontab("* * * * *"), ["climate-logger-01"]
)
scheduler.add_job(
    climate_logger, CronTrigger.from_crontab("* * * * *"), ["climate-logger-02"]
)

scheduler.start()
