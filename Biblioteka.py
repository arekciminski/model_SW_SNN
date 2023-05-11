from epanettools import epanet2 as et
class Epa:

    def __init__(self, parameters):
        self.parameters = parameters
        self.patern_index = []
        self.link_index = []
        self.patern_index = []
        self.nnodes = []
        self.nlinks = []

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
        for pn in self.parameters['pumps_patterns']:
            ret, px = et.ENgetpatternindex(pn)
            pattern_index.append(px)
        self.pumps_pattern_index = pattern_index

        pattern_index=[]
        for pn in self.parameters['demand_patterns']:
            ret, px = et.ENgetpatternindex(pn)
            pattern_index.append(px)
        self.demand_pattern_index = pattern_index


    def set_time_duration(self):
        et.ENsettimeparam(0,self.parameters['time_duration'])

    def set_tank_inital(self):
        for tank_in,initial_val in zip(self.tank_index,self.parameters['initial_tanks']):
            et.ENsetnodevalue(tank_in,8,initial_val)

    def set_patern_values(self):
         for i in range(len(self.demand_pattern_index)):
            for j in range(len(self.parameters['demand_pattern_values'][0])):
                et.ENsetpatternvalue(self.demand_pattern_index[i],j+1,self.parameters['demand_pattern_values'][i][j])

         for i in range(len(self.pumps_pattern_index)):
            for j in range(len(self.parameters['pumps_pattern_values'][0])):
                et.ENsetpatternvalue(self.pumps_pattern_index[i],j+1,self.parameters['pumps_pattern_values'][i][j])


    def save_temp_file(self):
        et.ENsaveinpfile('temporary_'+self.parameters['file_name'])

    def get_set_parameters(self):
        self.get_link_index()
        self.get_node_index()
        self.get_pattern_index()
        self.set_time_duration()
        #ep.save_temp_file()

    def prepare_empty_dict_to_comput(self):
        self.data = {'error_output': []}

        for mes_node in self.parameters['mes_nodes_names']:
            self.data['head_output_' + mes_node] = []

        for mes_link in self.parameters['mes_links_names']:
            self.data['flow_output_' + mes_link] = []

        for mes_tank in self.parameters['tanks_names']:
            self.data['tank_output_' + mes_tank] = []

        for tank_input in self.parameters['tanks_names']:
            self.data['tank_input_' + tank_input] = []

        for pump_input in self.parameters['pumps_patterns']:
            self.data['pump_input_' + pump_input] = []

        for demand_input in self.parameters['demand_patterns']:
            self.data['demand_input_' + demand_input] = []

    def get_hydraulic_values(self):

        et.ENopenH()
        et.ENinitH(0)
        time=[]
        flow=[[] for i in range(len(self.link_index))]
        pressure=[[] for i in range(len(self.node_index))]
        head=[[] for i in range(len(self.node_index))]
        error = []
        while True:
            ret, t = et.ENrunH()
            error.append(ret)
            time.append(t)
            if self.parameters['hydraulic_values'][0] == 'flow':
                for i in range(0,len(self.link_index)):
                    #print(self.link_index[i])
                    ret, p = et.ENgetlinkvalue(self.link_index[i], et.EN_FLOW)
                    flow[i].append(p)
            for i in range(0, len(self.node_index)):
                if self.parameters['hydraulic_values'][1] == 'pressure':
                    ret, p = et.ENgetnodevalue(self.node_index[i], et.EN_PRESSURE)
                    pressure[i].append(p)
                if self.parameters['hydraulic_values'][2] == 'head':
                    ret, p = et.ENgetnodevalue(self.node_index[i], et.EN_HEAD)
                    head[i].append(p)
            ret, tstep = et.ENnextH()
            if (tstep <= 0):
                break
        ret = et.ENcloseH()
        return flow, pressure, head, error, time

if __name__ == '__main__':
    print('To jest biblioteka pomocna przy generowaniu wyników z Epanetu')