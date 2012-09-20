from org.jfree.data.general import DefaultPieDataset
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart

def pie(data, name="", tridim=False):
    dataset = DefaultPieDataset();    
    for k,v in data.iteritems():        
        dataset.setValue(k, v) 
    if tridim:
        chart = ChartFactory.createPieChart3D(name,dataset, True, True, False)
    else:
        chart = ChartFactory.createPieChart(name,dataset, True, True, False)
    return Chart(chart)