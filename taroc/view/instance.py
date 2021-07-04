from taroc.ps import Column

HOST = Column('HOST', 25, lambda i: i[0])
JOB_ID = Column('JOB ID', 30, lambda i: i[1]['job_id'])
INSTANCE_ID = Column('INSTANCE ID', 23, lambda i: i[1]['instance_id'])


DEFAULT_COLUMNS = [HOST, JOB_ID, INSTANCE_ID]
