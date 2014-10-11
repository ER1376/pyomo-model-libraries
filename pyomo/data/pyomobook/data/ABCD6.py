import pyomo.modeling
from pyomo.core import *

model = AbstractModel()

model.Z = Set(dimen=3)
model.D = Param(model.Z)

instance = model.create('ABCD6.dat')

print('Z '+str(sorted(list(instance.Z.data()))))
print('D')
for key in sorted(instance.D.keys()):
    print(cname(instance.D,key)+" "+str(value(instance.D[key])))