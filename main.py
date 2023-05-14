#from epanettools import epanet2 as et

from Biblioteka import Epa
from multiprocessing import Process
import pandas as pd
import datetime


file_name = "chojnice_kwiecien_obiekt.inp"

parameters = {
    'file_name': file_name,
    'mes_links_names': ['F1','K1','P1'],
    'mes_nodes_names': ['083','158','180'],
    'pumps_names': ['F1','K1','P1'],
    'pumps_patterns_names': ['f1','k1','p1'],
    'demand_patterns_names': ['par2','kar2'],
    'time_duration_h': 24,  # [h]
    'hydraulic_step_s': 3600,  # [h]
    'tanks_names': ['180'],
    'initial_tanks_lev': [3.58],
    'min_tanks_lev':[1.2],
    'max_tanks_lev':[5],
    'hydraulic_values': ['flow', 'energy', 'head'],
    'number_iteration':1
}

parameters['num_mes_links'] = len(parameters['mes_links_names'])
parameters['num_mes_nodes'] = len(parameters['mes_nodes_names'])
parameters['num_pumps'] = len(parameters['pumps_names'])
parameters['num_demands'] = len(parameters['demand_patterns_names'])
parameters['num_tanks'] = len(parameters['tanks_names'])
parameters['time_duration_s'] = parameters['time_duration_h']*3600#[s]

ep = Epa(parameters)

t = datetime.datetime.now()
ep.get_data()
#print(datetime.datetime.now()-t)

keis = ['tank_output_180','tank_input_180', 'pump_input_F1', 'pump_input_K1', 'pump_input_P1', 'demand_input_par2', 'demand_input_kar2']


'''for ke in keis:
    print(ke,ep.data[ke])'''


for key in ep.data.keys():
    temp=[]
   # try:
    if type(ep.data[key][0]) != list:
        temp = ep.data[key]
    else:
        for i in range(parameters['number_iteration']):
            temp += ep.data[key][i]
    ep.data[key] = temp
    print(len(ep.data[key]))

#for key in ep.data.keys():
#    print(key,ep.data[key])


'''df = pd.DataFrame(ep.data)
df = df.reset_index(drop = True)
df.to_csv('dane_do_uczenia_'+str(parameters['number_iteration'])+'.csv',decimal =',',sep=';')
'''