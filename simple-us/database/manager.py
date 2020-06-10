import datetime
import os
from pathlib import Path
import sys

import sqlite3

import database.utils as dbutils


class DBManager:
    def __init__(self, directory_path: Path):
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
        sql = 'alter table SIMPLEJobs add column jobname TEXT'
        cur = conn.execute(sql)
        conn.close()

    def init_table(self, directory_path: str):
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
        if directory_path == dbutils.SHARED_JOBS_DIR:
            try:
                dbutils.mkdir_p(directory_path)
                os.chmod(directory_path, 0o775)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        else:
            dbutils.mkdir_p(directory_path)

        conn = sqlite3.connect(self.DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()

        # give simpleggroup read, write permission
        if directory_path == dbutils.SHARED_JOBS_DIR:
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

    def get_job_info(self, jobid):
        conn = sqlite3.connect(self.DB_FILE)
        sql = 'select * from SIMPLEJobs where jobid = ?;'
        # print sql
        cur = conn.execute(sql, (str(jobid),))
        return cur.fetchone()


if __name__ == "__main__":
    # from pathlib import Path
    # path = Path(".").absolute()
    # print("path:", path.parent.parent)
    db = DBManager(dbutils.PRIVATE_JOBS_DIR)
    for job in db.get_job_list():
        print(job)
