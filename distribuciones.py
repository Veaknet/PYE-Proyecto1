#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import *
from random import *

# Implementacion de la distribucion Bernoulli
def bernoulli(p=0.5, n=1):
	u = [uniform(0.0,1.0) for i in xrange(n)]
	return [ int(val > 1-p) for val in u]

# Implementacion de la distribucion Geometrica
def geometrica(p=0.5, n=1):
	x = [1,]*n
	for i in xrange(n):
		while not bernoulli(p=p)[0]:
			x[i]=x[i]+1
	return x