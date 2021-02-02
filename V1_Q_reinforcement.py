import gym
import random
import numpy as np
from V1_env_alg import Snakes_Ladders


env = Snakes_Ladders()

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1 # alpha
discount_rate = 0.9 # gamma
lamb = 0.1 # 0.5, and 0,9

exploration_rate = 1 #eps

rewards_all_episodes = []

eligibility = np.zeros(shape=(101,2)) # change here the dimentions to 201 or 301, and the dices numbers
q_table = np.zeros(shape=(101,2)) # change here the dimentions to 201 or 301, and dices numbers



for episode in range(num_episodes):

	state = env.reset()
	done = False 
	reward_current_episode = 0 

	for step in range(max_steps_per_episode): 

		exploration_rate_treseshold = random.uniform(0,1)
		if exploration_rate_treseshold > exploration_rate:
			action = np.argmax(q_table[state])
		
		else:
			action = random.randint(0, 1)


		new_state, reward, done, info = env.step(action) 


		eligibility[state, action] = eligibility[state,action] + 1


		td_error = reward + discount_rate * np.max(q_table[new_state, action]) - q_table[state, action]


		q_table[state,action] = q_table[state,action] + learning_rate  * eligibility[state,action] * td_error
	
		
		eligibility *= lamb * discount_rate

	
		reward_current_episode += reward

		if done:
			break
		else:
			state = new_state

	rewards_all_episodes.append(reward_current_episode)

	#exploration rate decay 

	exploration_rate = exploration_rate - 0.000009

	
	


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

n_states = 101
max_action = []
for j in range(n_states):
	x = np.argmax(q_table[j])
	max_action.append(x)


print(max_action)
