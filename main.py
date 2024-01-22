from BasicMonitoring import VizualizeMonitoring,Monitoring
import random

monitoring_list=[]
for  i in range(4):
  if (i%2)==0:
    mon_obj = VizualizeMonitoring([],[])
  else:
    mon_obj = Monitoring([],[])
  mon_obj.monitor_cpu(int(8))
  mon_obj.monitor_ram(int(8))
  monitoring_list.append(mon_obj)

for obj in monitoring_list:
  print("the type is: "+ str(type(obj)))
  obj()