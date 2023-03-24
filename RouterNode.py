#!/usr/bin/env python
import GuiTextArea
import RouterPacket
import F
from copy import deepcopy


class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    # Variable declaration
    neighbourCosts = None
    routingTable = None
    minCosts = None
    nextHop = None
    poisonReverse = False

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------

    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ")
        # Initialize class variables
        self.poisonReverse = False#self.sim.POISONREVERSE
        self.neighbourCosts = deepcopy(costs)
        self.minCosts = deepcopy((costs))

        self.routingTable = [[self.sim.INFINITY] *
                             self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.routingTable[self.myID] = deepcopy(self.neighbourCosts)
        self.nextHop = [-1] * self.sim.NUM_NODES

        for i in range(self.sim.NUM_NODES):
            if (costs[i] < self.sim.INFINITY):
                self.nextHop[i] = i
        self.myGUI.println("My initial routing table is :")
        self.myGUI.println(str(self.routingTable) + "\n")
        # first iteration of the Distance Vector algorithm
        self.prepare_send(None)

    # --------------------------------------------------

    def recvUpdate(self, pkt):
        self.myGUI.println(" --------------------------------------------------------------------")
        self.myGUI.println("I'm " + str(self.myID) + ", Got an update from " + str(pkt.sourceid) +
                           ", its news minimum costs are : " + str(pkt.mincost))
        #We update our routing table with its new min costs
        self.routingTable[pkt.sourceid] = pkt.mincost
        # Then we are going to compute our new min costs and see if it's less than the previous one, that we store
        previousMinCosts = deepcopy(self.minCosts)
        # for each node i we compute the min cost to go to him
        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println(
                    "Compute min cost to go to " + str(i) + " from " + str(self.myID))
                possibleCost = self.neighbourCosts[i]
                # We are going to check if the cost to go directly to i
                # is greater than passing through another node
                print(" Cost to go directly to " +
                      str(i) + " is " + str(possibleCost))
                for j in range(self.sim.NUM_NODES):
                    if (j != i and j != self.myID):
                        #We compute the cost to go to j from ourself + the min cost to go from j to i
                        possibleCost1 = self.neighbourCosts[j] + \
                            self.routingTable[j][i]

                        print("possible cost by " + str(j) + " to go to " +
                              str(i) + " is " + str(possibleCost1))
                        #We check which one is the lower
                        if possibleCost1 < possibleCost:
                            possibleCost = possibleCost1
                            # if we need to pass through j, we update the nextHop variable
                            self.nextHop[i] = j
                #We store the min cost
                self.minCosts[i] = possibleCost
                print("Finally my min cost to go to " +
                      str(i) + " is " + str(self.minCosts[i]))

        print("Finally my min cost after computation is " + str(self.minCosts))
        print("My previous one was: " + str(previousMinCosts))
        #If the min cost has changed, we send it to our direct neigbours
        if self.minCosts != previousMinCosts:
            print(" It changed so I send the new one")
            self.prepare_send(None)
        else:
            print("No change, I do nothing")

    # -------------------------------

    def prepare_send(self, nodePoisoned):
        self.myGUI.println("My new min cost is: " + str(self.minCosts))
        self.routingTable[self.myID] = self.minCosts
        #Variable to store the node that will need to be poisoned
        nodePoisoned = []

        for i in range(self.sim.NUM_NODES):

            #If the poisoned Revers is activated
            if (self.poisonReverse and self.nextHop[i] != i):
                #To go to i we need to go through an other node,
                #so we send to the other node that our cost to i is infinity
                self.myGUI.println("POISONING")
                fakeMinCosts = deepcopy(self.minCosts)
                fakeMinCosts[i] = self.sim.INFINITY
                pkt = RouterPacket.RouterPacket(self.myID, self.nextHop[i], fakeMinCosts)
                self.myGUI.println("POISON At time " + str(self.sim.getClocktime()) +
                                   " I'm sending my minimum cost " + str(fakeMinCosts) + "to " + str(self.nextHop[i]))
                self.sendUpdate(pkt)
                #We store the ID of the other node to be sure to not send it again with the not fake min costs
                nodePoisoned.append(self.nextHop[i])
            if (self.neighbourCosts[i] < self.sim.INFINITY and i != self.myID):

                if(i in nodePoisoned):
                    #For this node, we already send the poisoned min cost
                    pass
                else:

                    pkt = RouterPacket.RouterPacket(
                        self.myID, i, deepcopy(self.minCosts))
                    self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                                    " I'm sending my minimum cost " + str(self.minCosts) + "to " + str(pkt.destid))
                    self.sendUpdate(pkt)




        self.myGUI.println("\n")
    # --------------------------------------------------

    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

    # --------------------------------------------------

    def printDistanceTable(self):

        self.myGUI.println("Current routing table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println(str(self.routingTable) + "\n")
        # We print the route for each
        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println("Next hop to go to " + str(i) +
                                   " is " + str(self.nextHop[i]))
        self.myGUI.println("\n")
    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        self.myGUI.println(" --------------------------------------------------------------------")
        self.poisonReverse = self.sim.POISONREVERSE
        self.myGUI.println("updated link cost to " +
                           str(dest) + "(" + str(newcost) + ")")
        #Fisrt we update our neighbours costs
        for i in range(self.sim.NUM_NODES):
            if i == dest:
                self.neighbourCosts[i] = newcost

        self.myGUI.println("My news neighbours costs are :" +
                           str(self.neighbourCosts))
        self.myGUI.println("I going to compute my new min costs")
        #Secondly we compute our new min costs
        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println(
                    "Compute min cost to go to " + str(i) + " from " + str(self.myID))
                possibleCost = self.neighbourCosts[i] + self.routingTable[i][i]
                self.nextHop[i] = i
                self.myGUI.println(str(possibleCost))
                self.minCosts[i] = possibleCost
                self.routingTable[self.myID][i] = self.minCosts[i]
        #Finally, we send it to our directly attached neighbours
        for i in range(self.sim.NUM_NODES):
            if i!= self.myID and self.neighbourCosts[i]!=self.sim.INFINITY:
                pkt = RouterPacket.RouterPacket(
                    self.myID, i, deepcopy(self.minCosts))
                self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                               " I'm sending my minimum cost " + str(self.minCosts) + "to " + str(pkt.destid))
                self.sendUpdate(pkt)