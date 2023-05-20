import os
import requests

# update existing `Task`
def patch(**kwargs):
    id = kwargs.pop("id")

    data = kwargs
    files = {}

    if "img_path" in data:
        img_path = data.pop("img_path")
        files["img"] = open(img_path, "rb")

    return requests.patch(
        url=f"http://127.0.0.1:8000/task?id={id}",
        data=data,
        files=files
    )


if __name__ == "__main__":
    # python patch.py id="id of task" img_path="path to image" category="..." result="..."

    kwargs = dict(
        kwarg.split("=")
        for kwarg in os.sys.argv[1:]
    )

    resp = patch(**kwargs)
    print(resp.status_code)
    print(resp.json())
