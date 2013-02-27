from org.jfree.data.xy import XYSeries, XYSeriesCollection
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart
from org.jfree.chart.renderer.xy import XYSplineRenderer, XYLine3DRenderer

def curve(data, name="", smooth=True, trid=True):
  """
  Creates a curve based on a list of (x,y) tuples.
    
  Setting *smooth* to ``True`` results in a spline renderer renderer is used.

  Setting *trid* to ``True`` results in a 3D plot. In this case the ``smooth``
  argument is ignored.
  """
    
  dataset = XYSeriesCollection()
  xy = XYSeries(name);        
  for d in data:
    xy.add(d[0], d[1])
  dataset.addSeries(xy);
  chart = ChartFactory.createXYLineChart(None, None, None, dataset, 
    PlotOrientation.VERTICAL, True, True, False)

  if smooth:
      chart.getXYPlot().setRenderer(XYSplineRenderer())
  if trid:
      chart.getXYPlot().setRenderer(XYLine3DRenderer())        
    
  return Chart(chart)    
