import mesa
import numpy as np

from .agents import BarCustomer


class ElFarolBar(mesa.Model):
    def __init__(
        self,
        crowd_threshold=60,
        num_strategies=10,
        memory_size=10,
        N=100,
    ):
        super().__init__()
        self.running = True
        self.num_agents = N

        # Initialize the previous attendance randomly so the agents have a history
        # to work with from the start.
        # The history is twice the memory, because we need at least a memory
        # worth of history for each point in memory to test how well the
        # strategies would have worked.
        self.history = np.random.randint(0, 100, size=memory_size * 2).tolist()
        self.attendance = self.history[-1]

        # array for storing counters of customers who arrived when the crowd_threshold was reached
        self.arrived_when_full = []

        for unique_id in range(self.num_agents):
            BarCustomer(self, memory_size, crowd_threshold, num_strategies, unique_id)

        self.datacollector = mesa.DataCollector(
            model_reporters={"Customers": "attendance"},
            agent_reporters={"Utility": "utility", "Attendance": "attend"},
        )

    def step(self):
        self.datacollector.collect(self)
        self.attendance = 0
        self.agents.shuffle_do("update_attendance")

        # save count of customers who arrived at a full bar
        total_arrived_when_full = sum(agent.arrived_when_full for agent in self.agents)
        self.arrived_when_full.append(total_arrived_when_full)

        # We ensure that the length of history is constant
        # after each step.
        self.history.pop(0)
        self.history.append(self.attendance)
        self.agents.shuffle_do("update_strategies")
