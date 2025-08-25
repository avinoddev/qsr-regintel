
import os
from celery import Celery

app = Celery("regintel", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
app.conf.update(task_acks_late=True, worker_prefetch_multiplier=1, task_time_limit=600)
