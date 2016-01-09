#!/usr/bin/python
import unittest

class demo(object):
	def __init__(self, name, wealth):
		self.name = name
		self.wealth = wealth
				
	def show(self):
		print self.name, self.wealth, self.extra
		
	def addExtraSlot(self):
		self.extra = "more!"
		
a = demo("dale", "not much")
a.addExtraSlot()
a.show()
demo.extra = "somevalue"

b = demo("fred", "lots")
b.show()

f = open("stuff.py", "w")
f.write("hello")
f.close()

lines = [line.strip() for line in open("stuff.py")]

print lines

# Tut 8 sheet
class Calc(object):
	def __init__(self):
		self.count = 0
		
	def add(self, number):
		self.count += number
		
	def multiply(self, number):
		self.count *= number
		
	def get_value(self):
		return self.count
		
c = Calc()

assert (toRomain(4) == "IV") 
expect toNumber("")