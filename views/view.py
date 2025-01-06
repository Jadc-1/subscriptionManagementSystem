import __init__
from models.database import engine
from models.model import Subscription
from sqlmodel import Session, select
from datetime import date

class SubscriptionManagement():
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription): ## criamos a instância subscription que importa todos os dados do Subscription que criamos
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription
        
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription) ##Busque os dados da tabela subscription (isso é uma query)
            result = session.exec(statement) ##o exec é utilizado para executar querys, e estamos falando para executar statement, que vai selecionar a tabela inteira
            return result

sm = SubscriptionManagement(engine)
subscription = Subscription(empresa='netflix', site='netflix.com.br', data_assinatura=date.today(), valor= '150')
sm.create(subscription)


