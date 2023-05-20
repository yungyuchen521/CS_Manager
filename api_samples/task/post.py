import os
import requests

# create a new `Task`
def post(img_path: str, case_id: str):
    return requests.post(
        url="http://127.0.0.1:8000/task",
        data={"case": case_id},
        files={"img": open(img_path, "rb")}
    )


if __name__ == "__main__":
    # python post.py img_path="path to image" case_id="case_id"

    kwargs = dict(
        kwarg.split("=")
        for kwarg in os.sys.argv[1:]
    )
    
    resp = post(**kwargs)
    print(resp.status_code)
    print(resp.json())
