import datetime
import os
from pathlib import Path
import sys
from typing import List, Optional
from typing import Union

import sqlite3

from database.dbutils import AUTHOR
from database.dbutils import DESCRIPTION
from database.dbutils import JOB_ID
from database.dbutils import JOB_NAME
from database.dbutils import JOB_STATUS
from database.dbutils import MODEL_TYPE
from database.dbutils import PUBLISHED
from database.dbutils import SUBMIT_ID
from database.dbutils import SUBMIT_TIME
from model import Experiment
from utils import SIMPLEUtil


class DBManager:
    """ Manages communication with the database file

    A table row is represented represented as a list or an Experiment object in this class.
    The Experiment object representation helps with code completion, etc but for backward
    compatibility, the list representation is kept.
    """
    from model import Experiment

    def __init__(self, private_experiments=True):
        if private_experiments:
            directory_path = SIMPLEUtil.PRIVATE_JOBS_DIR
        else:
            directory_path = SIMPLEUtil.SHARED_JOBS_DIR

        self.DB_FILE = str(directory_path.joinpath("job.db"))
        # check if db file exists
        if not os.path.isfile(self.DB_FILE):
            print('not found')
            self.init_table(directory_path)

        # check if a user uses old db
        conn = sqlite3.connect(self.DB_FILE)
        sql = 'PRAGMA table_info(SIMPLEJobs);'
        cur = conn.execute(sql)
        ret = cur.fetchall()
        for col in ret:
            if col[1] == 'jobname':
                return

        # no jobname
        sql = '''alter table SIMPLEJobs add column jobname TEXT'''
        cur = conn.execute(sql)
        conn.close()

    def init_table(self, directory_path: Path):
        sql = '''
        CREATE TABLE SIMPLEJobs (
            jobid INTEGER PRIMARY KEY AUTOINCREMENT,
            submitId TEXT,
            submitTime TEXT,
            author TEXT,
            jobstatus TEXT,
            jobname TEXT,
            modeltype TEXT,
            published INTEGER,
            description TEXT
        );
        '''

        # create job folder first
        # For shared db, other admins should be able to update database
        # so read,write permissions are given to the simpleggroup
        if directory_path == SIMPLEUtil.SHARED_JOBS_DIR:
            try:
                SIMPLEUtil.mkdir(directory_path)
                os.chmod(str(directory_path), 0o775)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        else:
            SIMPLEUtil.mkdir(directory_path)

        conn = sqlite3.connect(self.DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()

        # give simpleggroup read, write permission
        if directory_path == SIMPLEUtil.SHARED_JOBS_DIR:
            os.chmod(self.DB_FILE, 0o664)

    def create_new_job(self):
        now = datetime.datetime.now()
        submit_time = now.strftime('%m/%d/%Y %H:%M:%S')

        conn = sqlite3.connect(self.DB_FILE)
        sql = 'insert into SIMPLEJobs(submitTime,jobstatus) values (?,?);'
        conn.execute(sql, (submit_time, 'None'))
        conn.commit()

        sql = 'select jobid from SIMPLEJobs order by jobid desc limit 1;'
        cur = conn.execute(sql)
        jobid = cur.fetchone()[0]

        conn.commit()
        conn.close()

        return str(jobid)

    def update_job_info(self, jobid, params):
        sql = 'update SIMPLEJobs set '
        for key in params:
            sql += key + ' = "' + str(params[key]) + '",'
            # print sql,'\n'

        sql = sql[:-1] + ' where jobid = "' + str(jobid) + '";'
        print(sql, '\n')

        conn = sqlite3.connect(self.DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()

        return True

    def update_job_status(self, jobid, status, submit_id):
        sql = 'update SIMPLEJobs set jobstatus = ? where jobid = ?;'

        conn = sqlite3.connect(self.DB_FILE)
        conn.execute(sql, (status, str(jobid)))
        conn.commit()
        conn.close()
        param = {'submitId': submit_id}

        return True

    def delete_job(self, jobid):
        conn = sqlite3.connect(self.DB_FILE)
        sql = 'delete from SIMPLEJobs where jobid = ?'
        conn.execute(sql, (str(jobid),))
        conn.commit()
        conn.close()
        return True

    def get_job_list(self):
        conn = sqlite3.connect(self.DB_FILE)
        sql = 'select * from SIMPLEJobs order by jobid desc;'
        cur = conn.execute(sql)
        return cur.fetchall()

    def get_experiments(self) -> List[Experiment]:
        jobs_as_lists = self.get_job_list()
        experiments = []
        for job in jobs_as_lists:
            exp = self.to_experiment(job)
            experiments.append(exp)
        return experiments

    def get_job_info(self, jobid):
        conn = sqlite3.connect(self.DB_FILE)
        sql = 'select * from SIMPLEJobs where jobid = ?;'
        # print sql
        cur = conn.execute(sql, (str(jobid),))
        return cur.fetchone()

    def get_experiment(self, jobid) -> Optional[Experiment]:
        # job_as_list = self.get_job_info(jobid)
        # if job_as_list is None:
        #     return None
        # self.to_experiment(job_as_list)
        for exp in self.get_experiments():
            if exp.id == jobid:
                return exp
        return None

    def to_list(self, experiment: Experiment) -> List[Union[str, int, None]]:
        experiment_as_list = [
            experiment.id,
            str(experiment.submission_id),
            experiment.submission_time,
            experiment.author,
            experiment.status,
            experiment.name,
            experiment.model,
            experiment.published,
            experiment.description
        ]
        return experiment_as_list

    def to_experiment(self, job: List[Union[str, int, None]]) -> Experiment:
        exp = Experiment(
            id=job[JOB_ID],
            name=job[JOB_NAME],
            status=job[JOB_STATUS],
            description=job[DESCRIPTION],
            model=job[MODEL_TYPE],
            author=job[AUTHOR],
            submission_id=job[SUBMIT_ID],
            submission_time=job[SUBMIT_TIME],
            published=job[PUBLISHED]
        )
        return exp


if __name__ == "__main__":
    # from pathlib import Path
    # path = Path(".").absolute()
    # print("path:", path.parent.parent)
    db = DBManager()
    print(db.get_experiments())
