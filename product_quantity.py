print('--------------------------------------------------------------')
print('|    Расчет количества проданного товара, для получения      |')
print('|                  необходимой прибыли                       |')
print('--------------------------------------------------------------\n')


def main():
    cost_price = input('\nВведите себестоимость: ')
    price = input('Введите отпускную цену: ')
    income = input('Введите необходимую прибыль: ')
    try:
        income = prep_value(income)
        cost_price = prep_value(cost_price)
        price = prep_value(price)
        print(
            f'Количество товара: {quantity_calculate(income, cost_price, price):.1f}')
    except:
        print('Введены неправильные данные...')


def prep_value(value):
    value = value.replace(',', '.')
    return float(value)


def quantity_calculate(income, cost_price, price):
    return income / (price - cost_price)


if __name__ == '__main__':
    while True:
        main()
        print('--------------------------')
        print('Продолжить нажмите <Enter>')
        ask = input('Для выхода введите <q>: ')
        if ask == 'q':
            break
