from epanettools import epanet2 as et

from Biblioteka import Epa
import numpy as np

file_name = "chojnice_kwiecien_obiekt.inp"
file_name = "siec_maly_obiekt.inp"

parameters = {
    'file_name': file_name,
    'mes_link_name': ['1'],
    'mes_node_name': ['6', '7'],
    'pumps_names': ['1'],
    'pattern_names': ['demand', 'pompka'],
    'pattern_values': [[1], [0.4]],
    'time_duration': 3600,
    'tank_names': ['7'],
    'initial_tanks': [4],
    'hydraulic_values': ['flow', '', 'head']
}

pump_input = []
tank_input = []
demand_input = []
flow_output = []
head_output = []
tank_output = []
error_output = []


ep = Epa(parameters)
ep.open_epanet()
ep.get_set_parameters()
for pump_control in np.arange(0.5, 1, 0.01):
    for tank_init in np.arange(0.1, 4.9, 0.1):
        for demand_par in np.arange(0.1, 1, 0.05):
            ep.parameter['pattern_values'] = [[demand_par], [pump_control]]
            ep.parameter['initial_tanks'] = [tank_init]
            ep.set_tank_inital()
            ep.set_patern_values()

            pump_input.append(pump_control)
            tank_input.append(tank_init)
            demand_input.append(demand_par)

            [flow, pressure, head, error, time] = ep.get_hydraulic_values()
            head_output.append(head[0][0])
            tank_output.append(head[1][0])
            flow_output.append(flow[0][0])
            error_output.append(error[0])
ep.close_epanet()




