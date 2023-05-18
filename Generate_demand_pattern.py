import seaborn as sns
import matplotlib.pyplot as plt
def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    temp = []
    for l in lines:
        if l != '\n' and l!='EPANET Pattern Data\n':
           temp.append(float(l))
    return temp

def save_file(file_name,data):
    f= open(file_name,'w')
    for i in range(len(data[0])):
        f.write(str(i)+';'+str(data[0][i])+';'+str(data[1][i])+'\n')
    f.close()

file_name = 'plac2.pat'

plac = read_file(file_name)

fig,ax = plt.subplots()

dem = []
for i in range(int(len(plac)/24)):
    dem.append(plac[i * 24:(i + 1) * 24])

temp_dem = []
for i in range(24):
    temp=[]
    for j in range(30):
        temp.append(plac[i+j*24])
    temp_dem.append(temp)

min_max_dem=[[],[]]
for i in range(24):
    min_max_dem[0].append(min(temp_dem[i]))
    min_max_dem[1].append(max(temp_dem[i]))

'''for i in range(int(len(plac)/24)):
    ax.step(range(0,24),dem[i],'k')
ax.step(range(0, 24), min_dem, 'r--')
ax.step(range(0, 24), max_dem, 'r--')
plt.show()'''

save_file('pattern_bounds.csv',min_max_dem)
