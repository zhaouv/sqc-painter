# -*- coding: utf-8 -*-
#可以使用中文注释，需要在另外的IDE中输入中文
#
import pya

layout = pya.Layout()
top = layout.create_cell("TOP")
l1 = layout.layer(1, 0)
top.shapes(l1).insert(pya.Box(0, 0, 1000, 200))
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
class Animal(object):
    def run(self):
        print('Animal is running...')
class Dog(Animal):
    def run(self):
        print('Dog is running...')
    def eat(self):
        print('Eating meat...')
class Cat(Animal):
    pass
dog = Dog()
dog.run()
dog.eat()
#函数和类能够正常使用
top.shapes(l1).insert(pya.Box(0, 0, my_abs(-100), 2000))
layout.write("[pythonout_test].gds")




#