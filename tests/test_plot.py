import unittest, threading, time
from random import randint
from geoscript import plot

class Worker(threading.Thread):

 def __init__(self, chart):
   threading.Thread.__init__(self)
   self.chart = chart

 def run(self):
   self.chart.show()

 def dispose(self):
   self.chart.dispose()

def render(chart):
  from java.lang import System 
  if not System.getProperty("java.awt.headless"):
    w = Worker(chart)
    w.start()
    time.sleep(2)
    w.dispose()

def randoms(n=100):
  return [randint(0,100) for x in range(n)]

cats = ['foo', 'bar', 'baz', 'bam', 'bom']

def catdata():
  return dict(zip(cats, randoms(len(cats)))) 

def testBarXY():
  render(plot.bar.xy(zip(randoms(), randoms())))
  
def testBarCategory():
  render(plot.bar.category(catdata()))
  render(plot.bar.category({'one': catdata(), 'two': catdata()}))

def testPie():
  render(plot.pie(catdata()))

def testRegression():
  render(plot.regression.linear(zip(randoms(), randoms())))
  render(plot.regression.power(zip(randoms(), randoms())))

def testScatter():
  render(plot.scatterplot(zip(randoms(),randoms())))

def testBox():
  render(plot.box(dict(zip(cats, [randoms() for i in range(len(cats))]))))
