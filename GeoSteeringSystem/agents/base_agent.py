#!/usr/bin/python
# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def execute(self, context):
        pass