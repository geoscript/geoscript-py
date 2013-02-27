from org.jfree.data.general import DefaultPieDataset
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart

def pie(data, name='', trid=False):
  """
  Creates a pie chart.

  *data* is a ``dict`` whose keys are category names and values are numeric 
  values.
  
  Setting *trid* to ``True`` results in a 3D char.
  """        
  dataset = DefaultPieDataset();    
  for k,v in data.iteritems():        
    dataset.setValue(k, v) 
  if trid:
    chart = ChartFactory.createPieChart3D(name, dataset, True, True, False)
  else:
    chart = ChartFactory.createPieChart(name, dataset, True, True, False)
  return Chart(chart)
