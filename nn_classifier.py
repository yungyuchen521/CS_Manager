from typing import List
from pathlib import Path

import torch
import torchvision
from PIL import Image

from src.cases.define import (
    CATEGORY_FIBER,
    CATEGORY_SCORCH,
    CATEGORY_CAKING,
    CATEGORY_OTHERS,
)


class Resnet18(torch.nn.Module):
    IMG_SIZE = (224, 224)
    WEIGHTS = "IMAGENET1K_V1"
    CLASS_CNT = 4

    def __init__(self):
        super().__init__()

        self._model = torchvision.models.resnet18(weights=self.WEIGHTS)
        for params in self._model.parameters():
            params.requires_grad = False

        self._model.fc = torch.nn.Sequential(
            torch.nn.Dropout(p=0.7, inplace=False),
            torch.nn.Linear(in_features=512, out_features=self.CLASS_CNT, bias=True),
        )

    def forward(self, imgs: torch.Tensor):
        return self._model(imgs)
    

class Classifier:
    MODEL_PATH = "nn_model"

    RESULT_MAPPING = {
        0: CATEGORY_CAKING,
        1: CATEGORY_FIBER,
        2: CATEGORY_OTHERS,
        3: CATEGORY_SCORCH,
    }

    def __init__(self):
        self._model = Resnet18()
        self._model.load_state_dict(torch.load(self.MODEL_PATH, map_location=torch.device("cpu")))

    def predict(self, img_paths: List[Path]) -> List[str]:
        if len(img_paths) == 0:
            return []

        imgs = [Image.open(p) for p in img_paths]
        imgs = [self._preprocess(img) for img in imgs]
        imgs = torch.stack(imgs)

        self._model.eval()
        raw_results = self._model(imgs)

        predicted_labels = [int(torch.argmax(res)) for res in raw_results]
        return [self.RESULT_MAPPING[label] for label in predicted_labels]

    def _preprocess(self, imgs: torch.Tensor) -> torch.Tensor:
        transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Resize(self._model.IMG_SIZE, antialias=True),
            ]
        )

        return transform(imgs)
