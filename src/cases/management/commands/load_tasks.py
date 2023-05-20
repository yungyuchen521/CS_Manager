from pathlib import Path
import shutil

from django.core.management import BaseCommand
from django.conf import settings

from src.cases.models import CaseModel, TaskModel


class Command(BaseCommand):
    help = "Load images for `TaskModel` from the given directory"

    IMG_SUFFIX_LIST = ["png", "jpg"]

    def add_arguments(self, parser):
        parser.add_argument("src", type=str, help="root directory of the images")

    def handle(self, *args, **options):
        dir_path = Path(options["src"])
        task_model_list = []
        pending_copies = [] # images to be copied into local storage

        for sub_dir in dir_path.iterdir():
            for img in sub_dir.glob("*"):
                if not img.is_file():
                    raise AssertionError
                
                name, suffix = img.name.split(".")
                if suffix not in self.IMG_SUFFIX_LIST:
                    raise AssertionError
                
                rel_path = Path("tasks") / img.name
                case_id = name.split("_", maxsplit=1)[0]
                case_model = CaseModel.objects.get(case_id=case_id)

                task_model_list.append(
                    TaskModel(
                        img=str(rel_path),
                        case=case_model,
                    )
                )

                src_path = img.resolve()
                dst_path = settings.MEDIA_ROOT / "tasks" / img.name
                assert not dst_path.exists()
                pending_copies.append((src_path, dst_path))

        # make sure that no image overwrites another
        assert len(pending_copies) == len(set(pending_copies))
        
        TaskModel.objects.bulk_create(task_model_list)

        # finally, copy images iff nothing goes wrong
        # making the copy operations atomic with db operations
        for src, dst in pending_copies:
            shutil.copy(src, dst)
