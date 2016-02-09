import random
import numpy as np

class ParticleFilter:
	def __init__(self, size = 100, evaluate = None, next_state = None, initial_state = None):
		self.size = size
		self.particle_list = []
		self.evaluate = evaluate
		self.next_state = next_state
		self.initial_state = initial_state
		self.current_step = 0

	def step(self):
		self.current_step += 1
		next_particles = np.apply_along_axis(self.next_state, 1, self.particle_list)
		likelihood_list = np.apply_along_axis(self.evaluate, 1, next_particles)
		self.particle_list = self.resampling(next_particles, likelihood_list)

	def resampling(self, particle_list, likelihood_list):
		samples = np.zeros([self.size, 2])
		random_list = np.sort(np.random.rand(self.size + 1) * sum(likelihood_list))
		random_list[self.size] = float('inf')

		reached_index = 0
		cumulative_value = 0
		for l, p in zip(likelihood_list, particle_list):
			cumulative_value += l
			while( random_list[reached_index] < cumulative_value and reached_index < self.size ):
				samples[reached_index] = p
				reached_index += 1

		return samples

	def estimate(self):
		return np.mean(self.particle_list, 0)

	def initialize(self):
		self.particle_list = map(self.initial_state, range(self.size))

if __name__ == "__main__":
	# this sample tracks a fixed point (0.2, 0.8)
	evaluate = lambda p: 1 / (1 + abs(p[0] - 0.2)) + 1 / (1 + abs(p[1] - 0.8))
	next_state = lambda p: [p[0] + random.random() * 0.2 - 0.1, p[1] + random.random() * 0.2 - 0.1]
	initial_state = lambda p: [random.random(), random.random()]

	pf = ParticleFilter(size = 100, evaluate = evaluate, next_state = next_state, initial_state = initial_state)

	pf.initialize()
	for i in range(100):
		print "Estimate ", pf.current_step, pf.estimate()
		pf.step()

