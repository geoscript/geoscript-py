from org.jfree.data.general import DefaultPieDataset
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart

def pie(data):
    dataset = DefaultPieDataset();    
    for k,v in data.iteritems():        
        dataset.setValue(k, v) 
    chart = ChartFactory.createPieChart("",dataset, True, True, False)
    return Chart(chart)