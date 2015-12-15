from chai import Chai
from collections import Counter
from markhov_chain import MarkhovChain

class SequentialRandom:

	def __init__(self):
		self.last = 0

	def _next(self):
		self.last += 1
		return self.last

	def sample(self, keys, num):
		l = []
		keys = list(keys)
		for i in range(num):
			l += [keys[self._next() % len(keys)]]
		return l

	def randint(self, a, b):
		r = b - a + 1
		n = self._next() % r
		return n + a

class TransitionTests(Chai):

	def setUp(self):
		
		super(TransitionTests, self).setUp()
		self.mc = MarkhovChain(random_source=SequentialRandom())

	def _make_dice(self):

		for i in range(1, 7):
			for j in range(1, 7):
				self.mc.add_transition(i, j)
		self.mc.set_random_state()

	def _dice_test(self, trials, expected):

		state_counts = Counter()

		for _ in range(trials):
			state_counts[self.mc.next_state()] += 1

		# Test transitions
		print()
		print("[ State distribution ]\n")

		for i in range(1, 7):
			print("   {} : {}".format(i, state_counts[i]))

		print("\nExpecting {}".format(expected))

		for k, c in state_counts.items():
			assertEqual(state_counts[k], expected[k])

	def test_fair_dice(self):

		self._make_dice()
		self._dice_test(1200, dict((x, 200) for x in range(1, 7)))

	def test_6_weighted_dice(self):

		self._make_dice()

		for i in range(1, 7):
			self.mc.add_transition(i, 6)

		expected = dict((x, 200) for x in range(1, 7))
		expected[6] = 400

		self._dice_test(1400, expected)

	def test_6_and_4_weighted_dice(self):

		self._make_dice()

		for i in range(1, 7):
			self.mc.add_transition(i, 6)
			self.mc.add_transition(i, 4)

		expected = dict((x, 200) for x in range(1, 7))
		expected[4] = 400
		expected[6] = 400

		self._dice_test(1600, expected)
