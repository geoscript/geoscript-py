from javax import swing
from org.jfree.chart import ChartPanel, ChartUtilities
from org.jfree.chart.plot import DatasetRenderingOrder
from org.jfree.chart.axis import NumberAxis
from geoscript import util

class Chart(object):
  """
  Chart backed by a JFreeChart chart object.
  """
    
  def __init__(self, chart):
    self.chart = chart
    self.datasets = 1
        
  def show(self, size=(500,500)):
    panel = ChartPanel(self.chart) 

    def onclose(e):
      e.getWindow().dispose()
      self.dispose()

    frame = swing.JFrame(windowClosing=onclose)
    frame.setContentPane(panel)
    frame.size = size
    frame.visible = True
    self.frame = frame
        
  def dispose(self):
    if self.frame is not None:
      self.frame.dispose()
    self.frame = None
     
  def savepng(self, filename, size=(500,500)):
    ChartUtilities.saveChartAsPNG(util.toFile(filename), self.chart, *size)
    
  def overlay(self, *charts):
    for chart in charts:
      self._overlay(chart)
            
  def _overlay(self, chart):        
    plot = self.chart.getPlot()
    plot.setDataset(self.datasets, chart.chart.getPlot().getDataset())
    plot.setRenderer(self.datasets, chart.chart.getPlot().getRenderer())
    plot.setDatasetRenderingOrder(DatasetRenderingOrder.FORWARD)

    yAxis = NumberAxis("") 
    plot.setRangeAxis(self.datasets, yAxis); 
    plot.mapDatasetToRangeAxis(self.datasets, self.datasets)
    self.datasets += 1
