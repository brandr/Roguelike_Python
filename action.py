"An action in the game which almost always consumes time."

class Action:

	def __init__(self, actor, method, arg, delay):
		self.actor, self.method, self.arg, self.delay = actor, method, arg, delay

	def execute(self):
		self.actor.execute_action(self.method, self.arg)