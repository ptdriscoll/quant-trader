from collections import deque, Counter
import time


class ApiMetrics:

    def __init__(self):
        self.request_times = deque()
        self.total_requests = 0
        self.failed_requests = 0
        self.retry_count = 0
        self.reconnect_count = 0
        self.peak_requests_per_minute = 0
        self.request_counts = Counter()
        
    def reset(self):
        self.request_times.clear()
        self.total_requests = 0
        self.failed_requests = 0
        self.retry_count = 0
        self.reconnect_count = 0
        self.peak_requests_per_minute = 0
        self.request_counts.clear()          

    def record_request(self, method_called=None):
        now = time.time()

        self.total_requests += 1

        if method_called:
            self.request_counts[method_called] += 1

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

    def get_request_summary(self):
        return dict(self.request_counts)

    def record_retry(self):
        self.retry_count += 1

    def record_failure(self):
        self.failed_requests += 1

    def record_reconnect(self):
        self.reconnect_count += 1   
        
    def print_summary(self):

        print('\n📊 API Metrics')
        print('----------------')
        print(f'Total Requests: {self.total_requests}')
        print(f'Requests/min: {self.requests_last_minute}')
        print(f'Peak/min: {self.peak_requests_per_minute}')
        print(f'Failures: {self.failed_requests}')
        print(f'Retries: {self.retry_count}')
        print('\nBy Endpoint:')

        for method, count in self.request_counts.items():
            print(f'  {method}: {count}')

        print() # Add terminal spacing        
