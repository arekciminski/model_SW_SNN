from epanettools import epanet2 as et
class Epa:

    def __init__(self, parameter):
        self.parameter = parameter
        self.patern_index = []
        self.link_index = []
        self.patern_index = []
        self.nnodes = []
        self.nlinks = []

    def open_epanet(self):
        ret = et.ENopen(self.parameter['file_name'], "Net3.rpt", "")

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
        for ln in self.parameter['mes_link_name']:
            ret, lx = et.ENgetlinkindex(ln)
            link_index.append(lx)
        self.link_index = link_index

    def get_node_index(self):
        node_index=[]
        for nn in self.parameter['mes_node_name']:
            ret, nx = et.ENgetnodeindex(nn)
            node_index.append(nx)
            self.node_index = node_index
        tank_index=[]
        for nn in self.parameter['tank_names']:
            ret, nx = et.ENgetnodeindex(nn)
            tank_index.append(nx)
            self.tank_index = tank_index

    def get_pattern_index(self):
        pattern_index=[]
        for pn in self.parameter['pattern_names']:
            ret, px = et.ENgetpatternindex(pn)
            pattern_index.append(px)
        print(pattern_index)
        self.pattern_index = pattern_index

    def set_time_duration(self):
        et.ENsettimeparam(0,self.parameter['time_duration'])

    def set_tank_inital(self):
        for tank_in,initial_val in zip(self.tank_index,self.parameter['initial_tanks']):
            et.ENsetnodevalue(tank_in,8,initial_val)

    def set_patern_values(self):
         for i in range(len(self.pattern_index)):
            for j in range(len(self.parameter['pattern_values'][0])):
                et.ENsetpatternvalue(self.pattern_index[i],j+1,self.parameter['pattern_values'][i][j])

    def save_temp_file(self):
        et.ENsaveinpfile('temporary_'+self.parameter['file_name'])

    def get_set_parameters(self):
        ep.get_link_index()
        ep.get_node_index()
        ep.get_pattern_index()
        ep.set_time_duration()
        ep.set_tank_inital()
        #ep.set_patern_values()
        #ep.save_temp_file()

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
            if self.parameter['hydraulic_values'][0] == 'flow':
                for i in range(0,len(self.link_index)):
                    #print(self.link_index[i])
                    ret, p = et.ENgetlinkvalue(self.link_index[i], et.EN_FLOW)
                    flow[i].append(p)
            for i in range(0, len(self.node_index)):
                if self.parameter['hydraulic_values'][1] == 'pressure':
                    ret, p = et.ENgetnodevalue(self.node_index[i], et.EN_PRESSURE)
                    pressure[i].append(p)
                if self.parameter['hydraulic_values'][2] == 'head':
                    ret, p = et.ENgetnodevalue(self.node_index[i], et.EN_HEAD)
                    head[i].append(p)
            ret, tstep = et.ENnextH()
            if (tstep <= 0):
                break
        ret = et.ENcloseH()
        return flow, pressure, head, error, time

if __name__ == '__main__':
    parameters = {
    'file_name' : "siec_maly_obiekt.inp",
    'mes_link_name' :['1','2'],
    'mes_node_name':['7'],
    'pumps_names' : ['pompka'],
    'pattern_names' :['demand','pompka'],
    'pattern_values' : [[1],[0.4]],
    'time_duration': 3600,
    'tank_names': ['7'],
    'initial_tanks' : [4],
    'hydraulic_values': ['flow', 'pressure', 'head']
    }

    ep = Epa(parameters)
    ep.open_epanet()
    ep.get_set_parameters()
    ep.set_patern_values()
    [flow, pressure, head, error, time] = ep.get_hydraulic_values()
    ep.close_epanet()
    print(pressure)