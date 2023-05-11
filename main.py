from epanettools import epanet2 as et

from Biblioteka import Epa
import matplotlib.pyplot as plt
#from GA import solve

print([[0]]*5)

file_name = "chojnice_kwiecien_obiekt.inp"
file_name = "siec_maly_obiekt.inp"

parameters = {
    'file_name' : "siec_maly_obiekt.inp",
    'mes_link_name' :['1','2'],
    'mes_node_name':['1','2','7'],
    'pumps_names' : ['pompka'],
    'pattern_names' :['demand','pompka'],
    'pattern_values' : [[0.3],[0.7331]],
    'time_duration': 3600,
    'tank_names': ['7'],
    'initial_tanks' : [2],
    'hydrailic_values' :['flow', 'pressure', 'head']}


ep = Epa(file_name)
ep.open_epanet()
#print(ep.get_link_number(pumps_names))
(ep.get_node_number(mes_node_name))
(ep.get_patern_number(pat_name))
[flow,pressure,head,error,time]=ep.get_hydraulic_values(['flow','pressure','head'])
ep.close_epanet()

print(error)




