import __init__
from models.database import engine
from models.model import Subscription

class SubscriptionManagement:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):

sm = SubscriptionManagement(engine)


