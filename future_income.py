print('--------------------------------------------------------------')
print('|        Расчет роста капитала в зависимости от %            |')
print('--------------------------------------------------------------\n')


def main():
    capital = input('Введите текущую сумму: ')
    percent = input('Введите кол-во %: ')
    years = input('Введите кол-во лет: ')
    try:
        capital = prep_value(capital)
        percent = prep_value(percent)
        years = prep_value(years)

        result = future_income_calculate(capital, percent, years)
        show_result(result)
    except:
        print('Введены неверные данные...')


def future_income_calculate(capital, percent, years):
    percent = percent / 100
    period = int(years // 1)
    part_of_period = years % 1

    for i in range(1, period + 1):
        capital *= 1 + percent
    capital += capital * part_of_period * percent
    return capital


def prep_value(value):
    value = value.replace(',', '.')
    return float(value)


def show_result(result):
    print(f'Итоговый капитал равен: {result:.2f}')


if __name__ == '__main__':
    while True:
        main()
        print('--------------------------')
        print('Продолжить нажмите <Enter>')
        ask = input('Для выхода введите <q>: ')
        if ask == 'q':
            break
