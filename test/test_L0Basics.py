#!/usr/bin/env python
# -*- coding: utf-8 -*-

#%%
#-------------------------------------------------------------
print('1+1=',1+1)
#我是注释
print('I\'m \"OK\"!')
print(r'\\\t\\')#不转义
print('\\\t\\')
print('\n')
#print('''line1
#line2
#line3''')
print(1!=1)
print(not (True or False))
print(None)
print(10/3,10.0/3)
print(ord('A'))
print(chr(65))
print(u'中文')
print('中文')

print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Michael', 1000000))
# %d 整数 
# %f 浮点数 
# %s 字符串 
# %x 十六进制整数 
#如果你不太确定应该用什么，%s永远起作用
#它会把任何数据类型转换为字符串：
print('%2d-%02d' % (3, 1))
print('%.2f' % 3.1415926)
#Unicode字符串
print(u'Hi, %s' % u'Michael')
print(1,1)
print(1)
print(1,1)
#end=int(raw_input('input a number'))
#print(end
print('-------------------------------------------------------')
#%%
#使用list和tuple
#list
classmates = ['Michael', 'Bob', 'Tracy']
print(len(classmates))
print(classmates[0])
print(classmates[-1])
classmates.append('Adam')#追加
print(classmates)
classmates.insert(1, 'Jack')#插入
print(classmates.pop())#删末尾
print(classmates)
classmates.pop(1)#删指定
classmates[1] = 'Sarah'
alist = ['python', True, [100, 'php'], 'scheme']
print(alist)
print(alist[2][1])

#tuple
#tuple不能修改
atuple=('tuple',1,True)
print(atuple)
oneatuple=('one',)#只有一个元素的tuple
gaituple=(1,2,[1,2])#list放在tuple中可以修改
print('-------------------------------------------------------')
#%%
#条件判断和循环
if True:
    print('a')
    print('a')
#四个空格是缩进
if False:
    print('a')
else:
    print('b')
    
if False:
    print('a')
elif False:
    print('b')
else:
    print('c')
#是非零数值、非空字符串、非空list等
#就判断为True，否则为False

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
sum = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum = sum + x
print(sum)

print(range(5))
sum = 0
for x in range(101):
    sum = sum + x
print(sum)

sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
#死循环可用Ctrl+C退出
print('-------------------------------------------------------')
#%%
#使用dict和set
dict1 = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(dict1['Michael'])
dict1['Adam'] = 67
dict1['Jack'] = 90
print(dict1)
print( 'Thomas' in dict1)#判断是否存在
print(dict1.get('Bob'))
print(dict1.get('Thomas'))#不存在会返回None
print(dict1.get('Thomas', -1))#不存在会返回-1
#删除key，pop(key)
print(dict1.pop('Bob'))
#dict需要占用大量的内存，内存浪费多
#dict的key必须是不可变对象

set1 = set([1, 2, 3])
set1.add(4)
set1.add(4)
print(set1)
set1.remove(4)
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)
#不可变对象
a = 'abc'
b = a.replace('a', 'A')
print(a,b)
print('-------------------------------------------------------')
#%%
#函数

#help(abs)
#help(cmp)
a=abs
print(a(-1))

def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
#return None可以简写为return
pass
#pass语句什么都不做
#pass可以用来作为占位符
print(my_abs(-2))

import math

def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
x, y = move(100, 100, 60, math.pi / 6)
print(x, y)
r = move(100, 100, 60, math.pi / 6)
print(r)
#返回值是一个tuple

def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
enroll('Sarah', 'F')
enroll('Bob', 'M', 7)
enroll('Adam', 'M', city='Tianjin')
#默认参数最好指向不变对象
#
#Python函数在定义的时默认参数的值就被计算出来
#默认参数也是一个变量
#随着调用函数
#默认参数的内容可能会改变
#会导致逻辑错误
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L

#通过list或tuple可以实现可变参数
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc([1, 2, 3]))
print(calc((1, 3, 5, 7)))
#可变参数
def calc2(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc2(1, 2))
print(calc2())
#参数numbers接收到的是一个tuple
#加一个*号，把list或tuple的元素变成可变参数传进去
nums = [1, 2, 3]
print(calc2(*nums))

#关键字参数
#传入0个或任意个含参数名的参数，
#关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
person('Michael', 30)
person('Bob', 35, city='Beijing')
person('Adam', 45, gender='M', job='Engineer')
kw = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **kw)

#参数组合
#顺序必须是：
#必选参数、默认参数、可变参数和关键字参数
def func(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
func(1, 2)
func(1, 2, c=3)
func(1, 2, 3, 'a', 'b')
func(1, 2, 3, 'a', 'b', x=99)
args = (1, 2, 3, 4)
kw = {'x': 99}
func(*args, **kw)
#对于任意函数，都可以通过
#类似func(*args, **kw)的形式调用
#无论它的参数是如何定义的

#递归函数
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
print(fact(5))
#===> fact(5)
#===> 5 * fact(4)
#===> 5 * (4 * fact(3))
#===> 5 * (4 * (3 * fact(2)))
#===> 5 * (4 * (3 * (2 * fact(1))))
#===> 5 * (4 * (3 * (2 * 1)))
#===> 5 * (4 * (3 * 2))
#===> 5 * (4 * 6)
#===> 5 * 24
#===> 120

#递归调用的次数过多，会导致栈溢出

#尾递归是指，在函数返回的时候，调用自身本身
#并且，return语句不能包含表达式
#这样，编译器或者解释器就可以把尾递归做优化
#使递归本身无论调用多少次，都只占用一个栈帧
#不会出现栈溢出的情况
def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
print(fact(5))
#===> fact_iter(5, 1)
#===> fact_iter(4, 5)
#===> fact_iter(3, 20)
#===> fact_iter(2, 60)
#===> fact_iter(1, 120)
#===> 120
#Python解释器没有做尾递归优化
print('-------------------------------------------------------')
#%%
#高级特性

#切片
#Slice
#不包含最后一个数字
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[0:3])
print(L[:3])
print(L[2:])
print(L[-2:])
print(L[-2:-1])
L = range(100)
print(L[:10:2])#前10个数，每两个取一个
print(L[::5])#所有数，每5个取一个
print(L[::-1])#反序
print(L[:])
#tuple的切片还是tuple
print((0, 1, 2, 3, 4, 5)[:3])
print('ABCDEFG'[:3])
print('ABCDEFG'[::2])
print(u'一个中文句子'[::2])

#迭代
#Iteration
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
#
print(u'------不同------')#
##for value in d.itervalues():
#
print(u'------不同------')#
##    print(value)
#
print(u'------不同------')#
##for k, v in d.iteritems():
#
print(u'------不同------')#
##    print(k,v)
for ch in 'ABC':
    print(ch)
#判断一个对象是可迭代对象
from collections import Iterable
print(isinstance('abc', Iterable))
print(isinstance([1,2,3], Iterable))
print(isinstance(123, Iterable))
#enumerate函数可以把一个list变成索引-元素对
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)

#列表生成式
#List Comprehensions
print(range(1, 11))
print([x * x for x in range(1, 11)])
print([x * x for x in range(1, 11) if x % 2 == 0])
print([m + n for m in 'ABC' for n in 'XYZ'])
import os # 导入os模块，模块的概念后面讲到
print([d for d in os.listdir('.')])
d = {'x': 'A', 'y': 'B', 'z': 'C' }
#
print(u'------不同------')#
##print([k + '=' + v for k, v in d.iteritems()])
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])#变小写
#isinstance函数可以判断一个变量是不是字符串
print(isinstance('abc', str))
print(isinstance(1, str))
L = ['Hello', 'World', 18, 'Apple', None]
print([s.lower() for s in L if isinstance(s, str)])
print([s.lower() if isinstance(s,str) else s for s in L])

#生成器
#Generator
#一边循环一边计算
g = (x * x for x in range(10))
#创建generator的一种方法
#把一个列表生成式的[]改成()
print(g)
#
print(u'------不同------')#
##print(g.next(),g.next(),g.next())
for n in g:
    print(n)
#用包含yield关键字的函数定义generator
#遇到return或执行完函数体最后一行结束循环
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
for n in fib(6):
    print(n)
def odd1():
    print('step 1')
    yield 1
    print('step 2')
    yield 3
    print('step 3')
    yield 5
odd2=odd1()
for n in odd2:
    print(n)
for n in odd1():
    print(n)
print('-------------------------------------------------------')
#%%
#函数式编程

#高阶函数
def add1(x, y, f):
    return f(x) + f(y)
print(add1(-5,6,abs))

#map
def fxx(x):
    return x * x
print(map(fxx,[1,2,3,4]))
print(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

#reduce
#reduce(f, [x1, x2, x3, x4]) 
# = f(f(f(x1, x2), x3), x4)
def fn(x, y):
    return x * 10 + y
#
print(u'------不同------')#
##print(reduce(fn, [1, 3, 5, 7, 9]))
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
#
print(u'------不同------')#
##print(reduce(fn, map(char2num, '13579')))
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return #
print(u'------不同------')#
##reduce(fn, map(char2num, s))
print(str2int('1235'))
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
def str2int(s):
    return #
print(u'------不同------')#
##reduce(lambda x,y: x*10+y, map(char2num, s))
print(str2int('1235'))
#
L = ['adam', 'LISA', 'barT']
def strAaa(s):
    if not isinstance(s, str):
        raise TypeError('bad operand type')
    return s[0].upper()+s[1:].lower()
print(strAaa('asDF'))
print(str.title('asDF'))
print(map(strAaa,L))
print(map(str.title,L))
#
print(u'------不同------')#
##print(reduce(lambda x,y:x*y,range(1,5)))

#filter
#过滤序列
def is_odd(n):
    return n % 2 == 1
print(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
def not_empty(s):
    return s and s.strip()
print(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
def isNotPrime(n):
    if n == 1:
        return True
    else:
        return 0 in map(lambda x: n % x, range(2, n))
print(filter(isNotPrime, range(1, 21)))

#sorted
#排序
print(sorted([36, 5, 12, 9, 21]))
def reversed_cmp(x, y):
    return -1*cmp(x,y)
#
print(u'------不同------')#
##print(sorted([36, 5, 12, 9, 21],reversed_cmp))
print(sorted(['bob', 'about', 'Zoo', 'Credit']))
def cmp_ignore_case(x, y):
    return cmp(x.upper(),y.upper())
#
print(u'------不同------')#
##print(sorted(['bob', 'about', 'Zoo', 'Credit'],cmp_ignore_case))
print('-------------------------------------------------------')
#%%
#返回函数
#函数作为返回值
#闭包 Closure
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f = lazy_sum(1, 3, 5, 7, 9)
print(f)
print(f())
#闭包引用循环变量会有问题，需要多嵌套一层函数
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs
f1, f2, f3 = count()
print(f1())
print(f2())
print(f3())
#通过多套一层函数，把传引用变成传值
#可利用lambda函数缩短代码
def count():
    fs = []
    for i in range(1, 4):
        def f(j):
            print(j,j,j,j)
            def g():
                print(j,j,j,j)
                return j*j
            return g
        fs.append(f(i))
    return fs
f1, f2, f3 = count()
print(f1)
print(f1())
print(f2())
print(f3())

#匿名函数
#关键字lambda表示匿名函数，冒号前是函数参数
#只能有一个表达式，不需要return
#返回值就是该表达式的结果
f = lambda x: x * x
print(f(5))
#可以把匿名函数作为返回值返回
def build(x, y):
    return lambda: x * x + y * y
ff=build(1,2)
print(ff)
print(ff())
print(build(1,2))
print(build(1,2)())

#装饰器
#Decorator
#不修改函数定义,在代码运行期间动态增加功能
def now():
    print('2013-12-25')
f = now
f()
print(f.__name__)
#定义log作为装饰
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
#把@log放到now()函数的定义处，相当于执行了语句
#now = log(now)
@log
def now():
    print('2013-12-25')
now()
#同名的now变量指向了新的函数
#调用now()将执行在log()函数中返回的wrapper()函数
#
#如果decorator本身需要传入参数
#需要编写一个返回decorator的高阶函数
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
#下一行等效于now = log('execute')(now)
@log('execute')
def now():
    print('2013-12-25')
now()
print(now.__name__)
#需要把原始函数的__name__等属性
#复制到wrapper()函数中
#在定义wrapper()前加上@functools.wraps(func)即可
import functools
#
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log('execute')
def now():
    print('2013-12-25')
now()
print(now.__name__)

#偏函数
#Partial function
#把函数的某些参数固定住（设置默认值）
#返回一个新的函数
import functools
int2 = functools.partial(int, base=2)
print(int2('10110'))
print(int2('1276', base=10))
# kw = { base: 2 }
# int('10010', **kw)
max2 = functools.partial(max, 10)
print(max2(5, 6, 7))
# args = (10, 5, 6, 7)
# max(*args)
print('-------------------------------------------------------')
#%%
#模块
#Module
#一个.py文件就称之为一个模块
#用目录作为顶层包名
#__init__.py是该文件夹名对应的模块
#第4行是一个字符串，表示模块的文档注释
#' a test module '
#第6行使用__author__变量把作者写进去
#__author__ = 'Michael Liao'
import sys
#导入模块
def test():
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')
if __name__=='__main__':
    test()
#argv变量，用list存储了命令行的所有参数
#argv第一个参数是该.py文件的名称
#python hello.py
#python hello.py Michael
print(sys.argv)
#在命令行运行模块文件时
#Python解释器把特殊变量__name__置为__main__
#可用于区分模块是否被直接执行
#import改模块时test()将不会被执行
#hello.test()

#别名
#import cStringIO as StringIO
#try:
#    import cStringIO as StringIO
#except ImportError: # 导入失败会捕获到ImportError
#    import StringIO
#
#try:
#    import json # python >= 2.6
#except ImportError:
#    import simplejson as json # python <= 2.5

#作用域
#正常的函数和变量名是公开的（public）可被直接引用
#类似__xxx__这样的变量是特殊变量
#可以被直接引用，但是有特殊用途
#类似_xxx和__xxx这样的函数或变量是非公开的（private），
def _private_1(name):
    return 'Hello, %s' % name
def _private_2(name):
    return 'Hi, %s' % name
def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)
print(greeting('Panda'))
print(greeting('Li'))

#安装第三方模块
#安装PIL
#pip install PIL
#import Image
#im = Image.open('temp.PNG')
#print(im.format, im.size, im.mode
#结果：PNG (384, 248) RGBA
#im.thumbnail((200, 100))
#im.save('thumb.jpg', 'JPEG')
#import sys
#print(sys.path#搜索路径
#sys.path.append('/Users/michael/my_py_scripts')
#这种方法是在运行时修改，运行结束后失效

#使用__future__
#__future__模块,把下一个新版本的特性导入到当前版本
#Python3.x的新的字符串的表示方法
#在3.x中，所有字符串都被视为unicode
#通过unicode_literals来使用Python 3.x的新的语法
#
#from __future__ import unicode_literals
#
print(u'------不同------')#
##print('\'xxx\' is unicode?', isinstance('xxx', unicode))
#
print(u'------不同------')#
##print('u\'xxx\' is unicode?', isinstance(u'xxx', unicode))
print('\'xxx\' is str?', isinstance('xxx', str))
print('b\'xxx\' is str?', isinstance(b'xxx', str))
#在Python 2.x中，如果是整数相除，结果仍是整数
#余数会被扔掉
#要做精确除法，必须把其中一个数变成浮点数
#在Python 3.x中，所有的除法都是精确除法
#地板除用//表示
#在Python 2.7的代码中直接使用Python 3.x的除法
#
#from __future__ import division
print('10 / 3 =', 10 / 3)
print('10.0 / 3 =', 10.0 / 3)
print('10 // 3 =', 10 // 3)
print('-------------------------------------------------------')
#%%
