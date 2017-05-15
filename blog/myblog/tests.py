from django.test import TestCase
# coding:utf8
list1 = [1,2,3,4,5,6,7,8,9,0]
list2=['hello','world','hello','victor','i','find','thx']
tuple1 = (1,2,3,4,5,6,7,8,9,0)
tuple2=('hello','world','hello','victor','i','find','thx')
# list1 = [1,2,3,4,5,6,7,8,9,0]
# list2=['hello','world','hello','victor','i','find','thx']
list3 = ['what','are','you','doing']
list3.extend(list2)
list2.remove('hello')
list1.reverse()
print list1
