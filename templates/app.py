import __init__
from views.view import SubscriptionManagement
from models.database import engine
from datetime import datetime
from decimal import Decimal
from models.model import Subscription


class UI:
    def __init__(self):
        self.subscription_service = SubscriptionManagement(engine)

    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Pagamento assinatura
            [6] -> Listar assinaturas
            [7] -> Sair
            ''')

            choice = int(input('Escolha uma opção: '))

            match choice:
                case 1:
                    self.add_subscription()
                case 2:
                    self.delete_subscription()
                case 3:
                    self.total_value()
                case 4:
                    self.subscription_service.gen_chart()
                case 5:
                    self.pay_subscription()
                case 6:
                    self.list_subscriptions()
                case _:
                    break
    def add_subscription(self):
        empresa = input("Empresa: ")
        site = input("Site(Opcional): ")
        data_assinatura = datetime.strptime(input("Data de Assinatura: "), "%d/%m/%Y")
        valor = Decimal(input("Valor: "))
        subscription = Subscription(empresa = empresa, site = site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)

    def delete_subscription(self):
        subscription = self.subscription_service.list_all()
        print("Escolha qual assinatura você deseja excluir: ")
        for i in subscription:
            print(f"[{i.id}] -> {i.empresa}")
        excluse = int(input("Escolha a assinatura a ser cancelada: "))

        self.subscription_service.delete(excluse)
        print(f"Assinatura excluída com sucesso")

    def total_value(self):
        print(f"O valor total mensal é: {self.subscription_service.total_value()}")

    def pay_subscription(self):
        print(f"Qual assinatura receberá o pagamento? ")
        empresa = input("Empresa: ")
        subscription = self.subscription_service.list_all()
        for i in subscription:
            if empresa == i.empresa:
                payment = Subscription(empresa = empresa, id = i.id)
                self.subscription_service.pay(payment)
                print(f"Pagamento {empresa} realizada com sucesso!")
    
    def list_subscriptions(self):
        subscription = self.subscription_service.list_all()
        print("Lista de todas as suas assinaturas: \n")
        for i in subscription:
            print(f"Empresa: {i.empresa}")
            print(f"Valor: {i.valor:.2f}\n")
        input(f"\nClique qualquer tecla para continuar..")

            
        
if __name__ == "__main__":
    UI().start()

