import gym
import random
import numpy as np
from V2_env_alg import Snakes_Ladders



def updateV(V_value, path, learning_rate , discount_rate, lamb, eligibility):


	for i in range( len(path)-2, -1, -1 ):

		new_state, reward, state = path[i]

		eligibility[state] = eligibility[state] + 1    


		td_error = reward + discount_rate * V_value[new_state] - V_value[state]

		V_value = V_value + learning_rate * td_error * eligibility

		eligibility *= lamb * discount_rate

	return V_value



def policyEvaluate(env):

	state = env.reset()
	path = []
	done = False 
	x = [0,1,2,3,4,5,6,7]
	sum_reward = 0	

	while not done:

		action = random.choice(x) # probabilidade de escolher o dado e escada
		
		new_state, reward, done, info = env.step(action)

		path.append((new_state, reward, state ))

		state = new_state

		sum_reward =  sum_reward + reward

	return path, reward



env = Snakes_Ladders()

learning_rate = 0.1 # alpha
discount_rate = 0.9 # gamma
lamb = 0.1 # 0.5, and 0,9
eligibility = np.zeros(101) # change here the dimentions to 201 or 301
V = np.zeros(101) # change here the dimentions to 201 or 301
n_steps = []
average_reward = []

for i in range(1000):
	state = env.reset()
	p, sum_reward = policyEvaluate(env)
	V_value = updateV(V, p, learning_rate, discount_rate, lamb, eligibility)
	n_steps.append(len(p))
	average_reward.append(sum_reward)




average = sum(n_steps)/ len(n_steps)
print("steps average", average)

average_reward = sum(average_reward)/1000
print("reward average", average_reward)


for i in V_value:
	print("{:.8f}".format(i))
