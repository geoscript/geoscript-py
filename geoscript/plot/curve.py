from org.jfree.data.xy import XYSeries, XYSeriesCollection
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart
from org.jfree.chart.renderer.xy import XYSplineRenderer, XYLine3DRenderer

def curve(data, name="", smooth=True, tridim=True):
    '''Creates a curve based on a list of (x,y) tuples.
    
    If *smooth* is true, then it uses a spline renderer.
    
    If *tridim* is true, then it creates a 3d-like plot.In this case
    smooth value is neglected and no smoothing is added'''
    dataset = XYSeriesCollection()
    xy = XYSeries(name);        
    for d in data:
        xy.add(d[0], d[1])
    dataset.addSeries(xy);
    chart = ChartFactory.createXYLineChart(
                None, None, None, dataset, PlotOrientation.VERTICAL, True, True, False)
    if smooth:
        chart.getXYPlot().setRenderer(XYSplineRenderer())
    if tridim:
        chart.getXYPlot().setRenderer(XYLine3DRenderer())        
    
    return Chart(chart)    
    