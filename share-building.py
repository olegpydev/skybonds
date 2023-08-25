"""
Решение тестового задания Долевое строительство

Сложность алгоритма O(n)
Расход памяти O(n)

--------------------
Скорость работы:
10_000_000 ~ 4.5 s (без учета ввода и печати данных)

--------------------
Субъективная оценка сложности: 1
Затраченное время: 10-15 минут на сам кад

Test input:
--------------------
4
1.5
3
6
1.5

--------------------
"""


def main():
    lst = [float(input()) for _ in range(int(input()))]
    sum_lst = sum(lst)
    result = [round(i / sum_lst, 3) for i in lst]
    for i in result:
        print(f'{i:.3f}')


if __name__ == '__main__':
    main()
