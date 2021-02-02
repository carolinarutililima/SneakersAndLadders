import gym
from gym import spaces, logger
from gym.utils import seeding
import copy 
import random




class Snakes_Ladders(gym.Env):


	def __init__(self):

		self.current_value = 0
		self.snakes = {
			98: 79,
			95: 75,
			93: 73,
			87: 24,
			64: 60,
			62: 19,
			54: 34,  
			17: 7
		}
		self.ladders = {
			1: 38,
			4: 14,
			9: 31,
			21: 42,
			28: 84,
			51: 67,
			71: 91,
			80: 100
		}       

		self.grid = 1 # grid dim 
		self.max_val = self.grid * 100

		
	def reset(self):
		self.current_value = 0
		self.snakes = {
			98: 79,
			95: 75,
			93: 73,
			87: 24,
			64: 60,
			62: 19,
			54: 34,  
			17: 7
		}
		self.ladders = {
			1: 38,
			4: 14,
			9: 31,
			21: 42,
			28: 84,
			51: 67,
			71: 91,
			80: 100
		} 
		return self.current_value

	def grid_option(self):

		final_snakes = {}
		for i in range(1, self.grid):
			for k, v in self.snakes.items():
				final_snakes[k + i * 100] = v + i * 100

		final_ladders = {}
		for i in range(1, self.grid):
			for k, v in self.ladders.items():
				final_ladders[k + i * 100] = v + i * 100

		return final_snakes, final_ladders

	def snake_ladder(self, action):


		self.snakes, self.ladders = self.grid_option()
		old_value = self.current_value
		self.current_value = self.current_value + action


		if self.current_value > self.max_val:
			sizegrid = self.current_value - self.max_val
			self.current_value = self.max_val - sizegrid

		print("\n" + " You moved from " + str(old_value) + " to " + str(self.current_value))


		if self.current_value in self.snakes:
			final_value = self.snakes.get(self.current_value)
			reward = -0.5 * final_value
			print("\n" +  " ~~~~~~~~>")
			print("\n" " You got a snake bite. Down from " + str(old_value) + " to " + str(self.current_value))

			
		elif self.current_value in self.ladders:
			final_value = self.ladders.get(self.current_value)
			reward = 1.5 * final_value
			print("\n"  + " ########")
			print("\n" + " You climbed the ladder from " + str(old_value) + " to " + str(self.current_value))

		else:
			final_value = self.current_value
			reward = 1 * final_value

		print("\n" + " Final state " + str(final_value))

		return final_value, reward
   
	
	def get_dice_value(self, dice):

		if dice == 0:
			action = random.randrange(1, 6, 2)
			#action = random.randint(1, 6)
		elif dice == 1:
			action = random.randrange(2, 7, 2)
			#action = random.randint(1, 6)		
		#elif dice == 2:
		#	action = random.randint(1, 6)		
		#elif dice == 3:
		#	action = random.randint(1, 6)
		#elif dice == 4:
		#	action = random.randint(1, 6)
		#elif dice == 5:
		#	action = random.randint(1, 6)
		return action


	def step(self, dice):
		done =  False 

		new_action = self.get_dice_value(dice)


		current_position, reward =  self.snake_ladder(new_action)

		if self.max_val == current_position:
			reward = 100 * reward 
			done = True 

		return current_position, reward, done, {}