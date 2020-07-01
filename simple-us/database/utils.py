# This module contains dummy data/methods for now

import os
from pathlib import Path

# TODO: Update this when porting to jupyter notebook on mygeohub
try:
    HOSTNAME = os.environ["HOSTNAME"]
except:
    HOSTNAME = ""

if "mygeohub" in HOSTNAME[:8]:
    PRIVATE_JOBS_DIR = Path("~/simpleUSRun/job")
else:
    # TODO: Update your local job directory
    PRIVATE_JOBS_DIR = Path("C:\\Users\\muhdr\\Documents\\simple-us\\job")
SHARED_JOBS_DIR = Path("Dummy path")

# Column number in database
JOB_ID = 0
SUBMIT_ID = 1
SUBMIT_TIME = 2
AUTHOR = 3
JOB_STATUS = 4
JOB_NAME = 5
MODEL_TYPE = 6
PUBLISHED = 7
DESCRIPTION = 8


def mkdir_p(path: str):
    pass
