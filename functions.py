# Copyright (C) 2021 Anatole Hernot (github.com/ahernot), Mines Paris (PSL Research University). All rights reserved.



def type_input (message: str, type_, max_iter: int = 10):
    val = None
    iter_nb = 0
    while True:
        val = input(message)

        try:
            val = type_(val)
            return val
        except:
            print('invalid input')

        iter_nb += 1

        if iter_nb > max_iter:
            raise InterruptedError('invalid input')
