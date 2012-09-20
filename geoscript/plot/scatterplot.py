from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.chart import  ChartFactory
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart.axis import NumberAxis
import itertools
from geoscript.plot.chart import Chart
from org.jfree.util import ShapeUtilities

def scatterplot(X,Y=None, name="", xlab="", ylab="", size= 3):
    '''creates a scatterplot from x and y data.
    Data can be passed as a list of (x,y) tuples or two lists with
    x and y values'''
    
    xAxis = NumberAxis(xlab)   
    xAxis.setAutoRangeIncludesZero(False)   
    yAxis = NumberAxis(ylab)   
    yAxis.setAutoRangeIncludesZero(False)   
   
    series = XYSeries("Values");     
    if Y is not None:
        iterable = itertools.izip(X, Y)
    else:
        iterable = X       
    for (x,y) in iterable:
        series.add(x, y);
            
    dataset = XYSeriesCollection()
    dataset.addSeries(series);
    chart = ChartFactory.createScatterPlot(name, xlab, ylab, dataset,\
                                           PlotOrientation.VERTICAL, True, True, False)    
    plot = chart.getPlot()
    plot.getRenderer().setSeriesShape(0, ShapeUtilities.createRegularCross(size,size));                  
    
    return Chart(chart)
    