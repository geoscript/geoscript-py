from javax import swing
from org.geotools.renderer.chart import GeometryDataset, GeometryRenderer
from org.jfree.chart import JFreeChart, ChartPanel
from org.jfree.chart.plot import XYPlot

def plot(geoms, size=(500,500)):
  """
  Plots a set of geometry objects into a xy grid.

  *geom* is a `list` of geometry objects to plot. *size* is the resulting
  size of the rendered plot.
  """

  if not isinstance(geoms, list):
    geoms = [geoms]

  data = GeometryDataset(geoms)
  r = GeometryRenderer()
  #r.setFillPolygons(True)

  plot = XYPlot(data, data.getDomain(), data.getRange(), r);
  chart = JFreeChart(plot)
  panel = ChartPanel(chart)
  
  frame = swing.JFrame()
  frame.setContentPane(panel)
  frame.size = size
  frame.visible = True
