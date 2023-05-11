from epanettools import epanet2 as et
import matplotlib.pyplot as plt
#from GA import solve

ret=et.ENopen("siec_maly_obiekt.inp","Net3.rpt","")
ret=et.ENopen("chojnice_kwiecien_obiekt.inp","Net3.rpt","")
et.ENopenH()
et.ENinitH(0)
time = []
nodes=[]
pres=[]
head=[]

ret,nnodes=et.ENgetcount(et.EN_NODECOUNT)
ret,npipes=et.ENgetcount(et.EN_NODECOUNT)
nodes=[]
links=[]
pres=[]
flow =[]
time=[]
for index in range(1,nnodes):
     ret,t=et.ENgetnodeid(index)
     nodes.append(t)
     t=[]
     pres.append(t)
     head.append(t)
#print (nodes)

for index in range(1,npipes):
     ret,t=et.ENgetlinkid(index)
     links.append(t)
     t=[]
     flow.append(t)
#print (links)

while True :
    ret,t=et.ENrunH()
    time.append(t)
    # Retrieve hydraulic results for time t
    for  i in range(0,len(links)):
        ret,p=et.ENgetlinkvalue(i+1, et.EN_FLOW)
        flow[i].append(p)
    for  i in range(0,len(nodes)):
        ret,p=et.ENgetnodevalue(i+1, et.EN_PRESSURE)
        pres[i].append(p)

        ret,p=et.ENgetnodevalue(i+1, et.EN_HEAD)
        head[i].append(p)
    ret,tstep=et.ENnextH()
    if (tstep<=0):
        break
ret=et.ENcloseH()

fig,ax=plt.subplots()
plt.plot(1)
for i in range(0,len(pres)-1):
    ax.plot(range(0,len(pres[i])),pres[i],label=nodes[i])
ax.legend()
plt.show()

fig,ax=plt.subplots()
plt.plot(2)
for i in range(0,len(head)-1):
    ax.plot(range(0,len(head[i])),head[i],label=nodes[i])
ax.legend()
plt.show()

fig,ax=plt.subplots()
plt.plot(3)
for i in range(0,len(flow)-1):
    ax.plot(range(0,len(flow[i])),flow[i],label=links[i])
ax.legend()
plt.show()