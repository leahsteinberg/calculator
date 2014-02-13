#!/usr/bin/env python
import cmd

# make it so it can deal with a number alone
# dont use list word


def parse(string):
	"""
	>>> parse('(232+4)3*5-32-9')
	3499
	>>> parse('4*4')
	16
	>>> parse('3(4*3)*5+8-7*3')
	167
	>>> parse('4*4')
	16
	>>> parse('4/4')
	1
	>>> parse('2(4*3)')
	24
	>>> parse('4')
	4
	>>> parse('4')
	4

	"""
	if string == 'quit':
		quit()
	
	string = number_touch(string)
	string = parens(string)
	tree = split_ops(string, ['+', '-'])
	if tree[0].count('*') or tree[0].count('/'):
		tree[0] = split_ops(tree[0], ['*', '/'])
		tree[0] = make_tree(tree[0], ['*', '/'])

	tree = make_tree(tree, ['+', '-'])
	return calc(tree)

def number_touch(calc_input):
	# input: something like (3)4, output: something like (3)*4 
	# if a number is right next to a parentheses, insert a multiplication symbol in between
	"""
	>>> number_touch('(2)3')
	'(2)*3'
	>>> number_touch('2+3(2+3)')
	'2+3*(2+3)'
	>>> number_touch('2(3)4')
	'2*(3)*4'
	"""

	touch_list = []
	for i in range(1, len(calc_input)-1):
		char = calc_input[i]
		if char == '(':
			if calc_input[i-1].isdigit():
				touch_list.append(i)
		if char == ')':
			if calc_input[i+1].isdigit():
				touch_list.append(i+1)
	# what does i represent in either case? the index where it will be?? issue here.. aft

	#need to put in * in order.. 
	#touch list needs ot be in assending order,(they will be)
	#and after i put on in touch list, I need to add 1 ot all the other ones in touch list and 
	#pop that one from touch list
	for i in range(len(touch_list)):
		index = touch_list[i]
		calc_input = calc_input[:index] + '*' + calc_input[index:]
		touch_list = map(lambda x: x+1, touch_list)

	return calc_input


def split_ops(string, category):
	# split on +, - OR *, /
	"""
	splits a string on pluses and minuses, makes a list
	>>> split_ops('2+3-4', ['+', '-'])
	['2', '+', '3', '-', '4']
	>>> split_ops('2*3/4+9*5+4-2435',  ['+', '-'])
	['2*3/4', '+', '9*5', '+', '4', '-', '2435']
	>>> split_ops('2*3/4+9*5+4-2435',  ['*', '/'])
	['2', '*', '3', '/', '4+9', '*', '5+4-2435']
	"""

	if len(string) == 1:
		string = string + '*1'
	tree = []
	nonop_buffer = ''
	for c in string:
		if c in category:
			tree.append(nonop_buffer)
			nonop_buffer = ''
			tree.append(c)
		else:
			nonop_buffer+=c
	tree.append(nonop_buffer)
	return tree

def make_tree(list, category):
	#takes in a list separated by + and - and puts it into a very left-heavy tree
	"""
	>>> make_tree(['1', '+', '2'], ['+', '-'])
	['+', '1', '2']
	>>> make_tree(['2', '+', '3', '-', '4'], ['+', '-'])
	['-', ['+', '2', '3'], '4']
	>>> make_tree(['232', '+', '4*3/5', '-', '32', '-', '9'], ['+', '-'])
	['-', ['-', ['+', '232', ['/', ['*', '4', '3'], '5']], '32'], '9']
	>>> make_tree(['3', '+', '2', '-', '3*4', '-', '2*3'], ['+', '-'])
	['-', ['-', ['+', '3', '2'], ['*', '3', '4']], ['*', '2', '3']]
	>>> make_tree(['32', '*', '4', '/', '3'], ['*', '/'])
	['/', ['*', '32', '4'], '3']

	"""
	tree = list[0]
	list.pop(0)
	for i in range(0, len(list)):
		if list[i] in category:
			subtree = list[i+1]
			if subtree.count('*') or subtree.count('/'):
				subtree = split_ops(subtree, ['*', '/'])
				subtree = make_tree(subtree, ['*', '/'])
			tree = [list[i], tree, subtree] 
	return tree


def calc(tree):
	"""
	takes in a tree or nested tree and "traverses" it to calculate based on order of operations
	>>> calc(['+', '2', '3'])
	5
	>>> calc(['+', ['-', '1', '3'], '4'])
	2
	>>> calc(['*', ['+', '3', '2'], '4'])
	20
	>>> calc(['/', ['/', '4', '2'], '2'])
	1
	"""

	if isinstance(tree[1], list):
		tree[1] = calc(tree[1]) 
	if isinstance(tree[2], list):
		tree[2] = calc(tree[2])
	if not isinstance(tree[1], list) and not isinstance(tree[2], list):
		operators = {"+": lambda x,y: x+y, "-": lambda x,y: x-y, "*": lambda x,y: x*y, "/": lambda x,y: x/y} # problem here with underflow??
		op_function = operators[tree[0]]
		return op_function(int(tree[1]), int(tree[2]))


def parens(string):
	"""
	>>> parens('(232+4)*3*5-32-9')
	'236*3*5-32-9'
	>>> parens('3*4*5*6-9')
	'3*4*5*6-9'
	>>> parens ('((3+4)*2)+3')
	'14+3'

	"""
	if '(' in string:
		parencounter = 0
		maxparen = 0
		index=0
		for c in string:
			if c == '(':
				parencounter+=1
				if parencounter>maxparen:
					maxparen = parencounter
					paren_index = index
			if c == ')':
				parencounter-=1
			index+=1

		#get copy of interior of parentheses	
		in_parens = ''
		for i in range(paren_index, len(string)): # weird hardcoding
			if string[i] == ')':
				close_index = i
				break
		in_parens = string[paren_index:close_index]
		in_parens = in_parens[1:len(in_parens)]

		#remove all trace of parentheses from string
		string = string[:paren_index] + string[close_index+1:]#weird hardcoding?
		
		paren_tree = split_ops(in_parens, ['+', '-'])
				#now it should be a list
		if paren_tree[0].count('*') or paren_tree[0].count('/'):
			paren_tree[0] = split_ops(paren_tree[0], ['*', '-'])
			paren_tree[0] = make_tree(paren_tree[0], ['*', '/'])
		paren_tree = make_tree(paren_tree, ['+', '-'])
		#now we should have a full tree of the inner parens
		paren_string = str(calc(paren_tree))
		#get a string calculation of what was in the parens
		string = string[:paren_index] + paren_string + string[paren_index:]
		
		#replace the whole parentheses with a new string
		return parens(string)
	else:
		#there's no parentheses in this
		return string

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	while(True):
		string = raw_input('Calculator: ')
		if len(string) >  0:
			print parse(string)



