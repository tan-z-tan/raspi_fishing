import random
import numpy

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
		next_particles = map(self.next_state, self.particle_list)
		likelihood_list = map(self.evaluate, next_particles)
		self.particle_list = self.resampling(next_particles, likelihood_list)

	def resampling(self, particle_list, likelihood_list):
		samples = []
		random_list = sorted(map(lambda x: random.random() * sum(likelihood_list), range(self.size)))
		random_list.append(float('inf'))

		reached_index = 0
		cumulative_value = 0
		for l, p in zip(likelihood_list, particle_list):
			cumulative_value += l
			while( random_list[reached_index] < cumulative_value and reached_index < self.size ):
				samples.append(p)
				reached_index += 1

		return samples

	def estimate(self):
		average = [0.0, 0.0]
		for p in self.particle_list:
			average[0] += p[0]
			average[1] += p[1]
		average[0] /= self.size
		average[1] /= self.size
		return average

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

