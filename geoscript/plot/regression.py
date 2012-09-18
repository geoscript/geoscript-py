from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.chart.renderer.xy import  XYLineAndShapeRenderer
from java.awt import Color
from org.jfree.chart import  JFreeChart
from org.jfree.chart.plot import XYPlot
from org.jfree.chart.axis import NumberAxis
import itertools
from org.jfree.data.statistics import Regression
from org.jfree.data.general import DatasetUtilities
from org.jfree.data.function import LineFunction2D, PowerFunction2D
from geoscript.plot.chart import Chart

def linearregression(X, Y):
    return regression(X, Y, 0)

def powregression(X, Y):
    return regression(X, Y, 1)


def regression(X,Y, regtype = 0):
    
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
      
    if regtype == 1:
        coefficients = Regression.getPowerRegression(dataset, 0)
        curve = PowerFunction2D(coefficients[0], coefficients[1])
        regdesc = "Power Regression"    
    else:
        coefficients = Regression.getOLSRegression(dataset, 0)   
        curve = LineFunction2D(coefficients[0], coefficients[1])
        regdesc = "Linear Regression"   
    
    regressionData = DatasetUtilities.sampleFunction2D(curve,   
                xmin, xmax, 100, "Fitted Regression Line")   
           
    plot.setDataset(1, regressionData)   
    renderer2 = XYLineAndShapeRenderer(True, False);   
    renderer2.setSeriesPaint(0, Color.blue)   
    plot.setRenderer(1, renderer2)
           
    jfchart = JFreeChart(regdesc, JFreeChart.DEFAULT_TITLE_FONT, plot, True);
    
    chart = Chart(jfchart)          
    chart.coeffs = coefficients
    
    return chart
    