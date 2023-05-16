from epanettools import epanet2 as et
from tqdm import tqdm
import numpy as np
import random

class Epa:

    def __init__(self, parameters):
        self.parameters = parameters
        self.random={}

    def open_epanet(self):
        ret = et.ENopen(self.parameters['file_name'], "Net3.rpt", "")

    def close_epanet(self):
        ret = et.ENclose()

    def get_number_of_nodes(self):
        ret, nnodes = et.ENgetcount(et.EN_NODECOUNT)
        self.nnodes = nnodes
        return nnodes

    def get_number_of_links(self):
        ret, nlinks = et.ENgetcount(et.EN_LINKCOUNT)
        self.nlinks = nlinks
        return nlinks

    def get_link_index(self):
        link_index=[]
        for ln in self.parameters['mes_links_names']:
            ret, lx = et.ENgetlinkindex(ln)
            link_index.append(lx)
        self.link_index = link_index

        pump_index=[]
        for ln in self.parameters['pumps_names']:
            ret, lx = et.ENgetlinkindex(ln)
            pump_index.append(lx)
        self.pumps_index = pump_index

    def get_node_index(self):
        node_index=[]
        for nn in self.parameters['mes_nodes_names']:
            ret, nx = et.ENgetnodeindex(nn)
            node_index.append(nx)
            self.node_index = node_index

        tank_index=[]
        for nn in self.parameters['tanks_names']:
            ret, nx = et.ENgetnodeindex(nn)
            tank_index.append(nx)
            self.tank_index = tank_index

    def get_pattern_index(self):
        pattern_index=[]
        for pn in self.parameters['pumps_patterns_names']:
            ret, px = et.ENgetpatternindex(pn)
            pattern_index.append(px)
        self.pumps_pattern_index = pattern_index

        pattern_index=[]
        for pn in self.parameters['demand_patterns_names']:
            ret, px = et.ENgetpatternindex(pn)
            pattern_index.append(px)
        self.demand_pattern_index = pattern_index


    def set_time_duration(self):
        et.ENsettimeparam(0,self.parameters['time_duration_s'])

    def set_tank_inital(self):
        for tank_in,initial_val in zip(self.tank_index,self.random['tanks_init_val']):
            et.ENsetnodevalue(tank_in,8,initial_val[0])

    def set_patern_values(self):
         for i in range(self.parameters['num_pumps']):
            #print(self.data.keys())
            for j in range(self.parameters['time_duration_h']):
                et.ENsetpatternvalue(self.pumps_pattern_index[i],j+1,self.random['pump_input'][i][j])

         for i in range(self.parameters['num_demands']):
            for j in range(self.parameters['time_duration_h']):
                et.ENsetpatternvalue(self.demand_pattern_index[i],j+1,self.random['demand_val'][i][j])


    def save_temp_file(self):
        et.ENsaveinpfile('temporary_'+self.parameters['file_name'])

    def get_set_parameters(self):
        self.get_link_index()
        self.get_node_index()
        self.get_pattern_index()
        self.set_time_duration()
        self.read_pattern_bounds_file()

    def prepare_empty_dict_to_comput(self):

        self.data = {'error_output': []}

        self.data['time_output'] = []

        for mes_node in self.parameters['mes_nodes_names']:
            self.data['head_output_' + mes_node] = []

        for mes_link in self.parameters['mes_links_names']:
            self.data['flow_output_' + mes_link] = []

        for mes_tank in self.parameters['tanks_names']:
            self.data['tank_output_' + mes_tank] = []

        for pumps_name in self.parameters['pumps_names']:
            self.data['energy_output_' + pumps_name] = []

        for tank_input in self.parameters['tanks_names']:
            self.data['tank_input_' + tank_input] = []

        for pump_input in self.parameters['pumps_names']:
            self.data['pump_input_' + pump_input] = []

        for demand_input in self.parameters['demand_patterns_names']:
            self.data['demand_input_' + demand_input] = []

    def get_hydraulic_values(self):

        et.ENopenH()
        et.ENinitH(0)
        time=[]
        flow=[[] for i in range(self.parameters['num_mes_links'])]
        head=[[] for i in range(len(self.node_index))]
        energy=[[] for i in range(self.parameters['num_pumps'])]
        error = []
        while True:
            ret, t = et.ENrunH()
            if t%self.parameters['hydraulic_step_s']==0:
                error.append(ret)
                time.append(t)
                if self.parameters['hydraulic_values'][0] == 'flow':
                    for i in range(0,len(self.link_index)):
                        #print(self.link_index[i])
                        ret, p = et.ENgetlinkvalue(self.link_index[i], et.EN_FLOW)
                        flow[i].append(p)

                if self.parameters['hydraulic_values'][2] == 'head':
                    for i in range(0, len(self.node_index)):
                        ret, p = et.ENgetnodevalue(self.node_index[i], et.EN_HEAD)
                        head[i].append(p)

                if self.parameters['hydraulic_values'][1] == 'energy':
                    for i in range(0, self.parameters['num_pumps']):
                        ret, p = et.ENgetlinkvalue(self.pumps_index[i], et.EN_ENERGY)
                        energy[i].append(p)

            ret, tstep = et.ENnextH()
            if (tstep <= 0):
                break
        ret = et.ENcloseH()
        return flow, energy, head, error, time


    def generate_random(self):

        self.random['pump_input'] = []
        self.random['demand_val'] = []
        self.random['tanks_init_val'] = []

        for ii in range(0, self.parameters['num_pumps']):
            pump_control = []
            for i in range(1, self.parameters['time_duration_h'] + 1):
                pump_control.append(random.randint(50, 100)/100)
            self.random['pump_input'].append(pump_control)
            self.data['pump_input_' + self.parameters['pumps_names'][ii]].append(pump_control)

        for ii in range(0, self.parameters['num_demands']):
            demand_val = []
            for i in range(0, self.parameters['time_duration_h'] ):
                demand_val.append(random.randint(int(self.pattern_bounds[i%24][0]*1000), int(self.pattern_bounds[i%24][1]*1000)) / 1000)
            self.random['demand_val'].append(demand_val)
            self.data['demand_input_' + self.parameters['demand_patterns_names'][ii]].append(demand_val)

        tanks_init_val = []
        for ii in range(0, self.parameters['num_tanks']):
            tanks_init_val.append(random.randint(self.parameters['min_tanks_lev'][ii] * 10,
                                                 self.parameters['max_tanks_lev'][ii] * 10) / 10)

        self.random['tanks_init_val'].append(tanks_init_val)

    def insert_data(self, head,flow, energy, error, time):

        for ii in range(0, self.parameters['num_mes_nodes'] - self.parameters['num_tanks'] + 1):
            self.data['head_output_' + self.parameters['mes_nodes_names'][ii]].append(head[ii])

        for ii in range(self.parameters['num_mes_nodes'] - self.parameters['num_tanks'],
                        self.parameters['num_mes_nodes']):
            self.data['tank_output_' + self.parameters['tanks_names'][
                self.parameters['num_mes_nodes'] - ii - 1]].append(head[ii])

        for ii in range(0, self.parameters['num_tanks']):
            temp_tank_init = []
            for i in range(0, self.parameters['time_duration_h']):
                temp_tank_init.append(self.random['tanks_init_val'][ii][0])
                #print([i,ii,temp_tank_init])
            self.data['tank_input_' + self.parameters['tanks_names'][ii]].append(temp_tank_init)


        for ii in range(self.parameters['num_mes_links']):
            self.data['flow_output_' + self.parameters['mes_links_names'][ii]].append(flow[ii])

        for ii in range(self.parameters['num_pumps']):
            self.data['energy_output_' + self.parameters['pumps_names'][ii]].append(energy[ii])

        self.data['time_output'].append(time)

        self.data['error_output'].append(error)

    def fix_data(self,flow, energy, head, error, time):

        for i in range(len(flow)):
            flow[i] = flow[i][:-1]

        for i in range(len(energy)):
            energy[i] = energy[i][:-1]

        for i in range(len(head)):
            head[i] = head[i][:-1]

        error = error[:-1]
        time = time[:-1]

        return flow, energy, head, error, time

    def read_pattern_bounds_file(self):
        with open(self.parameters['pattern_file_name']) as f:
            lines = f.readlines()
        self.pattern_bounds = []
        for l in lines:
            self.pattern_bounds.append([float(l.split(';')[1]),float(l.split(';')[2])])


    def get_data(self):

        self.prepare_empty_dict_to_comput()

        self.open_epanet()
        self.get_set_parameters()

        for i in tqdm(range(1, self.parameters['number_iteration']+1)):
            #print(i)
            self.generate_random()
            self.set_tank_inital()
            self.set_patern_values()
            self.save_temp_file()

            [flow, energy, head, error, time] = self.get_hydraulic_values()

            [flow, energy, head, error, time] = self.fix_data(flow, energy, head, error, time)

            self.insert_data(head , flow , energy , error,time)

        self.close_epanet()
if __name__ == '__main__':
    print('To jest biblioteka pomocna przy generowaniu wyników z Epanetu')