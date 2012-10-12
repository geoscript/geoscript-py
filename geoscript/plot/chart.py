from javax import swing
from org.jfree.chart import ChartPanel, ChartUtilities
from org.jfree.chart.plot import DatasetRenderingOrder
from org.jfree.chart.axis import NumberAxis
from geoscript import util

class Chart(object):
    """
    A class that wraps a JFreeChart Chart object and has method
    to easily show or save it
    """
    
    def __init__(self,chart):
        self.chart = chart
        self.datasets = 1
        
    def show(self, size=(500,500)):
        panel = ChartPanel(self.chart) 
        frame = swing.JFrame()
        frame.setContentPane(panel)
        frame.size = size
        frame.visible = True
        
    def savepng(self, filename, size=(500,500)):
        ChartUtilities.saveChartAsPNG(util.toFile(filename), self.chart, size[0], size[1])
    
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
