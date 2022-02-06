"""
Created on 25 Nov 2016
@author: keith

Setup bindings and attribute reports on given nodes and endpoints.

"""
import FF_zigbeeClusters as zcl
import FF_zigbeeToolsConfig as config

# nodes & endpoints 7c62
nodeList = [{'node': 'F29A', 'ep1': '05', 'ep2': '06'},
            # {'node':'DB43','ep1':'09','ep2':None}
            ]

ATTRS = "plugAttrs"


class hiveAttrs(object):
    def __init__(self, nodeList):
        self.tstat_heat_attrs = [('0000', '0001', '003C'),
                                 ('0012', '0001', '0078'),
                                 ('001C', '0001', '0078'),
                                 ('0023', '0001', '0078'),
                                 ('0024', '0001', '0078'),
                                 ('0029', '0001', '0078')]

        self.tstat_water_attrs = [('001C', '0001', '0078'),
                                  ('0023', '0001', '0078'),
                                  ('0024', '0001', '0078'),
                                  ('0029', '0001', '0078')]

        self.bg_clust_attrs = [('0020', '0001', '0078'),
                               ('0021', '0001', '0078'),
                               ('0022', '0001', '0078'),
                               ('0023', '0001', '0078'),
                               ('0024', '0001', '0078'),
                               ('0025', '0001', '0078'),
                               ('0026', '0001', '0078'),
                               ('0031', '0001', '0078')]

        # attrReports shall contain one line per node/cluster/ep combination (i.e. one row per required binding)
        self.attrReports = []
        for n in nodeList:
            self.attrReports.append({'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'Thermostat Cluster',
                                     'attrs': self.tstat_heat_attrs})
            self.attrReports.append({'nodeId': n['node'], 'epId': n['ep2'], 'clustName': 'Thermostat Cluster',
                                     'attrs': self.tstat_water_attrs})
            self.attrReports.append(
                {'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'BG Cluster', 'attrs': self.bg_clust_attrs})

        return


class plugAttrs(object):
    def __init__(self, nodeList):
        self.pwrConfigAttrs = [('0000', '0078', '0078'),  # mainsVoltage
                               ('0001', '0078', '0078')]  # mainsFrequency

        self.deviceTempConfigAttrs = [('0000', '0078', '0078')]  # currentTemperature

        self.onOffAttrs = [('0000', '0078', '0078')]  # onOff

        self.meterAttrs = [('0000', '0078', '0078'),  # currentSummationDelivered
                           ('0006', '0078', '0078'),  # powerFactor
                           ('0400', '0078', '0078')]  # instantaneousDemand

        self.attrReports = []
        for n in nodeList:
            self.attrReports.append({'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'Power Configuration Cluster',
                                     'attrs': self.pwrConfigAttrs})
            self.attrReports.append(
                {'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'Device Temperature Configuration Cluster',
                 'attrs': self.deviceTempConfigAttrs})
            self.attrReports.append(
                {'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'On/Off Cluster', 'attrs': self.onOffAttrs})
            self.attrReports.append(
                {'nodeId': n['node'], 'epId': n['ep1'], 'clustName': 'Metering Cluster', 'attrs': self.meterAttrs})

        return


attrClassDict = {"hiveAttrs": hiveAttrs(nodeList),
                 "plugAttrs": plugAttrs(nodeList)}

ATTRS = attrClassDict[ATTRS]

PORT = config.PORT
BAUD = config.BAUD

""" Helper methods """


def buildChangeRep(myClust, myAttr):
    """ Build the word for minimum reportable change.
        Digital Attrs -> None
        Analogue Attrs -> One zero per nibble e.g. 1byte = 00

    """
    _, _, attrType = zcl.getAttributeNameAndId(myClust, myAttr)
    AorD = zcl.dataTypes[attrType]['type']
    bits = zcl.dataTypes[attrType]['bits']
    if AorD == 'A':
        changeRep = '0' * int(bits / 4)
    elif AorD == 'D':
        changeRep = ''
    return changeRep


# Main Program Starts

if __name__ == "__main__":

    # Only import this if we are the main module (to prevent circular reference)
    import FF_threadedSerial as AT

    myWantedAttrs = ATTRS

    print("**** Configuration")
    print("")
    print("Port      = {}".format(config.PORT))
    print("Baud      = {}".format(config.BAUD))
    print("Firmware  = {}".format(config.FIRMWARE_ROOT_FILE_PATH))
    print("")

    # Print the nodes/endpoints/clusters/attributes and reporting configuration
    # Build a list of dicts containing the details for each attribute report config
    configList = []
    for node in ATTRS.attrReports:
        myNode = node['nodeId']
        myEp = node['epId']
        myClust = node['clustName']

        print("NodeId={0}, EP={1}, Clust={2}".format(myNode, myEp, myClust))

        attrs = node['attrs']
        # Print the clusters/attributes
        for attr in attrs:
            attrId = attr[0]
            minRep = attr[1]
            maxRep = attr[2]
            changeRep = buildChangeRep(myClust, attrId)
            _, attrName, _ = zcl.getAttributeNameAndId(myClust, attrId)
            print('    {},{:35},{},{},{}'.format(attrId, attrName, minRep, maxRep, changeRep))

            # nodeId, epId, clustId, attr, minRep, maxRep, changeRep
            clustId, _ = zcl.getClusterNameAndId(myClust)
            configList.append({'nodeId': myNode,
                               'epId': myEp,
                               'clustId': clustId,
                               'attrId': attrId,
                               'minRep': minRep,
                               'maxRep': maxRep,
                               'changeRep': changeRep})

        print("")

    # Setup bindings and attribute reporting
    i = input("Do you want to setup bindings and attribute reporting on these attributes? y/n ")
    if i.upper() == 'Y':

        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=True, rxQ=True, listenerQ=False)
        AT.debug = True
        # AT.getInitialData(node1,ep1,fastPoll=True, printStatus=True)

        print('Starting binding/reporting setup:')

        # Set required bindings
        for node in ATTRS.attrReports:
            nodeId = node['nodeId']
            epId = node['epId']
            clustId, _ = zcl.getClusterNameAndId(node['clustName'])
            print('Setting binding on {0},{1},{2}'.format(nodeId, epId, clustId))

            # Setup a binding
            _, _, mySrcAddr = AT.getEUI(nodeId, nodeId)
            _, _, myDstAddr = AT.getEUI('0000', '0000')
            respState, _, respValue = AT.setBinding(nodeId, mySrcAddr, epId, clustId, myDstAddr, '01')
            if not respState:
                print('Binding failed: ', respState, respValue)

        # Set attribute reporting on each attribute
        for attr in configList:
            respState, _, respValue = AT.setAttributeReporting(attr['nodeId'],
                                                               attr['epId'],
                                                               attr['clustId'],
                                                               attr['attrId'],
                                                               attr['minRep'],
                                                               attr['maxRep'],
                                                               attr['changeRep'])
            if not respState:
                print('Setting attribute reporting failed: ', respState, respValue)

    print('All Done')
