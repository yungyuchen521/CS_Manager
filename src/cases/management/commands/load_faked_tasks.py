from datetime import date, timedelta
from pathlib import Path
import random
import shutil

from django.core.management import BaseCommand
from django.conf import settings

from src.cases.models import CaseModel, TaskModel


class Command(BaseCommand):
    IMG_SUFFIX_LIST = ["png", "jpg", "jpeg"]

    def add_arguments(self, parser):
        parser.add_argument("src", type=str, help="root directory of the images")

    def handle(self, *args, **options):
        dir_path = Path(options["src"])

        today = date(year=2023, month=2, day=28)
        delta_list = list(range(365))
        random.shuffle(delta_list)

        batch_no_list = [
            "".join(random.choices("0123456789", k=10))
            for _ in range(30)
        ]

        case_model_list = []
        task_model_list = []
        pending_copies = []

        for sub_dir in dir_path.iterdir():
            imgs_in_folder = [
                img for img in sub_dir.glob("*")
                if img.is_file() and (img.name.split(".")[-1].lower() in self.IMG_SUFFIX_LIST)
            ]

            while imgs_in_folder:
                rand_date = today - timedelta(days=delta_list[0])
                new_case = CaseModel(
                    case_id=rand_date.strftime("%Y%m%d"),
                    product_name=random.choice(["PGSG", "SMAG", "ULTIMA_1", "ULTIMA_3", "ILLUMA_HA"]),
                    batch_no=random.choice(batch_no_list),
                    created_at=rand_date,
                )
                case_model_list.append(new_case)
                delta_list = delta_list[1:]

                task_cnt = self._rand_task_cnt()
                imgs = imgs_in_folder[:task_cnt]
                imgs_in_folder = imgs_in_folder[task_cnt:]
                for img in imgs:
                    new_task = TaskModel(
                        img=str(Path("tasks") / img.name),
                        case=new_case,
                    )
                    task_model_list.append(new_task)

                    dst_path = settings.MEDIA_ROOT / "tasks" / img.name
                    assert not dst_path.exists()
                    src_path = img.resolve()
                    pending_copies.append((src_path, dst_path))

        assert len(pending_copies) == len(set(pending_copies))     
        CaseModel.objects.bulk_create(case_model_list)
        TaskModel.objects.bulk_create(task_model_list)

        for src, dst in pending_copies:
            shutil.copy(src, dst)

    def _rand_task_cnt(self) -> int:
        n = random.randint(1, 10)
        if n >= 8:
            return 3
        elif n >= 5:
            return 2
        else:
            return 1
