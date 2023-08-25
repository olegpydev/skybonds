"""
Решение тестового задания Мегатрейдер

Реализованны 2 функции (подробные описания в самих функциях):
- megatrader - основная, реализация методом динамического программирования
- brute_force - контрольная и для сравнения скорости, использующая полный перебор

--------------------
Субъективная оценка сложности: 7
Затраченное время: 2-3 часа основная реализация + тестирование, рефакторинг,
                   документация и поэкспериментировать

Test input:
---------------------
2 2 8000
1 alfa-05 100.2 2
2 alfa-05 101.5 5
2 gazprom-17 100.0 2

---------------------
Speed tests:

lots=100, money=10_000
megatrader:     ~ 0.3 s
brute_force:    ~ 0.05 - 1.2 s

lots=100, money=20_000
megatrader:     ~ 0.7 s
brute_force:    ~ 6 - 42 s

lots=200, money=10_000
megatrader:     ~ 0.5 s
brute_force:    ~ 3 - 36+ s


megatrader:
lots=100, money=100_000    ~ 4.5 s
lots=1000, money=10_000    ~ 3 s

lots=1000, money=100_000   ~ 45 s

"""

from functools import cache


@cache
def get_worth_profit(data: tuple) -> tuple[int, int]:
    """
    Функция для подсчета затрат на покупку лота (worth) и полученной от него прибыли (profit).
    Из исходных данных в виде кортежа: day, name, price, count

    :param data: (day, name, price, count)
    :return: worth, profit
    """
    _, _, price, count = data
    worth = int(price * 10 * count)
    profit = count * 30 - (worth - count * 1000)
    return worth, profit


def brute_force(lst: list[tuple], money: float, n: int) -> float:
    """
    Функция полного перебора для подсчета максимальной прибыли, без восстановления покупок лотов.
    (тк она очень медленная, то делать в ней восстановление не вижу смысла)
    Сложность алгоритма O(2^n)

    Также поскольку данная реализация алгоритма рекурсивная, то имеет ограничение на глубину рекурсии.
    Т.е., количество лотов не более 800-900
    """
    if money == 0 or n == 0:
        return 0
    worth, profit = get_worth_profit(lst[n - 1])
    if worth > money:
        return brute_force(lst, money, n - 1)
    else:
        return max(profit + brute_force(lst, money - worth, n - 1), brute_force(lst, money, n - 1))


def megatrader(lst: list[tuple], money: int) -> tuple[int, list[tuple]]:
    """
    Решение задачи методом динамического программирования.
    Сложность алгоритма O(n * m)
    где n - количество лотов, m - общее количество денег

    Расход памяти в общем случае O(n * m), что при больших значениях n и m может приводить
    к перерасходу памяти, поэтому для сокращения расхода памяти используется вариант с
    сохранением только одной строки в массиве dp, таким образом расход памяти становится
    O(m)
    Но так как восстановить последовательность в таком случае невозможно, то используется
    дополнительный массив для хранения уникальных значений накопленного профита для всех лотов,
    что гораздо меньше, чем полноразмерный массив (n * m), по результатам тестов
    его размер (~20 x n).
    Итого по расходу памяти O(m)
    """

    dp = [0] * (money + 1)

    history = []

    for i in range(len(lst)):
        for j in range(len(dp) - 1, 0, -1):
            worth, profit = get_worth_profit(lst[i])
            if worth <= j:
                dp[j] = max(dp[j], dp[j - worth] + profit)

        # сохраняем только уникальные значения накопленного профита, с учетом исходного порядка
        history.append(tuple(dict.fromkeys(dp)))

    # восстанавливаем последовательность купленных лотов в обратном порядке
    max_profit = dp[money]
    result = []
    last_line = len(history) - 1

    while history:
        line = history.pop()
        if max_profit not in line:
            result.append(lst[last_line])
            _, profit = get_worth_profit(lst[last_line])
            max_profit -= profit
        if not history and max_profit:
            result.append(lst[0])
        last_line = len(history)

    return dp[money], result[::-1]


def test(lots: int = 100, money: int = 10000) -> None:
    """
    Функция для тестирования.
    Генерирует набор случайных данных указанного количества и сравнивает скорость и корректоность
    получаемых результатов функции megatrader и функции brute_force
    """
    from random import random, randint, choices
    from string import ascii_lowercase
    from time import perf_counter

    def timed(func):
        def wrapper(*args, **kwargs):
            t = perf_counter()
            res = func(*args, *kwargs)
            print(perf_counter() - t)
            return res
        return wrapper

    lst = []

    for i in range(lots):
        day = i
        name = ''.join(choices(ascii_lowercase, k=5))
        price = round((random() + 0.5) * 100, 1)
        count = randint(1, 20)
        lst.append((day, name, price, count))

    for i in lst:
        print(*i)

    @timed
    def megatrader_test() -> tuple[int, list[tuple]]:
        return megatrader(lst, money)

    max_profit, result = megatrader_test()
    print(max_profit)
    for res in result:
        print(*res)
    print()

    @timed
    def brute_force_test() -> float:
        return brute_force(lst, money, len(lst))

    # на больших тестовых параметрах (lots, money) следующие 3 строчки лучше комментировать
    # тк очень долго работает полный перебор
    res_brute_force = int(brute_force_test())
    assert max_profit == res_brute_force
    print(res_brute_force)


def main():
    n, m, money = map(int, input().split())
    lst = []
    while (s := input()) != '':
        day, name, price, count = s.split()
        lst.append((int(day), name, float(price), int(count)))

    max_profit, result = megatrader(lst, money)

    print(max_profit)
    for res in result:
        print(*res)
    print()


if __name__ == '__main__':
    main()
    # test(lots=100, money=10_000)
