class Subscription(object):
    def __init__(self, type):
        self.type = type

class Cancellation(object):
    def __init__(self, type):
        self.type = type

class Delivery(object):
    def __init__(self, message, address, sender):
        self.message = message
        self.address = address
        self.sender = sender
