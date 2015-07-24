#!/usr/bin/env python
# -*- coding: utf-8 -*-

from farm import *
from simpy import * 
from time import *
from random import *

from distribuciones import *

# Enumerado para modelar los posibles 
# estados de salud de un individuo dentro 
# de la simulacion
class IndividualState:
	Sano = 1
	Infectado_Sano = 2
	Infectado_Enfermo = 3
	Muerto = 4


class bird(object):
	state = IndividualState.Sano
	InitialIndividual = 0
	InitialInfected = 0
	MinLatencyInfection = 0
	MaxLatencyInfection = 0
	IllnessDuration = 0
	controllerState = None
	contagionFactor = 0
	mutationFactor = 0
	MaxIllnessPeriod = 0

	def __init__(
		self, 
		InitialIndividual,
		InitialInfected,
		MinLatencyInfection,
		MaxLatencyInfection,
		IllnessDuration,
		contagionFactor,
		mutationFactor,
		MaxIllnessPeriod,
		state = IndividualState.Sano,
		controllerState = None
	):
		self.InitialIndividual = InitialIndividual
		self.InitialInfected = InitialInfected
		self.MinLatencyInfection = MinLatencyInfection
		self.MaxLatencyInfection = MaxLatencyInfection
		self.IllnessDuration = IllnessDuration
		self.contagionFactor = contagionFactor
		self.mutationFactor = mutationFactor
		self.MaxIllnessPeriod = MaxIllnessPeriod
		self.state = state
		self.controllerState = controllerState

	def setState(self,state):
		self.state = state

	def getState(self):
		return self.state

	def setIllnessDuration(self, duration):
		self.IllnessDuration = duration

	def getIllnessDuration(self):
		return self.IllnessDuration

	def run(self, env):
		while True and self.getState()!=IndividualState.Muerto:
			if self.getState() == IndividualState.Infectado_Sano:
				latency = uniform(self.MinLatencyInfection, self.MaxLatencyInfection)
				illness = geometrica(p=self.getIllnessDuration())
				
				yield env.timeout(latency)
				self.setState(IndividualState.Infectado_Enfermo)
				yield env.timeout(self.MaxIllnessPeriod if illness[0]>self.MaxIllnessPeriod else illness[0])
				
				if illness[0] > self.MaxIllnessPeriod:
					self.setState(IndividualState.Muerto)
				else:
					mutation = bernoulli(
						(self.controllerState.getIndividualInfectedHealthy()*self.mutationFactor)/self.controllerState.getIndividual()
					)
					if mutation[0] == 1:
						self.setState(IndividualState.Infectado_Sano)
					else:
						self.setState(IndividualState.Sano)
			elif self.getState() == IndividualState.Sano:
				yield env.timeout(1)
				contagion = bernoulli(
						(self.controllerState.getIndividualInfectedIll()*self.contagionFactor)/self.controllerState.getIndividual()
					)
				if contagion[0] == 1:
					self.setState(IndividualState.Infectado_Sano)


class stateController(object):
	N=0    #  Cantidad total de individuos vivos en el galpon
	S=0    #  Cantidad de individuos sanos sin virus en el galpon
	IyS=0  #  Cantidad de individuos infectados pero sanos en el galpon
	IyE=0  #  Cantidad de individuos infectados y enfermos en el galpon
	M=0    #  Cantidad de individuos muertos en el galpon
	inidividualInitial = 0 # Cantidad inicial de individuos en el galpon (STATIC VALUE)
	controlList = []
	accountingTime = 1
	
	def __init__(self, controlList, N, S, IyS, IyE, accountingTime = 1):
		self.N = N
		self.inidividualInitial = N
		self.S = S
		self.IyS = IyS
		self.IyE = IyE
		self.controlList = controlList
		self.accountingTime = accountingTime

	def setAccountingTime(self, time):
		self.accountingTime = time

	def getAccountingTime(self):
		return self.accountingTime

	def getControlList(self):
		return self.controlList
	
	def setControlList(self, clist):
		self.controlList = clist

	def getIndividual(self):
		return self.N

	def getIndividualHealthy(self):
		return self.S
	
	def getIndividualInfectedHealthy(self):
		return self.IyS

	def getIndividualInfectedIll(self):
		return self.IyE

	def accountingOperation(self):
		self.N = 0
		self.IyS = 0
		self.IyE = 0
		self.S = 0
		for bird in self.controlList:
			if bird.getState() != IndividualState.Muerto:
				self.N += 1
				if  bird.getState() == IndividualState.Infectado_Sano:
					self.IyS += 1
				elif bird.getState() == IndividualState.Infectado_Enfermo:
					self.IyE += 1
				elif bird.getState() == IndividualState.Sano:
					self.S += 1
		self.M = self.inidividualInitial - self.N

	def run(self, env):
		while(True):			
			self.accountingOperation()
			print "Dia=%d | N= %d | IyS= %d | IyE= %d | S= %d | M=%d" %(env.now, self.N, self.IyS, self.IyE, self.S, self.M)
			yield env.timeout(self.getAccountingTime())


def simulate(fileData):
	env = Environment()
	controlList = []
	controller = stateController(
		controlList, 
		int(fileData['N_Ini']), 
		int(fileData['N_Ini']) - int(fileData['I_Ini']), 
		int(fileData['I_Ini']), 0
	)
	for i in xrange(int(fileData['N_Ini'])):
		birdInstance = bird(
			fileData['N_Ini'], 
			fileData['I_Ini'],
			fileData['Min_D_Late'],
			fileData['Max_D_Late'],
			fileData['p_D_E'],
			fileData['Factor_Contagio'],
			fileData['Factor_Muta'],
			fileData['Max_D_E'],
			IndividualState.Infectado_Sano if i<int(fileData['I_Ini']) else IndividualState.Sano,
			controller
		)
		controlList.append(birdInstance)
		env.process(birdInstance.run(env))
	controller.setControlList(controlList)
	env.process(controller.run(env))
	env.run(until=fileData['D_Corr'])
