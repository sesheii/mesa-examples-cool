# visualization of number customers who arrived at the crowd_threshold reached
# this plot depicts total amount for each step


import matplotlib.pyplot as plt
from examples.el_farol.el_farol.model import ElFarolBar

model = ElFarolBar(N=100, memory_size=10)
steps_n = 100
for i in range(steps_n):
    model.step()

plt.figure(figsize=(12, 6))
plt.plot(model.arrived_when_full,
         label='Number of customers who arrived at crowd_threshold reached for each step',
         color='orange'
         )
plt.title('Number of customers who arrived at crowd_threshold reached')
plt.xlabel('Number of steps')
plt.ylabel('Number of customers')
plt.grid()
plt.legend()
plt.show()
