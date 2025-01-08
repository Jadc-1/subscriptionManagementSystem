import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

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
            results = session.exec(statement).all() ##o exec é utilizado para executar querys, e estamos falando para executar statement, que vai selecionar a tabela inteira
            return results
        
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()
        
        
    def _has_pay(self, results):  ##colocamos _ quando a função não será acessado por fora
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa == subscription.empresa) ##To verificando se a empresa que eu quero pagar assinatura, ja está paga ou não
            results = session.exec(statement).all()           
            
            if self._has_pay(results): ##Estamos utilizando a função has pay, para verificar se ja esta pago
                question = input("Essa conta já foi paga esse mês,deseja pagar novamente? Y ou N: ")

                if not question.upper() == "Y":
                    return ##Mesma coisa que return None, então paramos a função aqui
            
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()

    def total_value(self):
        with Session(self.engine) as session: 
        # Cria uma consulta (statement) para selecionar todos os registros da tabela Subscription
            statement = select(Subscription) 
        # Executa a consulta e retorna todos os resultados como uma lista
            results = session.exec(statement).all() 

        total = 0
        # Itera sobre cada registro (result) retornado pela consulta
        for result in results:
            total += result.valor  # Soma o valor de cada assinatura ao total

        return float(total)

    def _get_last_12_months(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month,year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]
    
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)

                value_for_months.append(value)
        return value_for_months

    def gen_chart(self):
        last_12_months = self._get_last_12_months()
        value_for_months = self._get_values_for_months(last_12_months)

        last_12_months2 = []
        for i in last_12_months:
            last_12_months2.append(i[0]) 

        import matplotlib.pyplot as plt ##Cria um gráfico, porém precisa de uma interface, por isso instalamos esse biblioteca matplotlib e pyqt5
        x_sorted, y_sorted = zip(*sorted(last_12_months2, value_for_months))

        plt.plot(x_sorted, y_sorted)
        plt.show()

sm = SubscriptionManagement(engine)
#subscription = Subscription(empresa='vivo', site='vivo.com.br', data_assinatura=date.today(), valor= '150')

