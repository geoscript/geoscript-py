import java
import unittest
from geoscript.style import Fill, Stroke
from geoscript.filter import Filter
from org.geotools.styling import PolygonSymbolizer, LineSymbolizer

class Style_Test:

  def testSimple(self):
    s = Fill('red') + Stroke('blue', 2)
    st = s._style()

    syms = st.featureTypeStyles()[0].rules()[0].symbolizers()
    assert 2 == len(syms)

    sym = syms[0]
    assert isinstance(sym, PolygonSymbolizer)
    col = sym.getFill().getColor().evaluate(None)
    assert (255,0,0) == (col.red, col.green, col.blue)

    sym = syms[1]
    assert isinstance(sym, LineSymbolizer)
    col = sym.getStroke().getColor().evaluate(None)
    assert (0,0,255) == (col.red, col.green, col.blue)
    assert 2 == sym.getStroke().getWidth().evaluate(None)

  def testZ(self):
    s = (Fill('red') + Stroke('blue')) + Fill('green').zindex(1)
    st = s._style()

    assert 2 == len(st.featureTypeStyles())
    syms = st.featureTypeStyles()[0].rules()[0].symbolizers()
    assert 2 == len(syms)

    sym = syms[0]
    assert isinstance(sym, PolygonSymbolizer)
    col = sym.getFill().getColor().evaluate(None)
    assert (255,0,0) == (col.red, col.green, col.blue)

    sym = syms[1]
    assert isinstance(sym, LineSymbolizer)
    col = sym.getStroke().getColor().evaluate(None)
    assert (0,0,255) == (col.red, col.green, col.blue)

    syms = st.featureTypeStyles()[1].rules()[0].symbolizers()
    assert 1 == len(syms)  

    sym = syms[0]
    assert isinstance(sym, PolygonSymbolizer)
    col = sym.getFill().getColor().evaluate(None)
    assert (0,128,0) == (col.red, col.green, col.blue)

  def testScale(self):
    s = (Fill('red') + Stroke('blue')).range(-1, 1000) + Fill('green').range(1000,-1)
    st = s._style()

    rules = st.featureTypeStyles()[0].rules()
    assert 2 == len(rules)

    rule = rules[0] 
    assert 1000 == rule.getMaxScaleDenominator()
    syms = rule.symbolizers()
    assert 2 == len(syms)
    assert isinstance(syms[0], PolygonSymbolizer)
    assert isinstance(syms[1], LineSymbolizer)

    rule = rules[1] 
    assert 1000 == rule.getMinScaleDenominator()
    syms = rule.symbolizers()
    assert 1 == len(syms)
    assert isinstance(syms[0], PolygonSymbolizer)

  def testFilter(self):
    s = (Fill('red') + Stroke('blue')).where("FOO = 'foo'") + Fill('green').where("BAR = 'bar'")
    st = s._style()
 
    rules = st.featureTypeStyles()[0].rules()
    assert 2 == len(rules)

    rule = rules[0] 
    assert Filter("FOO = 'foo'") == Filter(rule.getFilter()) 
    syms = rule.symbolizers()
    assert 2 == len(syms)
    assert isinstance(syms[0], PolygonSymbolizer)
    assert isinstance(syms[1], LineSymbolizer)

    rule = rules[1] 
