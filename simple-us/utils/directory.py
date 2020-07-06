import errno
import os
from pathlib import Path
import re
import shutil
from typing import List


class SIMPLEUtil:

    WORKING_DIR: Path = Path.home().joinpath("SimpleUSRun")
    PRIVATE_JOBS_DIR: Path = WORKING_DIR.joinpath("job")
    SHARED_JOBS_DIR: Path = Path('/data/groups/simpleggroup/job')

    # APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    # DATA_DIR = SRC_DIR + "/data"
    # CORNSOY_SUPP_DIR = SRC_DIR + "/inputs/CornSoy/supp_files"

    @staticmethod
    def mkdir(dir_: Path):
        if not dir_.exists():
            dir_.mkdir(parents=True, exist_ok=True)

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
                print('Directory not copied. Error: %s' % e)

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
        os.system('rm -rf ' + str(dir_))

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
                    print(key, value)
                    # return "-cl QLAND_CUSTOM.txt" if <QLAND_CUSTOM> is found
                    option_string += value + " " + key.strip('<>')+".txt  "
                    print(option_string)
        return option_string

    @staticmethod
    def result_path(jobid: int, is_private=True):
        job_dir = SIMPLEUtil.PRIVATE_JOBS_DIR if is_private else SIMPLEUtil.SHARED_JOBS_DIR
        result_path = job_dir / Path(str(jobid)) / Path("outputs") / Path("results")
        return result_path

    @staticmethod
    def build_result_list(jobid: int):
        # example resultPath is self.jobpath + "/results"

        result_path = SIMPLEUtil.result_path(jobid)
        SIMPLEUtil.mkdir(result_path)

        root = str(result_path)
        print("root :", root)

        result_list = {}

        dir_list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
        print("dirlist: ", dir_list)

        for dir_ in dir_list:
            result_list[dir_] = {}
            root2 = root + "/" + dir_
            dirlist2 = [item for item in os.listdir(root2) if os.path.isdir(os.path.join(root2, item))]
            for dir2 in dirlist2:
                result_list[dir_][dir2] = {}
                root3 = root + "/" + dir_ + "/" + dir2
                dirlist3 = [item for item in os.listdir(root3) if os.path.isdir(os.path.join(root3, item))]
                for dir3 in dirlist3:
                    result_list[dir_][dir2][dir3] = []
                    root4 = root + "/" + dir_ + "/" + dir2 + "/" + dir3
                    dirlist4 = [item for item in os.listdir(root4) if os.path.isdir(os.path.join(root4, item))]
                    dirlist4.sort()
                    for dir4 in dirlist4:
                        result_list[dir_][dir2][dir3].append(dir4)

        return result_list

    @staticmethod
    def intersect_result_lists(first_list: dict, second_list: dict):
        # consider directories in level 1
        first_dirs_1 = [key for key in first_list.keys()]
        second_dirs_1 = [key for key in second_list.keys()]
        dirs_1 = [dir_ for dir_ in first_dirs_1 if dir_ in second_dirs_1]

        result_list = {}
        for dir_1 in dirs_1:
            pass
            # TODO: Finish this
