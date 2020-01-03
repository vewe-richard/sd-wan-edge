import json
import os
from scripts.utils import Utils

if __name__ == "__main__":
    with open('config.json') as json_file:
        config = json.load(json_file)
        config["CMD"] = "query"
        print(Utils().http_post("/north/", config))
