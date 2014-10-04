from java.lang import String
from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.data.category import DefaultCategoryDataset
from org.jfree.chart import ChartFactory
from org.jfree.chart.plot import PlotOrientation
from geoscript.plot.chart import Chart

def xy(data, name='', xlabel='', ylabel=''):
  """
  Creates a xy bar chart.         

  *data* is a list of (x,y) tuples
  """        
  series = XYSeries(name);
  for x,y in data:
    series.add(x,y)

  dataset =  XYSeriesCollection(series)
  if len(data) > 1:
    # hack to set interval width
    x0, x1 = data[0][0], data[1][0]
    if x1 > x0:
        w = x1 - x0
    else:
        w = x0 - x1
    dataset.setIntervalWidth(w)

  chart = ChartFactory.createXYBarChart(None, xlabel, False, ylabel, dataset,
    PlotOrientation.VERTICAL, True, True, False)
  return Chart(chart)

def category(data, name='', xlabel='', ylabel='', stacked=False, trid=False):
  """
  Creates a category bar chart.
    
  *data* is a ``dict`` whose keys are category names and whose values are 
  numerical (the height of the bar). 

  To plot multiple series *data* is specified as a ``dict`` whose keys are 
  series names and values are a ``dict`` of category names to numerical values.

  Setting *stacked* to ``True`` results in a stacked bar char. Setting *trid*
  to ``True`` results in a 3D bar chart.
  """ 
  dataset = DefaultCategoryDataset();
  for k,v in data.iteritems():    
    if isinstance(v, dict):
      for k2,v2 in v.iteritems():
        dataset.addValue(v2, k2, k)    
    else:
      dataset.addValue(v, "", k) 
 
  if trid:
    if stacked:
      chart = ChartFactory.createStackedBarChart3D(name, xlabel, ylabel, 
        dataset, PlotOrientation.VERTICAL, True, True, True)
    else:
      chart = ChartFactory.createBarChart3D(name, xlabel, ylabel, dataset, 
        PlotOrientation.VERTICAL, True, True, True) 
  else:
    if stacked:
      chart = ChartFactory.createStackedBarChart(name, xlabel, ylabel, dataset,
        PlotOrientation.VERTICAL, True, True, True)
    else:
      chart = ChartFactory.createBarChart(name, xlabel, ylabel, dataset, 
        PlotOrientation.VERTICAL, True, True, True)
  return Chart(chart)
