# -*- coding: utf-8 -*-
"""Sigla_MC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KfEyA4KvB6AVArmbC9s_jZHiwD-2cJ9t
"""

from os import stat
import math
import numpy as np
import matplotlib.pyplot as plt
import torch
from graphviz import Digraph
import pdb
import sys
import random

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        if not isinstance(data, (int, float)):
          raise TypeError("data must be a scalar (int or float)")
        self.data = data
        self.grad = 0
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out

    def sigmoid(self):
        out = Value(1/(1+math.exp(-self.data)), (self,), 'sigmoid')

        def _backward():
            self.grad += (out.data * (1-out.data)) * out.grad
        out._backward = _backward

    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self): #-self
        return self * -1

    def __radd__(self, other): # other + self
        return other + self

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad}, nm={self._nm})"

class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []

class Neuron(Module):

    def __init__(self, nin, nonlin='relu'):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(0)
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum((wi*xi for wi,xi in zip(self.w, x)), self.b)
        # Applicazione della funzione di attivazione selezionata per gli strati intermedi (relu) e per l'ultimo (sigmoid)
        if self.nonlin == 'sigmoid': # Caso dell'ultimo neurone
            return act.sigmoid()
        else:
            return act.relu()  #caso default, artivazione ReLU

    def parameters(self):
        return self.w + [self.b]

    def __repr__(self):
        return f"{self.nonlin}neuron({len(self.w)})"
        #return f"{'ReLU' if self.nonlin else 'Linear'}Neuron({len(self.w)})"

class Layer(Module):

    def __init__(self, nin, nout, nonlin='relu', **kwargs):
        self.neurons = [Neuron(nin, nonlin=nonlin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
#        return out[0] if len(out) == 1 else out
        return out

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"

class MLP(Module):

    def __init__(self, nin, nouts, nonlin='relu'): # Tipo di non-linearità std per tutti i neuroni
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i+1], nonlin='sigmoid' if i == (len(nouts) -1) else nonlin) for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"