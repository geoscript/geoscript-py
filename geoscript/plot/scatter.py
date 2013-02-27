from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.chart import  ChartFactory
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart.axis import NumberAxis
import itertools
from geoscript.plot.chart import Chart
from org.jfree.util import ShapeUtilities

def scatterplot(data, name="", xlabel="", ylabel="", size= 3):
  """
  Creates a scatter plot from x,y data.

  *data* is a list of (x,y) tuples.
  """
    
  xAxis = NumberAxis(xlabel)   
  xAxis.setAutoRangeIncludesZero(False)   
  yAxis = NumberAxis(ylabel)   
  yAxis.setAutoRangeIncludesZero(False)   
   
  series = XYSeries("Values");     
  for (i,j) in data:         
    series.add(i, j)

  dataset = XYSeriesCollection()
  dataset.addSeries(series);
  chart = ChartFactory.createScatterPlot(name, xlabel, ylabel, dataset, 
    PlotOrientation.VERTICAL, True, True, False)    
  plot = chart.getPlot()
  plot.getRenderer().setSeriesShape(0, 
    ShapeUtilities.createRegularCross(size,size));                  
    
  return Chart(chart)
    
