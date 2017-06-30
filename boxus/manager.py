import os
import pwd

from crontab import CronTab

CRON_JOB_ID = 'BOXUS_WATCHDOG_CRON_JOB'

class Manager:

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
