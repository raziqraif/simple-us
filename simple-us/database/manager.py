from datetime import datetime
from getpass import getuser
import os
from pathlib import Path
import sys
from typing import List, Optional
from typing import Union

import sqlite3

from database.dbutils import AUTHOR_DBCOL
from database.dbutils import AUTHOR_DBKEY
from database.dbutils import DESCRIPTION_DBCOL
from database.dbutils import DESCRIPTION_DBKEY
from database.dbutils import ID_DBCOL
from database.dbutils import ID_DBKEY
from database.dbutils import MODEL_DBCOL            # CustomCornsoy or CustomAllcrops
from database.dbutils import MODEL_DBKEY
from database.dbutils import NAME_DBCOL
from database.dbutils import NAME_DBKEY
from database.dbutils import PUBLISHED_DBCOL        # 1 if shared experiment 0 if private experiment
from database.dbutils import PUBLISHED_DBKEY
from database.dbutils import STATUS_DBCOL           # Completed / Pending / Failed
from database.dbutils import STATUS_DBKEY
from database.dbutils import SUBMISSION_ID_DBCOL
from database.dbutils import SUBMISSION_ID_DBKEY
from database.dbutils import SUBMISSION_TIME_DB_COL
from database.dbutils import SUBMISSION_TIME_DBKEY

from model import Experiment
from utils import SIMPLEUtil


class DBManager:
    """ Manages communication with the database file

    A table row is represented represented as a list or an Experiment object in this class.
    """
    from model import Experiment

    PRIVATE_DB_FILE = str(SIMPLEUtil.PRIVATE_JOBS_DIR / "job.db")
    SHARED_DB_FILE = str(SIMPLEUtil.SHARED_JOBS_DIR / "job.db")

    def __init__(self):

        if not Path(self.PRIVATE_DB_FILE).exists():
            self.initialize_db(is_private=True)
        # Note: Shared DB are not automatically created

        self._validate_private_db()

    def initialize_db(self, is_private):
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
        if not is_private:
            try:
                SIMPLEUtil.SHARED_JOBS_DIR.mkdir(parents=True, exist_ok=True)
                os.chmod(str(SIMPLEUtil.SHARED_JOBS_DIR), 0o775)
            except:
                raise
        else:
            SIMPLEUtil.PRIVATE_JOBS_DIR.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.PRIVATE_DB_FILE if is_private else self.SHARED_DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()

        # give simpleggroup read, write permission
        if not is_private:
            os.chmod(self.SHARED_DB_FILE, 0o664)

    def _validate_private_db(self):
        # check if a user uses old db
        conn = sqlite3.connect(self.PRIVATE_DB_FILE)
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

    @classmethod
    def last_modified(cls) -> datetime:
        # Return the latest time a db (shared/private) was modified
        private = os.path.getmtime(cls.PRIVATE_DB_FILE)
        private = datetime.fromtimestamp(private)
        if Path(cls.SHARED_DB_FILE).exists():
            shared = os.path.getmtime(cls.SHARED_DB_FILE)
            shared = datetime.fromtimestamp(shared)
            return private if private > shared else private
        return private

    def new_experiment(self, name: Optional[str] = None, description: Optional[str] = None,
                       model: Optional[str] = None) -> Experiment:
        now = datetime.now()
        submit_time = now.strftime('%m/%d/%Y %H:%M:%S')

        conn = sqlite3.connect(self.PRIVATE_DB_FILE)
        sql = 'insert into SIMPLEJobs(submitTime,jobstatus) values (?,?);'
        conn.execute(sql, (submit_time, 'Pending'))
        conn.commit()

        sql = 'select jobid from SIMPLEJobs order by jobid desc limit 1;'
        cur = conn.execute(sql)
        jobid = cur.fetchone()[0]

        conn.commit()
        conn.close()
        experiment = Experiment(id=jobid, name=name, description=description, model=model, author=getuser())
        self.update_experiment(experiment)
        return experiment

    def _insert_experiment(self, experiment: Experiment) -> int:
        """ Should only be used to insert seed data """""

        now = datetime.now()
        submit_time = now.strftime('%m/%d/%Y %H:%M:%S')

        db_file = self.PRIVATE_DB_FILE if experiment.is_private else self.SHARED_DB_FILE
        conn = sqlite3.connect(db_file)
        sql = 'insert into SIMPLEJobs(submitId, submitTime, author, jobstatus, jobname, modeltype, ' \
              'published, description) values (?,?,?,?,?,?,?,?);'
        conn.execute(sql, (experiment.id_str, submit_time, experiment.author, experiment.status, experiment.name,
                           experiment.model, experiment.published, experiment.description))
        conn.commit()

        sql = 'select jobid from SIMPLEJobs order by jobid desc limit 1;'
        cur = conn.execute(sql)
        jobid = cur.fetchone()[0]

        conn.commit()
        conn.close()

        return jobid

    def get_experiments(self) -> List[Experiment]:
        conn = sqlite3.connect(self.PRIVATE_DB_FILE)
        sql = 'select * from SIMPLEJobs order by jobid;'
        cur = conn.execute(sql)
        jobs_as_lists = cur.fetchall()

        if Path(self.SHARED_DB_FILE).exists():
            conn = sqlite3.connect(self.PRIVATE_DB_FILE)
            sql = 'select * from SIMPLEJobs order by jobid;'
            cur = conn.execute(sql)
            jobs_as_lists += cur.fetchall()

        experiments = []
        for job in jobs_as_lists:
            exp = self._to_experiment(job)
            experiments.append(exp)
        return experiments

    def get_experiment(self, jobid: int, is_private: bool) -> Optional[Experiment]:
        db_file = self.PRIVATE_DB_FILE if is_private else self.SHARED_DB_FILE
        conn = sqlite3.connect(db_file)
        sql = 'select * from SIMPLEJobs where jobid = ?;'
        cur = conn.execute(sql, (str(jobid),))
        job_as_list = cur.fetchone()

        if job_as_list is not None:
            exp = self._to_experiment(job_as_list)
            return exp
        else:
            return None

    def update_experiment(self, experiment: Experiment) -> bool:
        params = {}
        if experiment.submission_id is not None:
            params[SUBMISSION_ID_DBKEY] = experiment.submission_id
        if experiment.submission_time is not None:
            params[SUBMISSION_TIME_DBKEY] = experiment.submission_time
        if experiment.author is not None:
            params[AUTHOR_DBKEY] = experiment.author
        if experiment.status is not None:
            params[STATUS_DBKEY] = experiment.status
        if experiment.name is not None:
            params[NAME_DBKEY] = experiment.name
        if experiment.model is not None:
            params[MODEL_DBKEY] = experiment.model
        if experiment.published is not None:
            params[PUBLISHED_DBKEY] = experiment.published
        if experiment.description is not None:
            params[DESCRIPTION_DBKEY] = experiment.description

        if len(params.keys()) == 0:
            return False

        sql = 'update SIMPLEJobs set '
        for key in params.keys():
            sql += key + ' = "' + str(params[key]) + '",'
        sql = sql[:-1] + ' where jobid = "' + str(experiment.id) + '";'

        print("sql", sql)
        db_file = self.PRIVATE_DB_FILE if experiment.is_private else self.SHARED_DB_FILE
        conn = sqlite3.connect(db_file)
        conn.execute(sql)
        conn.commit()
        conn.close()

        return True

    def delete_experiment(self, experiment: Experiment):
        assert experiment.is_private  # Can only delete private experiment

        conn = sqlite3.connect(self.PRIVATE_DB_FILE)
        sql = 'delete from SIMPLEJobs where jobid = ?'
        conn.execute(sql, (str(experiment.id),))
        conn.commit()
        conn.close()
        return True

    def _to_experiment(self, job: List[Union[str, int, None]]) -> Experiment:
        exp = Experiment(
            id=job[ID_DBCOL],
            name=job[NAME_DBCOL],
            status=job[STATUS_DBCOL],
            description=job[DESCRIPTION_DBCOL],
            model=job[MODEL_DBCOL],
            author=job[AUTHOR_DBCOL],
            submission_id=job[SUBMISSION_ID_DBCOL],
            submission_time=job[SUBMISSION_TIME_DB_COL],
            published=job[PUBLISHED_DBCOL]
        )
        return exp


if __name__ == "__main__":
    # from pathlib import Path
    # path = Path(".").absolute()
    db = DBManager()
    # id_ = db.create_new_job()
    # db.update_job_status(1, "Completed", 2)
    import getpass
    user = "raziqraif"
    exp_ = Experiment(1, "Experiment", model="CustomAllcrop",
                      status="Completed", description="Allcrop test data.", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(2, "UM-E4", status="Completed", description="SIMPLE-G Workshop", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(3, "AC-E1", status="Completed", description="SIMPLE-G Workshop", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(4, "AC-E2", status="Completed", description="SIMPLE-G Workshop", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(5, "C5-E2", status="Completed", description="SIMPLE-G Workshop", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(6, status="Pending", description="SIMPLE-G US", author=user, submission_id="-",
                      submission_time=datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    db.update_experiment(exp_)
    exp_ = Experiment(7, name="UM-E6", status="Pending", author="muhdr", submission_id="-",
                      description="SIMPLE-G US Experiment")
    db.update_experiment(exp_)
    exp_ = Experiment(10,
                      model="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      name="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      status="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      author="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      description="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      submission_time="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      submission_id="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                      )
    db.update_experiment(exp_)
