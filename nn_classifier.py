from typing import List
from pathlib import Path

import torch
import torchvision

from src.cases.define import (
    TASK_RESULT_FIBER,
    TASK_RESULT_SCORCH,
    TASK_RESULT_CAKING,
    TASK_RESULT_OTHERS,
)


"""
    Replace `MockModel` with the actual model
"""
class MockModel(torch.nn.Module):
    def forward(self, imgs):
        import time
        time.sleep(5)  # simulate the time cost by the model
        return torch.rand(len(imgs), 4)


class Classifier:
    MODEL_PATH = "nn_model"

    """ change the mapping when the model is ready """
    RESULT_MAPPING = {
        0: TASK_RESULT_CAKING,
        1: TASK_RESULT_FIBER,
        2: TASK_RESULT_SCORCH,
        3: TASK_RESULT_OTHERS,
    } 

    def __init__(self):
        self._model = MockModel()
        """ uncomment the line below when the model is ready at `nn_model` """
        # self._model.load_state_dict(torch.load(self.MODEL_PATH))

    def predict(self, img_paths: List[Path]) -> List[str]:
        imgs = [torchvision.io.read_image(str(path)) for path in img_paths]
        raw_results = self._model(imgs)

        predicted_labels = [int(torch.argmax(res)) for res in raw_results]
        return [self.RESULT_MAPPING[label] for label in predicted_labels]
