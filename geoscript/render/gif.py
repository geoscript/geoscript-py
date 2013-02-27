import jarray
from java.io import ByteArrayInputStream, ByteArrayOutputStream
from javax.imageio import ImageIO, ImageWriteParam, ImageTypeSpecifier, IIOImage
from javax.imageio.metadata import IIOMetadataNode
from geoscript import util
from geoscript.render.image import Image

class GIF(Image):
   """
   Renderer that produces a GIF image.
   """

   def __init__(self):
     Image.__init__(self, 'gif')

   @staticmethod 
   def animated(images, file=None, delay=300, loop=False):
     """
     Generates an anmiated GIF. 

     The *images* parameter is a sequence of objects that can be read as 
     GIF images, such as an array of bytes.

     The *file* parameter specifies the file to generate. When omitted the 
     resulting animated GIF is returned from this function as an array byte. 

     The *delay* specifies the frame rate in milliseconds. 

     The *loop* parameter specifies whether the animated GIF should loop 
     continously.
     """
     from com.sun.media.imageioimpl.plugins.gif import GIFImageWriter
     from com.sun.media.imageioimpl.plugins.gif import GIFImageWriterSpi

     out = ByteArrayOutputStream() if file is None else util.toFile(file)
     ios = ImageIO.createImageOutputStream(out)
     w = GIFImageWriter(GIFImageWriterSpi())
     w.setOutput(ios)
     w.prepareWriteSequence(None)

     wp = w.getDefaultWriteParam()
     wp.setCompressionMode(ImageWriteParam.MODE_EXPLICIT)
     wp.setCompressionType('LZW')
     wp.setCompressionQuality(0.75)

     for img in images:   
       iis = ImageIO.createImageInputStream(util.toInputStream(img))
       ri = ImageIO.read(iis)

       md = w.getDefaultImageMetadata(ImageTypeSpecifier(ri),wp)
       t = IIOMetadataTree(md)
       t.set('GraphicControlExtension', delayTime=delay/10)
       if loop is True:
         n = t.set('ApplicationExtensions', 'ApplicationExtension', 
           applicationID='NETSCAPE', authenticationCode='2.0')
         n.setUserObject(jarray.array([0x1,0, 0], 'b'))
       t.commit()

       w.writeToSequence(IIOImage(ri, None, md), wp)

     w.endWriteSequence()
     ios.flush()
     ios.close()

     if file is None:
       return out.toByteArray()

class IIOMetadataTree(object):
   def __init__(self, md):
     self.md = md
     self.root = md.getAsTree(md.getNativeMetadataFormatName())

   def set(self, *path, **atts):
     n = self.find(self.root, *path)
     for k,v in atts.iteritems():
       n.setAttribute(k, str(v))

     return n

   def find(self, node, *path):
     for p in path:
       node = self.child(node, p)
     return node

   def child(self, node, name):
     for i in range(node.getLength()):
       n = node.item(i)
       if n.getNodeName().lower() == name.lower():
         return n
       
     n = IIOMetadataNode(name)  
     node.appendChild(n)
     return n

   def commit(self):
     self.md.setFromTree(self.md.getNativeMetadataFormatName(), self.root)

   def dump(self):
     from org.geotools.coverage.grid.io.imageio import IIOMetadataDumper
     dumper = IIOMetadataDumper(self.root)
     return dumper.getMetadata()
  
