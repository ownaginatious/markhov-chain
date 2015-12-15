from chai import Chai
from markhov_chain import MarkhovChain


class ApiTests(Chai):

	def setUp(self):

		super(ApiTests, self).setUp()
		self.mc = MarkhovChain()

	def test_add_transition(self):

		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")

		self.mc.add_transition("B", "A")
		self.mc.add_transition("B", "C")

		self.mc.add_transition("C", "A")

		expected = {
			'A': { 'B': 3},
			'B': { 'A': 1, 'C': 1 },
			'C': { 'A': 1 }
		}

		assertEqual(self.mc._transition_dump(), expected)

	def test_remove_transition_singles(self):

		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")

		self.mc.add_transition("B", "A")
		self.mc.add_transition("B", "C")

		self.mc.add_transition("C", "A")

		self.mc.remove_transition("A", "B")
		self.mc.remove_transition("B", "A")
		self.mc.remove_transition("B", "A")
		self.mc.remove_transition("C", "A")

		expected = {
			'A': { 'B': 2 },
			'B': { 'C': 1 }
		}

		assertEqual(self.mc._transition_dump(), expected)

	def test_remove_transition_all(self):

		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")
		self.mc.add_transition("A", "B")

		self.mc.add_transition("B", "A")
		self.mc.add_transition("B", "C")
		self.mc.add_transition("B", "C")
		self.mc.add_transition("B", "C")

		self.mc.add_transition("C", "A")

		self.mc.remove_transition("A", "B", all=True)
		self.mc.remove_transition("B", "A", all=True)
		self.mc.remove_transition("B", "A", all=True)
		self.mc.remove_transition("B", "C", all=True)
		self.mc.remove_transition("B", "C", all=True)

		expected = {
			'C': { 'A': 1 }
		}

		assertEqual(self.mc._transition_dump(), expected)

