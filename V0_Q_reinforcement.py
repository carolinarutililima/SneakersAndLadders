import gym
import random
import numpy as np
from V0_env_alg import Snakes_Ladders


env = Snakes_Ladders()

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1 # alpha
discount_rate = 0.99 # gamma
lamb = 0.1 # 0.5, and 0,9

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate =  0.01

rewards_all_episodes = []


eligibility = np.zeros(shape=(101,1)) # change here the dimentions to 201 or 301
q_table = np.zeros(shape=(101,1))  # change here the dimentions to 201 or 301



state = env.reset()

for episode in range(num_episodes):

	action = 0
	done = False 
	reward_current_episode = 0

	for step in range(max_steps_per_episode):

		new_state, reward, done, info = env.step()


		eligibility[state, action] = eligibility[state,action] + 1


		td_error = reward + discount_rate * np.max(q_table[new_state, action]) - q_table[state, action]


		q_table[state,action] = q_table[state,action] + learning_rate  * eligibility[state,action] * td_error
	
		
		eligibility *= lamb * discount_rate

	
		reward_current_episode += reward

		if done:
			state = env.reset()
			break
		else:
			state = new_state

	#exploration rate decay 

	exploration_rate =  min_exploration_rate + \
	(max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

	rewards_all_episodes.append(reward_current_episode)



# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
count = 1000

print("********Average reward per thousand episodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

# Print updated Q-table
print("\n\n********Q-table********\n")
print(q_table)

