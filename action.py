"An action in the game which almost always consumes time."

class Action:
	""" Action(Being/Status, Method, ?, int) -> Action

	An action to be stored and processed. With this system, an action can be "planned"
	before it is actually executed, actions can be processed in the correct order,
	and an action can be cancelled if necessary. (most of this work is handled in 
	the TurnCounter class.)
	
	Attributes:
	actor: The Being (or status) that will execute the action.
	method: The meat of the action. This is what the Being will do.
	arg: Some unknown argument to be used when calling the method.
		If more than one item of information is needed, simply pass a tuple of
		args of the form arg = (arg1, arg2, arg3, etc.)
	delay: This is how long the actor must wait after acting before it can act again.
	"""
	def __init__(self, actor, method, arg, delay):
		self.actor, self.method, self.arg, self.delay = actor, method, arg, delay

	def execute(self):
		""" a.execute( ) -> None

		This causes the action's being to execute the action.
		"""
		self.actor.execute_action(self.method, self.arg)
