#! /usr/bin/env python3

import sys, contextlib


def start_tag(tag, **kwargs):
	print('<{}{}>'.format(tag, ''.join(' {}="{}"'.format(k, v) for k, v in kwargs.items())))


# As suggested in https://docs.python.org/3/library/contextlib.html?highlight=contextmanager#contextlib.contextmanager
@contextlib.contextmanager
def tag(tag, **kwargs):
	start_tag(tag, **kwargs)
	yield
	print('</{}>'.format(tag))


def main(size = '10', rule = '30'):
	size = int(size)
	rule = int(rule)
	
	def state_bits(state):
		return '{{0:0{}b}}'.format(size).format(state)
	
	def step(state, size):
		
		return sum((rule >> (((state | state << size | state << size * 2) >> size + i - 1) & 0b111) & 1) << i for i in range(size))
	
	def generate_state(state):
		bits = state_bits(state)
		
		start_tag('a', name = bits)
		
		for i, b in enumerate(bits):
			with tag('a', href = '#' + state_bits(state ^ 1 << (size - i - 1))):
				print(b)
			
			print('|')
		
		with tag('a', href = '#' + state_bits(step(state, size))):
			print('Step')
		
		for _ in range(100):
			start_tag('br')
	
	def generate_page():
		print('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN") "http://www.w3.org/TR/html4/loose.dtd">')
		
		with tag('html'):
			with tag('head'):
				with tag('title'):
					print('Rule 30 in HTML!')
			
			with tag('body'):
				for i in range(2 ** size):
					generate_state(i)
	
	generate_page()


main(*sys.argv[1:])
