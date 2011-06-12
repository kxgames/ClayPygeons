class Subscription:
    def __init__(self, type):
        self.type = type

class Cancellation:
    def __init__(self, type):
        self.type = type

class Delivery:
    def __init__(self, message, address):
        self.address = address
        self.message = message
