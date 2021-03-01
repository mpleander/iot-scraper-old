from datetime import datetime
from typing import Any, Dict

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import Cfg
from src.dbbase import Db
from src.device_scraper import DeviceScraper

scraper = DeviceScraper()
db = Db()


def climate_logger_01():
    try:
        print(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " climate-logger-01")
        result: Dict[str, Any] = scraper._read_device_var("climate-logger-01")
        ext_device_id = Db().get_device_data_by_name("climate-logger-01")[
            "ext_device_id"
        ]
        timestamp: str = result["timestamp"]
        temperature: float = result["temperature"]
        humidity: float = result["humidity"]
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
    climate_logger_01, CronTrigger.from_crontab("0 * * * *")
)
# scheduler.add_job(climate_logger_01, 'interval', minutes=1)
scheduler.start()
