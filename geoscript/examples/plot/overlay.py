from geoscript.plot import *
import random

'''An example that shows how plots can be overlayed'''

if __name__ == '__main__':          
    xy = [(i,random.random() * 10) for i in range(10)]    
    chart = curve(xy)
    xy2 = [(i,random.random() * 3) for i in range(10)]    
    chart2 = curve(xy2)
    xy3 = [(i,random.random()) for i in range(10)]    
    chart3 = curve(xy3)
    xy4 = [(random.random() * 10,random.random() * 10) for i in range(100)]    
    chart4 = scatterplot(xy4)
    chart.overlay(chart2, chart3, chart4)
    chart.show()
        