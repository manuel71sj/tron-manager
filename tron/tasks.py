import time
from datetime import timedelta

from boot.celery import app


@app.task
def add(x, y):
    start = time.process_time()

    sum = 0

    for i in range(x):
        for j in range(y):
            sum += j

    end = time.process_time()
    print("Time elapsed: ", end - start)  # seconds
    print("Time elapsed: ", timedelta(seconds=end - start))
    return "end"
