import yaml
import os
import pwd

from crontab import CronTab

from .db     import DB

from .device import Device
from .sensor import Sensor

CRON_JOB_ID = 'BOXUS_WATCHDOG_CRON_JOB'

class Manager:

    def seed(self, seed_path):
        db = DB()
        db.connect()

        seed = yaml.load(open(seed_path, 'r').read())

        for s in seed['sensors']:
            new_s = Sensor(db.sensors)

            for k in s:
                new_s[k] = s[k]

            new_s.save()

        for d in seed['devices']:
            new_d = Device(db.devices)

            for k in d:
                new_d[k] = d[k]

            new_d.save()

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
