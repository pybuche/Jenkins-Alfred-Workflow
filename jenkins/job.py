import os
import urllib
from time import time
from datetime import datetime

class Job(object):
    def __init__(self, data):
        self._data = data

    @staticmethod
    def format_time_diff(diff):
        if not diff:
            return 'N/A'
        diff = diff // 1000
        # days
        days = diff // 86400
        # remaining seconds
        diff = diff - (days * 86400)
        # hours
        hours = diff // 3600
        # remaining seconds
        diff = diff - (hours * 3600)
        # minutes
        minutes = diff // 60
        # remaining seconds
        seconds = diff - (minutes * 60)
        # total time
        if days:
            return '{}d{}h'.format(days, hours)
        elif hours:
            return '{}h{}m'.format(hours, minutes)
        elif minutes:
            return '{}m{}s'.format(minutes, seconds)
        else:
            return '{}s'.format(seconds)

    @property
    def name(self):
        return urllib.unquote(self._data.get('name', ''))

    @property
    def url(self):
        return self._data.get('url')

    @property
    def status(self):
        return self._data.get('color')

    @property
    def image(self):
        return "{}/images/{}.png".format(os.getcwdu(), self.status)

    @property
    def description(self):
        return self._data.get('description', "")

    @property
    def last_build_url(self):
        last_build = self._data.get('lastBuild', {}).get('url')
        return '{}console#footer'.format(last_build)

    @property
    def build_infos(self):
        now = int(time()) * 1000 # Since jenkins timestamps are in ms
        # print self._data.get('lastSuccessfulBuild', {}).get('timestamp')
        last = self._data.get('lastBuild', {})
        last_success = self._data.get('lastSuccessfulBuild', {})
        last_fail = self._data.get('lastFailedBuild', {})

        last_success_duration = last_success.get('duration') if last_success else None
        last_duration = last.get('duration') if last else None
        last_success_timestamp = last_success.get('timestamp', now) if last_success else now
        last_fail_timestamp = last_fail.get('timestamp', now) if last_fail else now

        return "Last duration: {} - Last success: {} - Last fail: {}".format(
            self.format_time_diff(last_duration if last_duration else last_success_duration),
            self.format_time_diff(now - last_success_timestamp),
            self.format_time_diff(now - last_fail_timestamp)
        )
