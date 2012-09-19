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

def categorybars(cat):
    '''creates a barchart with categorical data.
    The input is a dict with category names as keys and values
    (the height of the bar= corresponding to that category''' 
    dataset = DefaultCategoryDataset();
    for k,v in cat.iteritems():        
        dataset.addValue(v, "", k) 
 
    chart = ChartFactory.createBarChart( 
        "",         
        "Categories",            
        "Values",       
        dataset,   
        PlotOrientation.VERTICAL,  
        True,                      
        True,                     
        True);                   
    return Chart(chart)