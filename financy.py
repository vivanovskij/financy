"""
Программа для работы с финансовыми расчетами
Version 1.1
Create by: Vitalij Ivanovskij <vivanovskijj@gmail.com>
Last change: 16.11.2020
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# Settings
WIDTH = 500
HEIGHT = 250
WIN_POS_X = 300
WIN_POS_Y = 100
TITLE = 'Financy calculate v1.1'
RESIZABLE_X = False
RESIZABLE_Y = False
FONT = 'Monaco 13'
NOTEBOOK_FONT = 'Monaco 10'
CAPTION_FONT = 'Monaco 13 bold'


class GUI():
    """Создает пользовательский интерфейс"""

    def __init__(self):
        self.root = self.create_main_GUI_window()
        self.tabs = self._create_GUI_tabs()
        self.applications = self._add_applications()
        self._bind_root_for_change_tabs()
        self.style = self.set_styles_for_GUI()
        self._application_init(0)

    def create_main_GUI_window(self):
        """Инициализация пользовательского окна"""
        root = Tk()
        root.title(TITLE)
        root.geometry(f'{WIDTH}x{HEIGHT}+{WIN_POS_X}+{WIN_POS_Y}')
        root.resizable(RESIZABLE_X, RESIZABLE_Y)
        return root

    def set_styles_for_GUI(self):
        """Инициализация стилей оформления виджетов"""
        style = ttk.Style()
        style.configure('.', font=FONT, padding=5)
        style.configure('TNotebook.Tab', font=NOTEBOOK_FONT, padding=3)
        return style

    def _create_GUI_tabs(self):
        """Создает виджет, который будет содержать вкладки на графическом окне"""
        tabs = ttk.Notebook(self.root, style='TNotebook')
        tabs.pack(fill='both', expand='yes')
        return tabs

    def _add_applications(self):
        """Инициализирует приложения"""
        self.income = Income(self)
        self.mid_percent = MidPersent(self)
        self.margin = Margin(self)
        return [self.income, self.mid_percent, self.margin]

    def _bind_root_for_change_tabs(self):
        """
        Устанавливает горячие клавиши <left>, <rigth> для root,
        для переключения вкладок.
        """
        self.root.bind('<KeyPress-Left>',
                       lambda event: self._select_prev_tab())
        self.root.bind('<KeyPress-Right>',
                       lambda event: self._select_next_tab())

    def _select_prev_tab(self):
        """Переход на предыдущую вкладку"""
        next_index, prev_index = self._get_tabs_indexes()
        self.tabs.select(prev_index)
        self._application_init(prev_index)

    def _select_next_tab(self):
        """Переход на следующую вкладку"""
        next_index, prev_index = self._get_tabs_indexes()
        self.tabs.select(next_index)
        self._application_init(next_index)

    def _application_init(self, index):
        """
        При переключении вкладки устанавливает курсор
        в первое поле для ввода
        """
        self.applications[index].entries[0].focus()

    def _get_tabs_indexes(self):
        """
        Определяет индексы предыдущей и следующей вкладок
        """
        cur_index = self.tabs.index('current')
        len_tabs = self.tabs.index('end')
        next_index = (cur_index + 1) % len_tabs
        prev_index = (cur_index - 1 + len_tabs) % len_tabs
        return (next_index, prev_index)

    def add_tab(self, frame, caption):
        """Добавляет приложение в отдельные вкладки"""
        self.tabs.add(frame, text=caption)
        tab_index = len(self.tabs.tabs()) - 1
        return tab_index

    def show_GUI(self):
        self.root.mainloop()


class Application():
    """Базовый класс для приложений"""

    def __init__(self, gui):
        self.gui = gui
        self.frame = ttk.Frame(gui.root)
        self.tab_index = self.gui.add_tab(self.frame, self.caption)

    def _add_label(self, text, row, column, sticky='e'):
        """Добавление текстового поля в интерфейс"""
        label = ttk.Label(self.frame, text=text, width=16)
        label.grid(row=row, column=column, sticky=sticky)
        return label

    def _add_entry(self, row, column):
        """Добавление поля ввода в интерфейс"""
        entry = ttk.Entry(self.frame, justify='center', font=FONT, width=10)
        entry.grid(row=row, column=column, sticky='n', padx=5)
        return entry

    def _prep_values(self, value):
        """Приведение данных из полей ввода к float"""
        value = value.replace(',', '.')
        return float(value)

    def _show_error_message(self):
        """Вывод сообщения об ошибке (если в поле ввода не число)"""
        messagebox.showinfo('Неверные данные', 'Введены неверные данные...')

    def _bind_entries(self, entries, function):
        """
        Установка гарячих для клавиш полей entries
        <Enter> - перемещение курсора на следующее поле 
                  и выполняет расчет результата
        <Up>/<Down> - перемещение курсора на поле вверх/вниз
        """
        for entry in entries:
            # Определение индексов полей: текущего, предыдущего и следующего
            cur_index = entries.index(entry)
            next_index = (cur_index + 1) % len(entries)
            prev_index = (cur_index - 1 + len(entries)) % len(entries)
            # Определение следующего поля для перемещения курсора
            # (при нажатии <Enter>, <Down>)
            next_entry = entries[next_index]
            # Определение предыдущего поля для перемещения курсора
            # (при нажатии <Up>)
            prev_entry = entries[prev_index]

            self._bind_entry('<KeyPress-Down>',
                             entry, next_entry)
            self._bind_entry('<KeyPress-Up>',
                             entry, prev_entry)
            self._bind_entry('<Return>',
                             entry, next_entry, function)
            self._bind_entry('<KP_Enter>',  # <KP_Enter> - Enter на доп. клав.
                             entry, next_entry, function)

    def _bind_entry(self, event_name, entry, next_entry, function=False):
        """
                Установка горячей клавиши для текущего поля
        event_name - тип события (<KeyPress-Down>,<KeyPress-Up>,<Return>')
        entry - текущее поле
        next_entry - поле в которое следует переместить курсор
        function -  функция, которая кроме перемещения курсора
                    будет выполняться при нажатии гарячей клавиши
                    (Для клавиши <Enter>).
                    Если не определена (False) - не выполняется ничего
                    (для клавиш <Up> и <Down>).
        """
        entry.bind(event_name,
                   lambda event,
                   entry=entry,
                   next_entry=next_entry,
                   function=function:
                   self._bind_apply(event, entry, next_entry, function))

    def _bind_apply(self, event, entry, next_entry, function):
        """Установка логики для горячей клавиши"""
        if self._check_entry(event, entry):
            next_entry.focus()
            if function:
                function()

    def _check_entry(self, event, entry):
        """Проверка поля на корректность данных"""
        value = entry.get()
        if not value:
            return True
        if value:
            try:
                # Если значение поля преобразовывается в float -
                # все в порядке
                value = self._prep_values(value)
                return True
            except:
                self._show_error_message()
                entry.delete(0, END)
                return False


class Margin(Application):
    """Класс для расчета маржи"""

    def __init__(self, gui):
        self.caption = 'Маржа'
        super().__init__(gui)
        self._add_labels()
        self.entries = self._add_entries()
        self._bind_entries(self.entries, self.margin_calculate)

    def _add_labels(self):
        self._add_label('', row=0, column=0)
        self._add_label('Себестоимость:', row=1, column=0)
        self._add_label('Цена:', row=2, column=0)
        self._add_label('Маржа равна:', row=1, column=2)
        self._add_label('Продажи:', row=3, column=0)
        self._add_label('Доход:', row=3, column=2, sticky='n')
        self.result_label = self._add_label(
            '', row=2, column=2, sticky='n')
        self.result_sales_label = self._add_label(
            '', row=4, column=2, sticky='n')

    def _add_entries(self):
        self.cost_price_entry = self._add_entry(row=1, column=1)
        self.price_entry = self._add_entry(row=2, column=1)
        self.sales_entry = self._add_entry(row=3, column=1)
        return [self.cost_price_entry, self.price_entry, self.sales_entry]

    def margin_calculate(self):
        """Расчет маржи"""
        cost_price = self.cost_price_entry.get()
        price = self.price_entry.get()
        sales = self.sales_entry.get()
        if cost_price and price:
            cost_price = self._prep_values(cost_price)
            price = self._prep_values(price)
            margin = (price - cost_price) / price * 100
            self.result_label['text'] = f'{margin:.1f}%'
            if sales:
                sales = self._prep_values(sales)
                income = sales * margin / 100
                self.result_sales_label['text'] = f'{income:.2f}'


class Income(Application):
    """Класс для расчета роста капитала"""

    def __init__(self, gui):
        self.caption = 'Рост капитала'
        super().__init__(gui)
        self._add_labels()
        self.entries = self._add_entries()
        self._bind_entries(self.entries, self._income_calculate)

    def _add_labels(self):
        self._add_label('', row=0, column=0)
        self._add_label('Капитал:', row=1, column=0)
        self._add_label('Процент(год.):', row=2, column=0)
        self._add_label('Пополнение(мес.):', row=3, column=0)
        self._add_label('Кол-во лет:', row=4, column=0)
        self._add_label('Итоговый капитал:', row=1, column=3)
        self.result_label = self._add_label(
            '', row=2, column=3, sticky='n')

    def _add_entries(self):
        self.capital_entry = self._add_entry(row=1, column=1)
        self.percent_entry = self._add_entry(row=2, column=1)
        self.replenish_entry = self._add_entry(row=3, column=1)
        self.years_entry = self._add_entry(row=4, column=1)
        return (self.capital_entry,
                self.percent_entry,
                self.replenish_entry,
                self.years_entry)

    def _income_calculate(self):
        """Расчет будущего капитала"""
        capital = self.capital_entry.get()
        percent = self.percent_entry.get()
        replenish = self.replenish_entry.get()
        years = self.years_entry.get()
        if capital and percent and years:
            capital = self._prep_values(capital)
            if replenish:
                replenish = self._prep_values(replenish)
            else:
                replenish = 0
            percent = self._prep_values(percent)
            # процент вычисляется как среднее геометрическое
            # за период 12 месяцев
            percent = ((1 + percent / 100) ** (1 / 12) - 1) * 100
            years = self._prep_values(years)
            monthes = int((years * 12) // 1)

            for i in range(0, monthes):
                capital += capital * percent / 100
                capital += replenish
            self.result_label['text'] = f'{capital:,.2f}'


class MidPersent(Application):
    """
    Класс для расчета среднего процента в год.
    Пример:
    Получаем прибыль 40% за 4 года. Какая доходность в год?
    Делить 40% на 4 не верно. Нужно взять среднее геометрическое значение.
    Расчитывается как корень 4-й степени (4 года) из 1.40 (прирост 40%)
    Ответ: 8.78%

    """

    def __init__(self, gui):
        self.caption = 'Средний процент'
        super().__init__(gui)
        self._add_labels()
        self.entries = self._add_entries()
        self._bind_entries(self.entries, self.mid_percent_calculate)

    def _add_labels(self):
        self._add_label('', row=0, column=0)
        self._add_label('Процент:', row=1, column=0)
        self._add_label('Кол-во лет:', row=2, column=0)
        self._add_label('Средний процент:', row=1, column=3)
        self.result_label = self._add_label(
            '', row=2, column=3, sticky='n')

    def _add_entries(self):
        self.percent_entry = self._add_entry(row=1, column=1)
        self.years_entry = self._add_entry(row=2, column=1)
        return [self.percent_entry, self.years_entry]

    def mid_percent_calculate(self):
        """Расчет среднего процента"""
        percent = self.percent_entry.get()
        years = self.years_entry.get()
        if percent and years:
            percent = self._prep_values(percent)
            years = self._prep_values(years)
            mid_percent = ((1 + percent / 100) ** (1 / years) - 1) * 100
            self.result_label['text'] = f'{mid_percent:.2f}%'


def main():
    gui = GUI()
    gui.show_GUI()


if __name__ == '__main__':
    main()
