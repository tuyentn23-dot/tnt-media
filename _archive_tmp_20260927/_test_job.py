import sys
sys.path.insert(0, '.')
from pipeline import job

print('make_job_id:', job.make_job_id())
j = job.Job(channel_id='x')
print('job_id:', j.job_id)
print('validate:', j.validate())
print('pending->running:', job.valid_transition(job.JOB_TRANSITIONS, 'pending', 'running'))
print('done->running:', job.valid_transition(job.JOB_TRANSITIONS, 'done', 'running'))
print('rendered->approved:', job.valid_transition(job.PUB_TRANSITIONS, 'rendered', 'approved'))
print('rendered->published:', job.valid_transition(job.PUB_TRANSITIONS, 'rendered', 'published'))
