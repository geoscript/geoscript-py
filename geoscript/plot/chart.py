from javax import swing
from org.jfree.chart import ChartPanel, ChartUtilities
from geoscript import util

class Chart():
    
    def __init__(self,chart):
        self.chart = chart
        
    def show(self, size=(500,500)):
        panel = ChartPanel(self.chart) 
        frame = swing.JFrame()
        frame.setContentPane(panel)
        frame.size = size
        frame.visible = True
        
    def savepng(self, filename, size=(500,500)):
        ChartUtilities.saveChartAsPNG(util.toFile(filename), self.chart, size[0], size[1])