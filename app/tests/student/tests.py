import json
import os


def load_student_data() -> dict:
    curr_dir = os.path.dirname(__file__)

    path = os.path.join(curr_dir, "data.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file {path} not found")

    with open(path, "r") as f:
        data = json.load(f)

    return data


