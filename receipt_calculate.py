print('--------------------------------------------------------------')
print('|            На какую сумму нужно продать товара,            |')
print('|              чтобы получить желаемую прибыль               |')
print('|                  при определенной марже                    | ')
print('--------------------------------------------------------------\n')


def receipt():
    income = input('\nВведите необходимый доход: ')
    percent = input('Введите % маржи: ')

    try:
        income = prep_value(income)
        percent = prep_value(percent)
        print(f'Необходимая выручка: {receipt_calculate(income, percent)}')
    except:
        print('Введены неправильные данные...')


def receipt_calculate(income, percent):
    return f'{income / (percent / 100):.2f}'


def prep_value(value):
    value = value.replace(',', '.')
    return float(value)


if __name__ == '__main__':
    while True:
        receipt()
        print('--------------------------')
        print('Продолжить нажмите <Enter>')
        ask = input('Для выхода введите <q>: ')
        if ask == 'q':
            break
