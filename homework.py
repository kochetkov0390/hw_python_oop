import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        form_date = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, form_date).date()


class Calculator:

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = sum([record.amount for record in self.records
                           if record.date == self.today])
        return today_stats

    def get_week_stats(self):
        number_days = self.today - dt.timedelta(days=7)
        week_stats = sum([record.amount for record in self.records
                          if number_days <= record.date <= self.today])
        return week_stats

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(7)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = (self.limit - self.get_today_stats())
        if calories_remained <= 0:
            return 'Хватит есть!'
        else:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')


class CashCalculator(Calculator):

    RUB_RATE = 1.00
    USD_RATE = 60.00
    EURO_RATE = 70.00

    def get_today_cash_remained(self, currency):
        CURRENCIES = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE)
        }
        cash_remained = (self.limit - self.get_today_stats())
        currency_name, rate = CURRENCIES[currency]
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in CURRENCIES:
            return 'Валюта не поддерживается'
        cash_remained = cash_remained / rate
        if cash_remained < 0:
            cash_remained = abs(cash_remained)
            return ('Денег нет, держись: твой долг -'
                    f'{cash_remained: .2f} {currency_name}')
        return f'На сегодня осталось {cash_remained:.2f} {currency_name}'


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
    """огромная просьба подойти к ревью лояльнее)"""
    """не смогу физически внести правки до дедлайна"""
