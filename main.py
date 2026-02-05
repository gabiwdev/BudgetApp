from itertools import zip_longest
from math import floor
from math import ceil

# Classe de categoria de gastos
class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []


    def deposit(self, amount, description=''):
        """Método para depositar uma quantia na conta atual, com uma descrição opcional"""
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        """Método para sacar uma quantia da conta se a quantia existir dentro da categoria atual"""
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True

        else:
            return False

    def get_balance(self):
        """Retorna a quantia de dinheiro atual da conta"""
        balance = 0

        for n in self.ledger:
            balance += n['amount']
        return balance

    def transfer(self, amount, target):
        """Função de transfêrencia para outra categoria, gera o withdraw e deposit nas respectivas contas"""
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {target.name}')
            target.deposit(amount, f'Transfer from {self.name}')
            return True

        else:
            return False

    def check_funds(self, amount):
        """Retorna true caso possuir a quantia requisitada e false se não"""
        if amount > self.get_balance():
            return False

        else:
            return True

    def __str__(self):
        """Cria a representação em String da categoria"""


        left_padding = (15 - floor(len(self.name) / 2))
        right_padding = (15 - ceil(len(self.name) / 2))

        # Cria um titulo com o nome da categoria centralizada
        title = f'{"*" * left_padding}{self.name}{"*" * right_padding}'
        lines = [title]

        # Resume os gastos
        for x in self.ledger:
            number = f'{x["amount"]:.2f}'

            lines.append((f'{x["description"].ljust(23, " ")[:23]}{number.rjust(7, " ")}'))

        # Mostra o total
        lines.append(f'Total: {self.get_balance()}')
        return '\n'.join(lines)


def writehr(m, y='', z='', p=''):
    """Função feita pra escrever até quatro palavras horizontalmente, requisitada no desafio"""

    cols = [
        m.name,
        y.name if isinstance(y, Category) else '',
        z.name if isinstance(z, Category) else '',
        p.name if isinstance(p, Category) else ''
    ]

    lines = []

    for row in zip_longest(*cols, fillvalue=''):
        line = ''.join(f' {ch} ' if ch else '   ' for ch in row)
        lines.append(line.rstrip() + '  ')

    return '    ' + '\n    '.join(lines)


def create_spend_chart(categories):
    """Função para criar um gráfico mostrando a porcentagem de gasto de cada categoria"""

    x = 100
    totalSpent = 0
    eachSpent = []
    perSpent = []
    for i in categories:
        spent = 0

        # Calcula o total gasto e adiciona o valor x gasto pela categoria a uma lista
        for s in i.ledger:
            if s['amount'] < 0:
                totalSpent += -s['amount']
                spent += -s['amount']
            else:
                totalSpent += 0
        eachSpent.append(spent)

    # Transforma a quantia gasta de cada categoria em porcentagem
    for g in eachSpent:
        result = g / totalSpent * 100

        perSpent.append(floor(result / 10) * 10)
    lines = []
    lines.append('Percentage spent by category')

    # Esse loop cria as colunas do gráfico
    while x >= 0:
        string = f'{str(x).rjust(3, " ")}|'
        for y in perSpent:
            string = string + f' {"o" if y >= x else " "} '
        string = string + ' '
        lines.append(string)
        x -= 10

    # Adiciona na lista "linhas" um separador
    lines.append('-'.rjust(5, " ") + f'{"---" * len(perSpent)}')

    # Adiciona na lista linhas as palavras de cada categoria escrita horizontalmente
    lines.append(writehr(*categories))
    return '\n'.join(lines)


clothes = Category('Clothes')
food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
food.transfer(100, clothes)
clothes.withdraw(100)
groceries = Category('Groceries')
groceries.deposit(1000, 'deposit')
groceries.withdraw(900, 'groceries')

print(writehr(*[food, clothes, groceries]))

print(create_spend_chart([food, clothes, groceries]))