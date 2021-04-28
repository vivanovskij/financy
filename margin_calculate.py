print('Наценка = Отпускная цена – Себестоимость/ Себестоимость х 100%')
print('Маржа = Отпускная цена – Себестоимость/ Отпускная цена х 100%')
print('--------------------------------------------------------------')
print('|                    Расчет маржи                            |')
print('--------------------------------------------------------------\n')


def main():
    cost_price = input('\nВведите себестоимость: ')
    price = input('Введите отпускную цену: ')

    try:
        cost_price = prep_value(cost_price)
        price = prep_value(price)
        print(f'Маржа равна: {margin_calculate(cost_price, price)}')
    except:
        print('Введены неправильные данные...')


def margin_calculate(cost_price, price):
    return f'{(price - cost_price) / price * 100:.1f}%'


def prep_value(value):
    value = value.replace(',', '.')
    return float(value)


if __name__ == '__main__':
    while True:
        main()
        print('--------------------------')
        print('Продолжить нажмите <Enter>')
        ask = input('Для выхода введите <q>: ')
        if ask == 'q':
            break
