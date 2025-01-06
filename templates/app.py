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
            [5] -> Sair
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
                #TODO: Chamar o método pay na interface
                case _:
                    break
    def add_subscription(self):
        empresa = input("Empresa: ")
        site = input("Site: ")
        data_assinatura = datetime.strptime(input("Data de Assinatura: "), "%d/%m/%Y")
        valor = Decimal(input("Valor: "))
        subscription = Subscription(empresa = empresa, site = site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)

    def delete_subscription(self):
        subscription = self.subscription_service.list_all()
        print("Escolha qual assinatura você deseja excluir: ")
        ##TODO: Quando excluir a assinatura, excluir todos os pagamentos dela
        for i in subscription:
            print("[{i.id}] -> {i.empresa}")
        excluse = int(input("Escolha a assinatura a ser cancelada: "))

        self.subscription_service.delete(excluse)
        print(f"Assinatura da excluída com sucesso")

    def total_value(self):
        print(f"O valor total mensal é: {self.subscription_service.total_value()}")

if __name__ == "__main__":
    UI().start()

