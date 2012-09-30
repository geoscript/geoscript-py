from org.jfree.data.statistics import DefaultBoxAndWhiskerCategoryDataset
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart

def box(data):
    '''creates a box and whiskers plot.
    Data is passed as a dict with category names as keys and lists of numbers as values
    '''
    dataset  = DefaultBoxAndWhiskerCategoryDataset()
    for name, values in data.iteritems():    
        dataset.add(values, "", name);
    chart = ChartFactory.createBoxAndWhiskerChart("", "", "", dataset, True)
    return Chart(chart)
        
            
            