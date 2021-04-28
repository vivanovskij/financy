print('--------------------------------------------------------------')
print('|        Расчет среднего процента в год для прибыли          |')
print('--------------------------------------------------------------\n')


def main():
    percent = input('\nВведите кол-во процентов: ')
    years = input('Введите кол-во лет: ')
    try:
        percent = prep_value(percent)
        years = prep_value(years)
        result = mid_geometry(percent, years)
        show_result(result)
    except:
        print('Введены неверные данные...')


def ask_continue():
    print('--------------------------')
    print('Продолжить нажмите <Enter>')
    ask = input('Для выхода введите <q>: ')
    return ask


def mid_geometry(percent, years):
    return ((1 + percent / 100) ** (1. / years) - 1) * 100


def prep_value(value):
    value = value.replace(',', '.')
    return float(value)


def show_result(result):
    print(f'Доход равен: {result:.2f}% в год.')


if __name__ == '__main__':
    while True:
        main()
        if ask_continue() == 'q':
            break
