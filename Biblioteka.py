from epanettools import epanet2 as et
class Epa:

    def __init__(self, file_name):
        self.file_name = file_name
        self.patern_index = []
        self.link_index = []
        self.patern_index = []
        self.nnodes = []
        self.nlinks = []
    def open_epanet(self):
        ret = et.ENopen(self.file_name, "Net3.rpt", "")
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
    def get_link_number(self,link_names):
        link_index=[]
        for ln in link_names:
            ret, lx = et.ENgetlinkindex(ln)
            link_index.append(lx)
        self.link_index = link_index
        return link_index
    def get_node_number(self,node_names):
        node_index=[]
        for nn in node_names:
            ret, nx = et.ENgetnodeindex(nn)
            node_index.append(nx)
        self.node_index = node_index
        return node_index
    def get_patern_number(self,patern_names):
        patern_index=[]
        for pn in patern_names:
            ret, px = et.ENgetpatternindex(pn)
            patern_index.append(px)
        self.patern_index = patern_index
        return patern_index
    def get_hydraulic_values(self,hydrailic_values):
        et.ENopenH()
        et.ENinitH(0)
        time=[]
        flow=[[]]*len(self.link_index)
        pressure=[[]]*len(self.node_index)
        head=[[]]*len(self.node_index)
        error = []
        while True:
            ret, t = et.ENrunH()
            error.append(ret)
            time.append(t)
            if hydrailic_values[0] == 'flow':
                for i in range(0,len(self.link_index)):
                    #print(self.link_index[i])
                    ret, p = et.ENgetlinkvalue(self.link_index[i], et.EN_FLOW)
                    flow[i].append(p)
                    print(self.link_index[i],p, flow[i])
                #print(i,p,len(flow),len(flow[0]),t/3600)
            for i in range(0, len(self.node_index)):
                if hydrailic_values[1] == 'pressure':
                    ret, p = et.ENgetnodevalue(i, et.EN_PRESSURE)
                    pressure[i].append(p)
                if hydrailic_values[2] == 'head':
                    ret, p = et.ENgetnodevalue(i, et.EN_HEAD)
                    head[i].append(p)
            ret, tstep = et.ENnextH()
            if (tstep <= 0):
                break
        ret = et.ENcloseH()
        return flow, pressure, head, error, time