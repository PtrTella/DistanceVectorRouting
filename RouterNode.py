#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    # Varible dclaration
    neighbourCosts = None
    minCosts = None
    nextHop = None
    PoisonReverse = False

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        # Initialize class variables
        self.PoisonReverse = self.sim.POISONREVERSE
        self.minCosts = deepcopy(costs)
        self.neighbourCosts = [[self.sim.INFINITY]*self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.neighbourCosts[ID] = costs        
        self.nextHop = [-1] * self.sim.NUM_NODES
        for i in range(self.sim.NUM_NODES):
                if (costs[i] < self.sim.INFINITY):
                    self.nextHop[i] = i

        print("NODE %d" % ID) 
        print(self.neighbourCosts)
        print(self.minCosts)
        print(self.nextHop)

    def minCostUpdate(self):
        for i in range(self.sim.NUM_NODES):
            if (i != self.myID):
                self.minCosts[i] = self.sim.INFINITY
                for j in range(self.sim.NUM_NODES):
                    if (self.neighbourCosts[j][i] < self.sim.INFINITY):
                        self.minCosts[i] = min(self.minCosts[i], self.neighbourCosts[j][i] + self.minCosts[j])
                        if (self.minCosts[i] == self.neighbourCosts[j][i] + self.minCosts[j]):
                            self.nextHop[i] = j
        print(self.minCosts)

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        self.neighbourCosts[pkt.sourceid] = pkt.mincost
        self.minCosts = deepcopy(self.neighbourCosts[self.myID])
        pass


    # --------------------------------------------------
    def sendUpdate(self, pkt):
        pkt.sourceid = self.myID
        pkt.mincost = deepcopy(self.minCosts)
        pkt.destid = F.ALLNODES
        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))


    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        pass
