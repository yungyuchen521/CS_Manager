from typing import List
from threading import Thread

from django.conf import settings

from nn_classifier import Classifier
from src.cases.models import TaskModel
from src.cases.managers import TaskManager


def thread(func):
    def wrapper(*args):
        Thread(target=func, args=args).start()

    return wrapper

# temporary work-around, classifier should run a separated server
classifier = Classifier()

@thread
def classify_images(tasks: List[TaskModel]):
    img_paths = [settings.MEDIA_ROOT / task.img.path for task in tasks]
    results = classifier.predict(img_paths)

    for task, result in zip(tasks, results):
        task.category = result

    TaskManager.bulk_update(tasks, fields=["category"])
