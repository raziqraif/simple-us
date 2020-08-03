import errno
import os
from os import symlink
from pathlib import Path
import re
import shutil
from subprocess import call
import sys
from typing import List

from notebook import notebookapp


def in_mygeohub():
    return ("HOSTNAME" in os.environ.keys()) and ("mygeohub" in os.environ["HOSTNAME"])


def base_url() -> str:
    if in_mygeohub():
        # From geotiff tutorial code
        url = "https://proxy.mygeohub.org"
        nb = None
        session = os.environ['SESSION']
        servers = list(notebookapp.list_running_servers())
        for server in servers:
            if session in server['base_url']:
                nb = server['base_url']
                nb_dir = server['notebook_dir']
                break
        url += nb + "tree"
    else:
        url = "http://localhost:8888/tree"
    return url


def shared_jobs_dir() -> Path:
    if ("HOSTNAME" in os.environ.keys()) and ("mygeohub" in os.environ["HOSTNAME"]):
        return Path('/data/groups/simpleggroup/job')
    else:
        return Path.home() / "shared_jobs"


class SIMPLEUtil:
    WORKING_DIR: Path = Path.home() / "SimpleUSRun"
    PRIVATE_JOBS_DIR: Path = WORKING_DIR / "job"
    SHARED_JOBS_DIR: Path = shared_jobs_dir()
    SHARED_JOBS_SYM_LINK: Path = WORKING_DIR / "shared"  # For mygeohub's Jupyter. It needs a path relative to home

    TEMP_DIR: Path = WORKING_DIR / "temp"  # To store temp directories for display/comparison "sessions"
    LOG_FILE: Path = TEMP_DIR / "simple-us.log"
    BASE_URL = base_url()  # For Jupyter server. It is assumed the server is started from the home directory
    PRIVATE_JOBS_URL = BASE_URL + "/SimpleUSRun/job"
    SHARED_JOBS_URL = BASE_URL + "/SimpleUSRun/shared"

    # TODO: Update this because the project structure has changed
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    DATA_DIR = SRC_DIR + "/data"
    CORNSOY_SUPP_DIR = SRC_DIR + "/inputs/CornSoy/supp_files"

    @classmethod
    def initialize_working_directory(cls):
        if not cls.WORKING_DIR.exists():
            cls.WORKING_DIR.mkdir(parents=True)
        if not cls.PRIVATE_JOBS_DIR.exists():
            cls.PRIVATE_JOBS_DIR.mkdir(parents=True)
        if not cls.TEMP_DIR.exists():
            cls.TEMP_DIR.mkdir(parents=True)
        if not cls.LOG_FILE.exists():
            cls.LOG_FILE.touch()
        if cls.SHARED_JOBS_DIR.exists() and not cls.SHARED_JOBS_SYM_LINK.exists():
            symlink(str(cls.SHARED_JOBS_DIR), str(cls.SHARED_JOBS_SYM_LINK))
        shutil.rmtree(str(cls.TEMP_DIR))
        cls.TEMP_DIR.mkdir(parents=True)


    @classmethod
    def upload_file(cls, save_path: Path):
        if in_mygeohub():
            call(["/usr/bin/importfile", str(save_path)])

    @classmethod
    def download_file(cls, file_path: Path):
        if in_mygeohub():
            call(["/usr/bin/exportfile", str(file_path)])

    @staticmethod
    def copy(src: Path, dest: Path):
        src = str(src)
        dest = str(dest)
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                raise Exception("Directory not copied")

    # does not chmod for directories
    @staticmethod
    def make_readable_recursive(dest: Path):
        dest = str(dest)
        for root, dirs, files in os.walk(dest):
            for momo in dirs:
                dirpath = os.path.join(root, momo)
                old_stat = os.stat(dirpath)
                # directory must have execute bit for directory traversing
                os.chmod(dirpath, old_stat.st_mode | 0o755)
            for momo in files:
                filepath = os.path.join(root, momo)
                old_stat = os.stat(filepath)
                os.chmod(filepath, old_stat.st_mode | 0o764)

    @staticmethod
    def rmdir(dir_: Path):
        if dir_.exists() and dir_.is_dir():
            shutil.rmtree(str(dir_))

    @staticmethod
    def replace_file(file_path: Path, str_ori: str, str_dst: str):
        file_path = str(file_path)
        with open(file_path, 'r') as f:
            co = f.read()
            new_co = re.sub(str(str_ori), str(str_dst), co)
            with open(file_path, 'w') as fw:
                fw.write(new_co)

    @staticmethod
    def create_custom_file(file_path: Path, val_list: List[any]):
        file_path = str(file_path)
        with open(file_path, 'w') as f:
            f.write(str(len(val_list))+" REAL;\n")
            for v in val_list:
                f.write(str(v)+"\n")

    @staticmethod
    def get_custom_shocks_options(id_str: str):
        from model import Experiment
        assert Experiment.is_private_id_str(id_str)
        from .experimentutil import ExperimentManager

        file_path = ExperimentManager.outputs_directory(id_str) / Path("SIMPLE_G.cmf")
        customs = {'<QLAND_CUSTOM>': '-cl',
                   '<QNITRO_CUSTOM>': '-cn',
                   '<QWATER_CUSTOM>': '-cw',
                   # baseline custom files
                   '<POP_CUSTOM>': '-bp',
                   '<INCOME_CUSTOM>': '-bi',
                   '<BIOFUEL_CUSTOM>': '-bf',
                   '<CROPPDVT_CUSTOM>': '-bc',
                   '<ANIMALPDVT_CUSTOM>': '-ba'
                   }
        option_string = ""
        with open(file_path, 'r') as f:
            co = f.read()

            for key, value in customs.items():
                if key in co:
                    # return "-cl QLAND_CUSTOM.txt" if <QLAND_CUSTOM> is found
                    option_string += value + " " + key.strip('<>')+".txt  "
        return option_string
