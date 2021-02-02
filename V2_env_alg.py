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

		self.grid = 1 # grid dim it can be 2 or 3
		self.max_val = self.grid * 100
		self.drone = 50

		
	def reset(self):
		self.current_value = 0
		self.drone = 50
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
		
		reward = 1
		snakes, ladders = self.grid_option()
		old_value = self.current_value
		x = [1,2,3,4,5,6]

		if action in x:
			
			self.current_value = self.current_value + action

			print("\n" + " You moved from " + str(old_value) + " to " + str(self.current_value))

			if self.current_value == self.drone:
				drone_magic = random.randint(1,2)
				if drone_magic == 1:
					self.current_value = self.current_value + 10
					print("\n" +  " <0>")
					print("\n" " You found the drone " + str(old_value) + " to " + str(self.current_value))
				else:
					self.current_value = self.current_value - 20
					print("\n" +  " <0>")
					print("\n" " You found the drone " + str(old_value) + " to " + str(self.current_value))

			if self.current_value > self.max_val:
				sizegrid = self.current_value - self.max_val
				self.current_value = self.max_val - sizegrid

			if self.current_value < 1:
				self.current_value = 1

			if self.current_value in self.snakes:
				final_value = self.snakes.get(self.current_value)
				reward = -0.5 * final_value
				print("\n" +  " ~~~~~~~~>")
				print("\n" " You got a snake bite. Down from " + str(old_value) + " to " + str(self.current_value))
				
			else:
				
				final_value = self.current_value
				reward = reward * final_value

		else: 
			if action == 'n_ladder':
		 		final_value = self.current_value
		 		reward = final_value

			elif action == 'ladder':
		 		if self.current_value in ladders:
		 			final_value = ladders.get(self.current_value)
		 			reward = 1.25 * final_value
		 			print("\n"  + " ########")
		 			print("\n" + " You climbed the ladder from " + str(old_value) + " to " + str(final_value))
		 		else:
		 			final_value = self.current_value
		 			reward = -1.25 * final_value
		
		print("\n" + " Final state " + str(final_value))

		return final_value, reward
   
	
	def get_dice_value(self, dice):

		if dice == 0:
			action = random.randint(1, 6)
		elif dice == 1:
			action = random.randint(1, 6)
		elif dice == 2:
			action = random.randint(1, 6)
		elif dice == 3:
			action = random.randint(1, 6)
		elif dice == 4:
			action = random.randint(1, 6)
		elif dice == 5:
			action = random.randint(1, 6)
		elif dice == 6:
			action = 'n_ladder'
		elif dice == 7:
			action = 'ladder'
		return action


	def Drone(self):
		walkdrone = random.randint(1,2)

		if walkdrone == 1:
				self.drone = self.drone + 1
		else:
				self.drone = self.drone - 1
			
		if self.drone == 100:
				self.drone = 1
		elif self.drone == 1:
				self.drone = 100


	def step(self, action):
		done =  False 

		atual_value = self.current_value

		new_action = self.get_dice_value(action)
		current_value, reward =  self.snake_ladder(new_action)
		
		self.Drone()

		if self.max_val == current_value:
			reward = reward * 100
			done = True 

		return current_value, reward, done, {}