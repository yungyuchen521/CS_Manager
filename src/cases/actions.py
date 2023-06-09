from typing import List
from threading import Thread

from django.conf import settings

from nn_classifier import Classifier
from src.cases.models import CaseModel, TaskModel
from src.cases.managers import CaseManager, TaskManager


# temporary work-around, classifier should run on a separated server instead
classifier = Classifier()


def analyze_cases(cases: List[CaseModel], force: bool=False):
    manager = CaseManager()

    tasks = []
    for case in cases:
        tasks += manager.get_with_task_set_by_case_id(case.case_id).task_set.all()
    
    if not tasks:
        return

    classify_tasks(tasks, force)

    for case in cases:
        result = manager.get_majority_class_from_tasks(case.case_id)
        if result is not None:
            case.category = result
            case.report = f"Predicted foreign matter: {result}"  # to be replaced by templates
    
    manager.bulk_update(cases=cases, fields=["category", "report"])


def classify_tasks(tasks: List[TaskModel], force: bool=False):
    img_paths = [
        settings.MEDIA_ROOT / task.img.path for task in tasks
        if force or (task.category is None)
    ]  # skip tasks which were already classified if `force` is false
    results = classifier.predict(img_paths)

    for task, result in zip(tasks, results):
        task.category = result

    TaskManager.bulk_update(tasks, fields=["category"])
