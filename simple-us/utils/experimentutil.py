import glob
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Tuple, Optional, List

from model import Experiment
from database import DBManager


# This class is modified from the original simpleus' JobManager class


class ExperimentManager:
    db = DBManager()
    params = {}

    DEFAULT_WALTIME = 300  # minute
    TOOL_REV_CORNSOY = 'runSIMPLE_US_corn-r61'
    TOOL_REV_ALLCROPS = 'runSIMPLE_US_corn'  # TODO: change later when allcrops script is ready by Steve
    jobid = None

    @classmethod
    def working_directory(cls, id_str: str) -> Path:
        from .simpleutil import SIMPLEUtil
        id_ = str(Experiment.to_id(id_str))
        if Experiment.is_private_id_str(id_str):
            return SIMPLEUtil.PRIVATE_JOBS_DIR / id_
        else:
            return SIMPLEUtil.SHARED_JOBS_SYM_LINK / id_

    @classmethod
    def outputs_directory(cls, id_str: str) -> Path:
        return cls.working_directory(id_str) / "outputs"

    @classmethod
    def results_directory(cls, id_str: str) -> Path:
        return cls.outputs_directory(id_str) / "results"

    @classmethod
    def supplementary_directory(cls, id_str: str) -> Path:
        return cls.working_directory(id_str) / "supp"

    @classmethod
    def _initialize_working_directory(cls, id_str) -> bool:
        #  Create working, output, and supp directory. If already existed, re-initialize it
        work_dir = cls.working_directory(id_str)
        outputs_dir = cls.outputs_directory(id_str)
        supp_dir = cls.supplementary_directory(id_str)
        if work_dir.exists():
            shutil.rmtree(str(work_dir))
        work_dir.mkdir(parents=True)
        outputs_dir.mkdir(parents=True)
        supp_dir.mkdir(parents=True)
        return True

    ###########################################################
    # job submission.
    # Jungha Woo
    # model can be either 'Custom AllCrops' or 'Custom CornSoy'
    ###########################################################
    @classmethod
    def submit_experiment(cls, model: str, name: str, description: str) -> Tuple[bool, Optional[Experiment]]:
        # get new job id form DB
        experiment = cls.db.new_experiment(model=model, name=name, description=description)
        if experiment is None:
            return False, experiment

        id_str = experiment.id_str
        cls._initialize_working_directory(id_str)
        working_dir = cls.working_directory(id_str)
        outputs_dir = cls.outputs_directory(id_str)

        # TODO: Remove these after this method has been properly implemented
        experiment.status = "Pending"
        cls.db.update_experiment(experiment)
        return True, experiment

        # TODO: Implement "control" and finish this method
        """
        os.chdir(str(outputs_dir))

        waltime = cls.DEFAULT_WALTIME

        # prepare CMF input file
        source_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

        os.system('cp %s/SIMPLE_G.cmf %s' % (source_dir + "/bin", outputs_dir))
        sys.stdout.flush()
        # SIMPLE-G-mapping_file.csv is required to get readable string for each shock variables in the output dialog
        os.system('cp -r %s %s' % (SIMPLEUtil.CORNSOY_SUPP_DIR, working_dir))

        # TODO: Implement control class
        # NOTE: From the svn, it seems like control does not have to be instantiated. So, apply_baseline_shocks could
        # probably be a classmethod/staticmethod
        control = None
        if (experiment is not None) and (control is not None):
            # write baseline shocks to CMF
            control.apply_baseline_shocks(id_str)  # TODO: Implement this
            # write policy shocks to the CMF file
            control.set_policy_tab.get_all_policies(id_str)  # TODO: Implement this
        else:
            print("Job submit failed ")
            return False, None

        if model == 'CornSoy':
            tool_rev = cls.TOOL_REV_CORNSOY
        else:
            tool_rev = cls.TOOL_REV_ALLCROPS

        option_string_customfiles = SIMPLEUtil.get_custom_shocks_options(id_str)
        # submit job
        # TODO: Add custom file uploads
        jobcmd = 'submit -w ' + str(waltime) + \
                 ' --detach' + \
                 ' ' + tool_rev + \
                 ' -cmf SIMPLE_G.cmf ' + \
                 option_string_customfiles

        print("jobcmd:", jobcmd)
        sys.stdout.flush()
        print('\n> Job submission command : ')
        print(jobcmd)

        # return True, ''

        ret = subprocess.check_output(jobcmd.split())
        if 'Detaching from run' not in ret:
            # job submission error
            experiment.status = "Failed"
            cls.db.update_experiment(experiment)
            # return False, ret.replace('\\n','\n')  # TODO: What is the format of ret?

        print(ret.replace('\\n', '\n'))

        # get job submission id
        submit_id = ret.split()[3][:-1]
        print('\n> Job has been submitted successfully. Cluster job submission id : ', submit_id)

        experiment.submission_id = submit_id
        experiment.status = "Pending"
        experiment.model = model
        experiment.published = 0
        updated = cls.db.update_experiment(experiment)

        if not updated:
            return False, None
        return True, experiment
        """

    @classmethod
    def update_experiments_status(cls, experiments: List[Experiment]):
        # TODO: test this
        # Note: before this, the experiments are loaded from the db in this method. They are now passed as an arg
        # to avoid expensive db calls

        for experiment in experiments:
            if (not experiment.is_private) or (experiment.status == "Completed") or (experiment.status == "Failed"):
                continue
            if experiment.status in ['Pending', 'Queued', 'Running', 'Completing']:
                experiment.status = cls.get_experiment_status(experiment)
                cls.db.update_experiment(experiment)

        sys.stdout.flush()

    @classmethod
    def get_experiment_status(cls, experiment: Experiment):  # [Registered, Submitted, Queued, Running, Completed ]
        # TODO: Test this
        submit_id = experiment.submission_id
        id_str = experiment.id_str
        cmd = 'submit --status ' + submit_id

        trial = 0
        while True:  # status command sometimes returns nothing
            ret = subprocess.check_output(cmd.split())
            ret = ret.split()

            if len(ret) > 5:
                break
            if trial > 2:
                return cls.check_experiment_success(id_str, submit_id)
            trial += 1
        if ret[8] in ['Registered', 'Submitted']:
            return 'Pending'
        if ret[8] == 'Complete':
            return 'Completing'
        return ret[8]

    @classmethod
    def check_experiment_success(cls, id_str: str, submit_id: str) -> str:
        # TODO: Test this
        outputs_dir = cls.outputs_directory(id_str)

        ret = len(glob.glob(str(outputs_dir) + '/*.sl4'))
        if ret == 0:
            status = 'Failed'
        else:
            status = 'Completed'

        # attach to job to terminate the process
        cmd = 'submit --attach ' + submit_id
        os.system(cmd)  # check_output stuck for some reasons..
        # ret = subprocess.check_output(cmd.split())
        return status

    @classmethod
    def delete_experiment(cls, experiment: Experiment):
        # Note: The experiment is passed as an argument to avoid expensive db call
        # TODO: test this
        assert experiment.is_private
        assert isinstance(experiment, Experiment)

        # submit_id = job_info[1]
        # if self.getJobStatus(submit_id) in ['Pending', 'Queued', 'Running']:
        if experiment.status in ['Pending', 'Queued', 'Running', 'Completing']:
            cmd = 'submit --kill ' + experiment.submission_id
            ret = subprocess.check_output(cmd.split())

        # delete experiment working directory
        shutil.rmtree(str(cls.working_directory(experiment.id_str)))

        # delete experiment from db
        cls.db.delete_experiment(experiment.id_str)
