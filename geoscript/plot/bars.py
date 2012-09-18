from org.jfree.data.xy import XYSeriesCollection, XYSeries
from org.jfree.data.category import DefaultCategoryDataset
from org.jfree.chart import ChartFactory
from org.jfree.chart.plot import PlotOrientation
from geoscript.plot.chart import Chart

def xybars(data, name="xybars"):
    series = XYSeries(name);
    for x,y in data:
        series.add(x,y)
    dataset =  XYSeriesCollection(series)
    chart = ChartFactory.createXYBarChart(None, "X", False,"Y", 
            dataset, PlotOrientation.VERTICAL, True, True, False)
    return Chart(chart)

def categorybars(cat):
    dataset = DefaultCategoryDataset();
    for c in cat:
        dataset.addValue() 
#===============================================================================
# 
# dataset.addValue(18, taxi1,dia1); 
# dataset.addValue(15, taxi1,dia2); 
# dataset.addValue(16, taxi1,dia3); 
# dataset.addValue(12, taxi1,dia4);
# dataset.addValue(16, taxi2,dia1); 
# dataset.addValue(19, taxi2,dia2); 
# dataset.addValue(10, taxi2,dia3); 
# dataset.addValue(11, taxi2,dia4);
# JFreeChart graficoBarras = ChartFactory.createBarChart( 
#         "Uso de los Taxis",        //Título de la gráfica 
#         "Días de labor",           //leyenda Eje horizontal 
#         "Número de carreras",      //leyenda Eje vertical 
#         dataset,                   //datos 
#         PlotOrientation.VERTICAL,  //orientación 
#         true,                      //incluir leyendas 
#         true,                      //mostrar tooltips 
#         true);                   
# graficoBarras.setBackgroundPaint(Color.LIGHT_GRAY);
# CategoryPlot plot =(CategoryPlot) graficoBarras.getPlot(); 
# plot.setBackgroundPaint(Color.CYAN); //fondo del grafico 
# plot.setDomainGridlinesVisible(true);//lineas de rangos, visibles 
# plot.setRangeGridlinePaint(Color.BLACK);//color de las lineas de rangos
# mostrarGrafico(graficoBarras,"Gráfico de barras");
#===============================================================================