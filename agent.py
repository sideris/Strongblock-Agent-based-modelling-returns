import random

from constants import (STRONG_TO_NODE, MAKE_NODE_COST_GAS, CLAIM_COST_WITH_GAS, SELL_STRONG_COST_GAS,
                       NODE_MAINTAINANCE_GAS_PER_M, NODE_MAINTAINANCE_PER_M, BUY_STRONG_COST_GAS, MAX_NODES)


class Agent:
    def __init__(self, **kwargs):
        self.__has_ticked = False
        self.name = kwargs.get('name', None)
        self.nodes = kwargs.get('nodes', 0)
        self.node_goal = kwargs.get('node_goal', 10)
        self.cost_sheet = []
        self.benefit_sheet = []
        self.threshold_good_price_to_sell = kwargs.get('price_to_sell', random.randint(350, 700))  # TODO not used
        self.total_strong_wallet = kwargs.get('starting_strong', 0) # TODO not used
        self.total_strong_accum = kwargs.get('pending_strong', 0) # TODO not used

    def buy_strong_and_add_nodes(self, strong_price: float, n_nodes: int):
        self.cost_sheet[-1] += (n_nodes * strong_price * STRONG_TO_NODE) + \
                               MAKE_NODE_COST_GAS * n_nodes + \
                               BUY_STRONG_COST_GAS
        self.nodes += n_nodes

    def pay_node_maintainance_fees(self):
        self.cost_sheet[-1] += NODE_MAINTAINANCE_PER_M * self.nodes + NODE_MAINTAINANCE_GAS_PER_M

    def create_node(self) -> bool:
        self.__raise_if_not_tick()
        if self.nodes >= self.node_goal or self.nodes == MAX_NODES:
            return False
        if self.total_strong_wallet >= STRONG_TO_NODE:
            self.total_strong_wallet -= STRONG_TO_NODE
            self.cost_sheet[-1] += MAKE_NODE_COST_GAS
            self.nodes += 1
            return True
        elif self.total_strong_wallet + self.total_strong_accum >= STRONG_TO_NODE:
            self.claim_strong()
            self.cost_sheet[-1] += MAKE_NODE_COST_GAS
            self.nodes += 1
            self.total_strong_wallet = self.total_strong_wallet - STRONG_TO_NODE
            return True
        return False

    def sell_strong_in_wallet(self, strong_price: float):
        self.__raise_if_not_tick()
        gained = strong_price * self.total_strong_wallet - SELL_STRONG_COST_GAS
        self.benefit_sheet += gained
        self.total_strong_wallet = 0

    def claim_strong(self):
        self.__raise_if_not_tick()
        self.cost_sheet[-1] += CLAIM_COST_WITH_GAS
        self.total_strong_wallet = self.total_strong_wallet + self.total_strong_accum
        self.total_strong_accum = 0

    def claim_and_sell(self, strong_price: float):
        self.claim_strong()
        self.sell_strong_in_wallet(strong_price)

    def tick(self):
        """ Time tick per day. Called before any decision made """
        self.cost_sheet.append(0)
        self.benefit_sheet.append(0)
        self.total_strong_accum += self.nodes * 0.1
        self.__has_ticked = True

    def __raise_if_not_tick(self):
        if not self.__has_ticked:
            raise Exception('Agent has not ticked')

    def prepare_next_tick(self):
        self.__has_ticked = False
