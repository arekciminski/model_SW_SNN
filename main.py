#from epanettools import epanet2 as et

from Biblioteka import Epa
from multiprocessing import Process
import pandas as pd
import time

file_name = "chojnice_kwiecien_obiekt.inp"

parameters = {
    'file_name': file_name,
    'mes_links_names': ['F1','K1','P1'],
    'mes_nodes_names': ['083','158','180'],
    'pumps_names': ['F1','K1','P1'],
    'pumps_patterns': ['f1','k1','p1'],
    'demand_patterns': ['par2','kar2'],
    'pumps_pattern_values': [[0.8],[0.8],[0.8]],
    'demand_pattern_values': [[0.7],[0.7],[0.7]],
    'time_duration': 3600,
    'tanks_names': ['180'],
    'initial_tanks_lev': [3.58],
    'min_tanks_lev':[0.5],
    'max_tanks_lev':[5],
    'hydraulic_values': ['flow', 'energy', 'head'],
    'number_iteration':1_000_000
}

parameters['num_mes_links'] = len(parameters['mes_links_names'])
parameters['num_mes_nodes'] = len(parameters['mes_nodes_names'])
parameters['num_pumps'] = len(parameters['pumps_names'])
parameters['num_demands'] = len(parameters['demand_patterns'])
parameters['num_tanks'] = len(parameters['tanks_names'])


ep = Epa(parameters)

t = time.process_time()
ep.get_data()
print(time.process_time() - t)

'''t = time.process_time()
p = Process(target = ep.get_data())
p.start()
p.join()
print(time.process_time() - t)'''


'''#print(ep.data.keys())
for key in ep.data.keys():
    print(key, ep.data[key])'''


df = pd.DataFrame(ep.data)
df = df.reset_index(drop = True)
df.to_csv('dane_do_uczenia_'+str(parameters['number_iteration'])+'.csv',decimal =',',sep=';')
#print(df)


