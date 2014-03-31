"An action in the game which almost always consumes time."

class Action:

	def __init__(self, being, method, arg, delay):
		self.being, self.method, self.arg, self.delay = being, method, arg, delay

	def execute(self):
		self.being.execute_action(self.method, self.arg)