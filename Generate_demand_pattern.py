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

min_dem=[]
max_dem=[]
for i in range(24):
    min_dem.append(min(temp_dem[i]))
    max_dem.append(max(temp_dem[i]))

for i in range(int(len(plac)/24)):
    ax.step(range(0,24),dem[i],'k')
ax.step(range(0, 24), min_dem, 'r--')
ax.step(range(0, 24), max_dem, 'r--')
plt.show()