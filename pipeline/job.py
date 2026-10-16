# -- coding: utf-8 --
# pipeline/job.py - Job dataclass cho pipeline
import json, time, os, uuid

VALID_STATUS = ['pending', 'running', 'done', 'failed', 'cancelled']

JOB_TRANSITIONS = {
	'pending': {'running', 'cancelled'},
	'running': {'done', 'failed', 'cancelled'},
	'done': set(),
	'failed': {'pending'},
	'cancelled': set(),
}

PUB_STATUS = ['rendered', 'approved', 'rejected', 'publishing', 'published', 'publish_failed']
PUB_TRANSITIONS = {
	'rendered': {'approved', 'rejected'},
	'approved': {'publishing', 'rejected'},
	'publishing': {'published', 'publish_failed'},
	'publish_failed': {'approved', 'rejected'},
	'published': set(),
	'rejected': set(),
}


def valid_transition(table, cur, nxt):
	return nxt in table.get(cur, set())


def make_job_id():
	return 'job_' + time.strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:8]


class Job:
	def __init__(self, channel_id, topic=None, kind=None,
		length_override=None, voice_override=None, voice_preset=None, music_mood=None,
		count=1, require_approval=True, run_at=None, repeat=None,
		priority=5, created_by='agent', job_id=None, modules=None):
		self.job_id = job_id or make_job_id()
		self.channel_id = channel_id
		self.topic = topic
		self.kind = kind
		self.length_override = length_override
		self.voice_override = voice_override
		self.voice_preset = voice_preset
		self.music_mood = music_mood
		self.count = int(count) if count else 1
		self.require_approval = bool(require_approval)
		self.run_at = run_at
		self.repeat = repeat
		self.priority = int(priority) if priority else 5
		self.created_by = created_by
		self.modules = modules or {}
		self.status = 'pending'
		self.error = None

	def to_dict(self):
		return {
			'job_id': self.job_id,
			'channel_id': self.channel_id,
			'topic': self.topic,
			'kind': self.kind,
			'length_override': self.length_override,
			'voice_override': self.voice_override,
			'voice_preset': self.voice_preset,
			'music_mood': self.music_mood,
			'count': self.count,
			'require_approval': self.require_approval,
			'run_at': self.run_at,
			'repeat': self.repeat,
			'priority': self.priority,
			'created_by': self.created_by,
			'modules': self.modules,
			'status': self.status,
		}

	def to_json(self):
		return json.dumps(self.to_dict(), ensure_ascii=False)

	@classmethod
	def from_dict(cls, d):
		return cls(
			channel_id=d.get('channel_id'),
			topic=d.get('topic'),
			kind=d.get('kind'),
			length_override=d.get('length_override'),
			voice_override=d.get('voice_override'),
			voice_preset=d.get('voice_preset'),
			music_mood=d.get('music_mood'),
			count=d.get('count', 1),
			require_approval=d.get('require_approval', True),
			run_at=d.get('run_at'),
			repeat=d.get('repeat'),
			priority=d.get('priority', 5),
			created_by=d.get('created_by', 'agent'),
			job_id=d.get('job_id'),
			modules=d.get('modules') or {},
		)

	@classmethod
	def from_json(cls, s):
		return cls.from_dict(json.loads(s))

	def validate(self):
		errs = []
		if not self.channel_id:
			errs.append('channel_id rong')
		if self.count < 1 or self.count > 50:
			errs.append('count phai 1-50')
		return errs

	def repr_mark(self):
		return 'Job(' + self.job_id + ',' + self.channel_id + ',' + str(self.kind) + ')'
