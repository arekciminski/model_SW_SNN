from epanettools import epanet2 as et

from Biblioteka import Epa
import matplotlib.pyplot as plt
#from GA import solve

print([[0]]*5)

file_name = "chojnice_kwiecien_obiekt.inp"
file_name = "siec_maly_obiekt.inp"

mes_link_name =['1','2']
mes_node_name =['1','2']
#pumps_names = ['F1','K1','P1']
pat_name =['demand','pompka']
ep = Epa(file_name)
ep.open_epanet()
print(ep.get_number_of_links())
print(ep.get_number_of_nodes())
print(ep.get_link_number(mes_link_name))
#print(ep.get_link_number(pumps_names))
print(ep.get_node_number(mes_node_name))
print(ep.get_patern_number(pat_name))
[flow,pressure,head,error,time]=ep.get_hydraulic_values(['flow','pressure','head'])
ep.close_epanet()

print(len(flow[0]),len(error)*3)




