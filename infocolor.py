class Info:
	MOD = '\033[94m[MOD] '
	STATUS = '\033[92m[STATUS] '
	WARNING = '\033[93m[WARNING] '
	ERROR = '\033[91m[ERROR] '
	ENDC = '\033[0m'

	@staticmethod
	def prints(string):
		print(Info.STATUS + string + Info.ENDC)

	@staticmethod
	def printw(string):
		print(Info.WARNING + string + Info.ENDC)

	@staticmethod
	def printe(string):
		print(Info.ERROR + string + Info.ENDC)

	@staticmethod
	def printm(string):
		print(Info.MOD + string + Info.ENDC)

	@staticmethod
	def printi(string):
		print("[INFO] " + string)