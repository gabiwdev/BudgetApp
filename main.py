from itertools import zip_longest
from math import floor
from math import ceil


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True

        else:
            return False

    def get_balance(self):
        balance = 0

        for n in self.ledger:
            balance += n['amount']
        return balance

    def transfer(self, amount, target):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {target.name}')
            target.deposit(amount, f'Transfer from {self.name}')
            return True

        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False

        else:
            return True

    def __str__(self):

        left_padding = (15 - floor(len(self.name) / 2))
        right_padding = (15 - ceil(len(self.name) / 2))

        title = f'{"*" * left_padding}{self.name}{"*" * right_padding}'
        lines = [title]
        for x in self.ledger:
            number = f'{x["amount"]:.2f}'

            lines.append((f'{x["description"].ljust(23, " ")[:23]}{number.rjust(7, " ")}'))
        lines.append(f'Total: {self.get_balance()}')
        return '\n'.join(lines)


def writehr(m, y='', z='', p=''):
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
    x = 100
    totalSpent = 0
    eachSpent = []
    perSpent = []
    for i in categories:
        spent = 0

        ## Calcula o total gasto e adiciona o valor x gasto pela categoria a uma lista
        for s in i.ledger:
            if s['amount'] < 0:
                totalSpent += -s['amount']
                spent += -s['amount']
            else:
                totalSpent += 0
        eachSpent.append(spent)

        ## Divide o valor da lista por 100 e ve quantos % ele gastou

    for g in eachSpent:
        result = g / totalSpent * 100

        perSpent.append(floor(result / 10) * 10)
    lines = []
    lines.append('Percentage spent by category')

    while x >= 0:
        string = f'{str(x).rjust(3, " ")}|'
        for y in perSpent:
            string = string + f' {"o" if y >= x else " "} '
        string = string + ' '
        lines.append(string)
        x -= 10

    lines.append('-'.rjust(5, " ") + f'{"---" * len(perSpent)}')
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
##print(food)
##print(clothes)
print(create_spend_chart([food, clothes, groceries]))