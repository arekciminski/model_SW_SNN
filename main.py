from epanettools import epanet2 as et

from Biblioteka import Epa
import numpy as np
import pandas as pd

file_name = "chojnice_kwiecien_obiekt.inp"
file_name = "siec_maly_obiekt.inp"

parameters = {
    'file_name': file_name,
    'mes_links_names': ['1'],
    'mes_nodes_names': ['5','6','7'],
    'pumps_names': ['1'],
    'pumps_patterns': ['pompka'],
    'demand_patterns': ['demand'],
    'pumps_pattern_values': [[0.3]],
    'demand_pattern_values': [[0.7]],
    'time_duration': 3600,
    'tanks_names': ['7'],
    'initial_tanks': [4],
    'hydraulic_values': ['flow', '', 'head']
}

parameters['num_mes_links'] = len(['1'])
parameters['num_mes_nodes'] = len(['5','6'])
parameters['num_pumps'] = len(['1'])
parameters['num_demands'] = len(['demand'])
parameters['num_tanks'] = len(['7'])


ep = Epa(parameters)


ep.prepare_empty_dict_to_comput()

ep.open_epanet()
ep.get_set_parameters()
for pump_control in np.arange(0.5, 1, 0.01):
    for tank_init in np.arange(0.1, 4.9, 0.1):
        for demand_par in np.arange(0.1, 1, 0.05):
            ep.parameters['demand_pattern_values'] = [[demand_par]]
            ep.parameters['pumps_pattern_values'] = [[pump_control]]
            ep.parameters['initial_tanks'] = [tank_init]
            ep.set_tank_inital()
            ep.set_patern_values()

            ep.data['pump_input_pompka'].append(pump_control)
            ep.data['tank_input_7'].append(tank_init)
            ep.data['demand_input_demand'].append(demand_par)

            [flow, pressure, head, error, time] = ep.get_hydraulic_values()

            for i in range(0,ep.parameters['num_mes_nodes']-ep.parameters['num_tanks']):
                ep.data['head_output_'+ep.parameters['mes_nodes_names'][i]].append(head[i][0])

            for i in range(ep.parameters['num_mes_nodes']-ep.parameters['num_tanks'],ep.parameters['num_mes_nodes']):
                ep.data['tank_output_'+ep.parameters['tanks_names'][ep.parameters['num_mes_nodes']-i-1]].append(head[i][0])

            for i in range(ep.parameters['num_mes_links']):
                ep.data['flow_output_'+ep.parameters['mes_links_names'][i]].append(flow[i][0])


#            ep.data['error_output'].append(error[0])
ep.close_epanet()

#print(ep.data.keys())
print(len(ep.data['tank_output_7']))
print(len(ep.data['tank_output_7']))

df = pd.DataFrame(ep.data)
#df.to_csv('dane_do_uczenia.csv',decimal =',',sep=';')
#print(df)


