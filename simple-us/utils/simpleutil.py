import errno
import os
from os import symlink
from os import listdir
from pathlib import Path
import re
import shutil
from typing import List

from notebook import notebookapp


def base_url() -> str:
    if ("HOSTNAME" in os.environ.keys()) and ("mygeohub" in os.environ["HOSTNAME"]):
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


class SIMPLEUtil:

    WORKING_DIR: Path = Path.home() / "SimpleUSRun"
    PRIVATE_JOBS_DIR: Path = WORKING_DIR / "job"
    SHARED_JOBS_DIR: Path = Path('/data/groups/simpleggroup/job')
    SHARED_JOBS_SYM_LINK: Path = WORKING_DIR / "shared"  # For mygeohub's Jupyter. It needs a path relative to home
    TEMP_DIR: Path = WORKING_DIR / "temp"  # To store temp directories for display/comparison "sessions"
    BASE_URL = base_url()  # For Jupyter server. It is assumed the server is started from the home directory
    PRIVATE_JOBS_URL = BASE_URL + "/SimpleUSRun/job"
    SHARED_JOBS_URL = BASE_URL + "/SimpleUSRun/shared"

    if not WORKING_DIR.exists():
        WORKING_DIR.mkdir(parents=True)
    if not PRIVATE_JOBS_DIR.exists():
        PRIVATE_JOBS_DIR.mkdir(parents=True)
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir(parents=True)
    if SHARED_JOBS_DIR.exists() and not SHARED_JOBS_SYM_LINK.exists():
        symlink(str(SHARED_JOBS_DIR), str(SHARED_JOBS_SYM_LINK))

    # directory
    # APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    # DATA_DIR = SRC_DIR + "/data"
    # CORNSOY_SUPP_DIR = SRC_DIR + "/inputs/CornSoy/supp_files"

    @classmethod
    def init_working_directory(cls):
        shutil.rmtree(str(cls.TEMP_DIR))
        cls.TEMP_DIR.mkdir(parents=True)

    @staticmethod
    def experiment_result_path(exp_id_str: str, make_path=True) -> Path:
        from model import Experiment

        id = Experiment.to_id(exp_id_str)
        is_private = Experiment.is_private_id_str(exp_id_str)
        job_dir = SIMPLEUtil.PRIVATE_JOBS_DIR if is_private else SIMPLEUtil.SHARED_JOBS_SYM_LINK
        result_path = job_dir / Path(str(id)) / Path("outputs") / Path("results")

        if make_path:
            result_path.mkdir(parents=True, exist_ok=True)
        return result_path

    @staticmethod
    def new_session_id() -> int:
        sessions = listdir(str(SIMPLEUtil.TEMP_DIR))
        max_ = 0
        for session in sessions:
            try:
                max_ = max(max_, int(session))
            except:
                continue
        max_ += 1
        return max_

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
    def get_custom_shocks_options(jobid: int):

        file_path = SIMPLEUtil.PRIVATE_JOBS_DIR / Path(str(jobid)) / Path("outputs") / Path("SIMPLE_G.cmf")

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