import yaml
import os
import pwd

from crontab import CronTab

from .device import Device
from .sensor import Sensor

CRON_JOB_ID = 'BOXUS_WATCHDOG_CRON_JOB'

class Manager:

    db = None

    def __init__(self, db = None):
        if db:
            self.db = db

    def seed(self, seed_path):
        seed = yaml.load(open(seed_path, 'r').read())

        for db_name, Cls in [['sensors', Sensor], ['devices', Device]]:
            for r in seed[db_name]:
                new_r = Cls(self.db)

                for k in r:
                    new_r[k] = r[k]

                new_r.save()

    def install_cron(self, command, interval):
        # Current user cron
        user_cron = CronTab(pwd.getpwuid(os.getuid()).pw_name)

        old_jobs = user_cron.find_comment(CRON_JOB_ID)
        for j in old_jobs:
            user_cron.remove(j)

        job = user_cron.new(command=command, comment=CRON_JOB_ID)
        job.minute.every(interval)
        job.enable()

        user_cron.write()
