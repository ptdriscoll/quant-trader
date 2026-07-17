from collections import Counter, deque
from datetime import datetime
from zoneinfo import ZoneInfo
import time

class ApiMetrics:
    def __init__(self):
        self.start_time = time.time()

        self.request_times = deque()
        self.endpoint_counts = Counter()

        self.total_requests = 0
        self.failed_requests = 0
        self.retry_count = 0
        self.reconnect_count = 0

        self.peak_requests_per_minute = 0

    def record_request(self, endpoint='Unknown'):
        now = time.time()

        self.total_requests += 1
        self.endpoint_counts[endpoint] += 1
        self.request_times.append(now)

        while self.request_times and self.request_times[0] < now - 60:
            self.request_times.popleft()

        self.peak_requests_per_minute = max(
            self.peak_requests_per_minute,
            len(self.request_times)
        )

    @property
    def requests_last_minute(self):
        return len(self.request_times)

    @property
    def uptime_seconds(self):
        return int(time.time() - self.start_time)

    @property
    def average_requests_per_minute(self):
        uptime_minutes = self.uptime_seconds / 60

        if uptime_minutes == 0:
            return 0

        return self.total_requests / uptime_minutes

    def record_retry(self):
        self.retry_count += 1

    def record_failure(self):
        self.failed_requests += 1

    def record_reconnect(self):
        self.reconnect_count += 1

    def print_summary(self):
        eastern = ZoneInfo('America/New_York')
        now = datetime.now(eastern)

        uptime = self.uptime_seconds
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        if days:
            uptime_string = f'{days}d {hours}h {minutes}m'
        elif hours:
            uptime_string = f'{hours}h {minutes}m'
        else:
            uptime_string = f'{minutes}m'

        print('\n📊 API Metrics')
        print(
            f'As of: {now.strftime("%Y-%m-%d %H:%M:%S ET")} '
            f'(Uptime: {uptime_string})'
        )
        print('----------------')

        print(f'Total Requests: {self.total_requests}')
        print(f'Requests/min: {self.requests_last_minute}')
        print(f'Average Requests/min: {self.average_requests_per_minute:.1f}')
        print(f'Peak Requests/min: {self.peak_requests_per_minute}')

        print('\nReliability')
        print(f'  Failures: {self.failed_requests}')
        print(f'  Retries: {self.retry_count}')
        print(f'  Reconnects: {self.reconnect_count}')

        print('\nBy Endpoint:')

        for endpoint, count in sorted(self.endpoint_counts.items()):
            print(f'  {endpoint}: {count}')