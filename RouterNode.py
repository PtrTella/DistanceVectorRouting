#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    # Variable declaration
    neighbourCosts = None
    minCosts = None
    nextHop = None
    poisonReverse = False
    immidiateNeighbours = None
    prevNeighbourCosts = None
    

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        # Initialize class variables
        self.poisonReverse = self.sim.POISONREVERSE
        self.minCosts = deepcopy(costs)
        self.immidiateNeighbours = deepcopy(costs)

        self.neighbourCosts = [[self.sim.INFINITY]*self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.neighbourCosts[ID] = costs        
        self.nextHop = [-1] * self.sim.NUM_NODES
        for i in range(self.sim.NUM_NODES):
                if (costs[i] < self.sim.INFINITY):
                    self.nextHop[i] = i


        self.myGUI.println("My initial routing table is :")
        self.myGUI.println(str(self.neighbourCosts) +"\n")

        self.prepare_send()

    
    # --------------------------------------------------
    def recvUpdate(self, pkt):
        self.myGUI.println("Got an update from " + str(pkt.sourceid) +
                ", its minimum costs is : " + str(pkt.mincost))
        self.neighbourCosts[pkt.sourceid] = pkt.mincost
        for i in range (self.sim.NUM_NODES):

            if (i!=self.myID):
                newCost = self.neighbourCosts[self.myID][pkt.sourceid] + pkt.mincost[i]
                if (self.minCosts[i] > newCost):
                    self.minCosts[i] = newCost
                    self.neighbourCosts[self.myID][i] = self.minCosts[i]
                    self.nextHop[i] = pkt.sourceid
                    self.prepare_send()
    def prepare_send(self):
        self.myGUI.println("My new min cost is: "+ str(self.minCosts))
        for i in range(self.sim.NUM_NODES):
            if (self.immidiateNeighbours[i] < self.sim.INFINITY and i != self.myID):
                # Poisoned Reversed
                falseMincost = deepcopy(self.minCosts)
                if self.sim.POISONREVERSE:
                    falseMincost = deepcopy(self.minCosts)
                    if self.nextHop[i] != i:
                            falseMincost[i] = self.sim.INFINITY

                    pkt = RouterPacket.RouterPacket(self.myID, i, falseMincost)
                    self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                        " I'm sending my minimum cost " + str(falseMincost) + "to " + str(pkt.destid))
                    self.sendUpdate(pkt)
                else:#end Poisoned Reverse
                    pkt = RouterPacket.RouterPacket(self.myID, i, deepcopy(self.minCosts))
                    self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                                       " I'm sending my minimum cost " + str(falseMincost) + "to " + str(pkt.destid))
                    self.sendUpdate(pkt)

    # --------------------------------------------------
    def sendUpdate(self,pkt):
        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        if(self.neighbourCosts != self.prevNeighbourCosts):
            self.myGUI.println("Current routing table for " + str(self.myID) +
                            "  at time " + str(self.sim.getClocktime()))
            self.myGUI.println(str(self.neighbourCosts) + "\n")
            self.prevNeighbourCosts = deepcopy(self.neighbourCosts)
            # We print the route for each
            for i in range(self.sim.NUM_NODES):
                if i!=self.myID:
                    self.myGUI.println("Next hop to go to "+ str(i)+
                                   " is "+ str(self.nextHop[i]))
        self.myGUI.println("\n")
    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        self.myGUI.println("\nUpdating link cost between " + str(self.myID) + " to " + str(dest) + " of " + str(newcost) + "\n")
        self.immidiateNeighbours[dest] = newcost

        #New computation
        for i in range(self.sim.NUM_NODES):
            if (i != self.myID):
                updateCost= newcost+ self.neighbourCosts[dest][i]
                if (self.minCosts[i] > updateCost):
                    self.minCosts[i] = updateCost
                    self.neighbourCosts[self.myID][i] = self.minCosts[i]
                    self.prepare_send()


