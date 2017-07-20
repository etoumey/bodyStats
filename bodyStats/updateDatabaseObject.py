


class GCData:
  dowData = []
  data = []



# rhr class
class rhr(GCData):
  
  def printInfo(self):
    print self.dowData

# sleep class
class sleep(GCData):



rhrUpdate = rhr()
for i in range(0,5):
  rhrUpdate.dowData.append(i) 

print rhrUpdate.dowData
print '\n\n'

rhrUpdate.printInfo()
