from org.jfree.data.statistics import DefaultBoxAndWhiskerCategoryDataset
from org.jfree.chart import ChartFactory
from geoscript.plot.chart import Chart

def box(data):
  """
  Creates a box and whiskers plot.

  *data* is a ``dict`` whose keys are category names and values are list of
  numeric values.
  """
  dataset  = DefaultBoxAndWhiskerCategoryDataset()
  for name, values in data.iteritems():    
    dataset.add(values, "", name);
  chart = ChartFactory.createBoxAndWhiskerChart("", "", "", dataset, True)
  return Chart(chart)
