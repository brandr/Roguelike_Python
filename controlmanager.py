""" Organizes various control contexts based on the situation.
"""

from maingamecontrols import * 

class ControlManager:
	""" ControlManager( ... ) -> ControlManager

	Can hold one Controls object at a time.

	Attributes:

	Controls: current control scheme for keyboard input.

	"""

	def __init__(self, controls):
		self.current_controls = controls

	def process_event(self, event):
		self.current_controls.process_event(event)