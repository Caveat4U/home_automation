import abc

class Input(object):
    def __enter__(self):
    	pass

    def __init__(self):
        self.triggered = False
        print "Hello"

    def is_triggered(self):
    	'''
    	If the item triggered something, return True and reset the pushed indicator.
    	'''
    	if self.triggered:
    		self.triggered = False
    		return True
    	else:
    		return False

    def __exit__(self):
    	pass


class HueButton(Input): pass
class WemoButton(Input): pass
class iClickerRemotes(Input):
	def __enter__(self):
		pass

	def __init__(self):
		pass

	def __exit__(self):
		pass