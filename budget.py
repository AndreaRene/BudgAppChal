from re import split


class Category:
    def __init__(self, name, ledger=None):
        self.name = name
        self.ledger = ledger or []
      
    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
      
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -abs(amount), 'description': description})
            return True
        return False
      
    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)
      
    def transfer(self, amount, newCat):
        if self.withdraw(amount, f'Transfer to {newCat.name}'):
           newCat.deposit(amount, f'Transfer from {self.name}')
           return True
        return False
      
    def check_funds(self, amount):
        return self.get_balance() >= amount
  
    def __repr__(self):
        ledger_array = [self.name.center(30, '*')]
        for entry in self.ledger:
            ledger_array.append(f"{entry['description'][:23]:23}{entry['amount']:>7.2f}")
        ledger_array.append(f"Total: {self.get_balance()}")
        return ('\n').join(ledger_array)

def create_spend_chart(categories):

    category_data = []
    total_expenditures = sum(abs(sum(entry['amount'] for entry in category.ledger if entry['amount'] < 0)) for category in categories)
  
    for category in categories:
        category_expenditures = abs(sum(entry['amount'] for entry in category.ledger if entry['amount'] < 0))
        percentage = (category_expenditures / total_expenditures * 100) // 10 * 10
        category_data.append({'amount' : category_expenditures, 'name': category.name, 'percentage': int(percentage)})

    chart_lines = []
    for i in reversed(range(0, 101, 10)):
        chart_line = (f'{i}| ').rjust(5, ' ')
        for data in category_data:
            chart_line += ('o  ' if data['percentage'] >= i else '   ')
        chart_lines.append(chart_line)
    chart_lines_str = '\n'.join(chart_lines)
    bottom_line = '    ' + '-' * (len(categories) * 3 + 1)

    name_lines = []
    longest_name_length = len(max(category_data, key=lambda x: len(x['name']))['name'])
    for i in range(longest_name_length):
        name_line = []
        for category in category_data:
            padded_name = category['name'].ljust(longest_name_length, ' ')
            name_letters = padded_name[i] + '  '
            name_line.append(name_letters)
        alligned_name_lines = ''.join(name_line).rjust(len(bottom_line))
        name_lines.append(alligned_name_lines)
    
    name_lines_str = '\n'.join(name_lines)
        
    full_chart = f"Percentage spent by category\n{chart_lines_str}\n{bottom_line}\n{name_lines_str}"
  
    return full_chart
  