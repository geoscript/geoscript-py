from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.chart.renderer.xy import  XYLineAndShapeRenderer
from org.jfree.chart import  JFreeChart
from org.jfree.chart.plot import XYPlot
from org.jfree.chart.axis import NumberAxis
import itertools
from geoscript.plot.chart import Chart

def scatterplot(X,Y):
    
    xAxis = NumberAxis("X")   
    xAxis.setAutoRangeIncludesZero(False)   
    yAxis = NumberAxis("Y")   
    yAxis.setAutoRangeIncludesZero(False)   
   
    series = XYSeries("Values"); 
    xmax = xmin = None       
    for (x,y) in itertools.izip(X, Y):
        series.add(x, y);
        if xmax is None:
            xmax = xmin = x
        else:
            xmax = max(xmax, x)
            xmin = min(xmin, x)
            
    dataset = XYSeriesCollection()
    dataset.addSeries(series);
    renderer1 = XYLineAndShapeRenderer(False, True)
    plot = XYPlot(dataset, xAxis, yAxis, renderer1)   
                  
    jfchart = JFreeChart("Scatterplot", JFreeChart.DEFAULT_TITLE_FONT, plot, True);
    
    chart = Chart(jfchart)          
        
    return chart
    