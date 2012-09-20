from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.data.category import DefaultCategoryDataset
from org.jfree.chart import ChartFactory
from org.jfree.chart.plot import PlotOrientation
from geoscript.plot.chart import Chart

def xybars(data, name="xybars"):
    '''Creates a xy bars chart. 
    
    Input is a list of tuples with (x,y) values'''
    series = XYSeries(name);
    for x,y in data:
        series.add(x,y)
    dataset =  XYSeriesCollection(series)
    chart = ChartFactory.createXYBarChart(None, "X", False,"Y", 
            dataset, PlotOrientation.VERTICAL, True, True, False)
    return Chart(chart)

def intervalbars(data, name="xybars"):
    '''Creates a xy bars chart, whit bars defining intervals. 
    Input is a list of tuples in the form ((lo,hi),y), *lo* and *hi* being
    the lower and upper limits of the interval and *y* the count on that interval'''
    pass

def categorybars(cat, name="", xlab="", ylab="", stacked=False, tridim=False):
    '''Creates a barchart with categorical data.
    
    The input is a dict with category names as keys and numerical values
    (the height of the bar) corresponding to that category as values.
    
    Multiple series can be plot, by passing a dict with series names as keys
    and dicts as the one described above as values.
    
    By setting *stacked* to true the result will be a stacked bar chart''' 
    dataset = DefaultCategoryDataset();
    for k,v in cat.iteritems():    
        if isinstance(v, dict):
            for k2,v2 in v.iteritems():
                dataset.addValue(v2, k2, k)    
        else:
            dataset.addValue(v, "", k) 
 
    if tridim:
        if stacked:
            chart = ChartFactory.createStackedBarChart3D(name, xlab, ylab, dataset,
                                           PlotOrientation.VERTICAL, True, True, True)
        else:
            chart = ChartFactory.createBarChart3D(name, xlab, ylab, dataset,
                                           PlotOrientation.VERTICAL, True, True, True) 
    else:
        if stacked:
            chart = ChartFactory.createStackedBarChart(name, xlab, ylab, dataset,
                                           PlotOrientation.VERTICAL, True, True, True)
        else:
            chart = ChartFactory.createBarChart(name, xlab, ylab, dataset,
                                           PlotOrientation.VERTICAL, True, True, True)
    return Chart(chart)