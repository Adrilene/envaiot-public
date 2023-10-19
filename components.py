from Configurator.configurator import Configurator
from Simulator.simulator import Simulator
from Observer.observer import Observer
from Effector.effector import Effector

configurator = Configurator()
simulator = Simulator()
observer = Observer()
effector = Effector()

from threading import Condition

condition = Condition()
