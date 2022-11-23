from imports import *

class modelConfig:
  def __init__(self, config, model):
    self.model=[]
    self.listaConfig=config
    self.model = [model]


    

    def add(self, layer):
      self.model.append(layer)

