import random
from collections import defaultdict


class MarkhovChain(object):

    def __init__(self, transitions=None):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.present_state = None
        if transitions is None:
            return
        for s_init, s_next, count in transitions:
            if s_next in self.transitions[s_init]:
                raise Exception("Transition %s -> %s defined multiple"
                        + " times in initializer" % (s_init, s_next))
            self.transitions[s_init][s_next] = count
        if self.present_state not in self.transitions:
            self.present_state = random.randrange(0, len(self.transitions))

    def add_transition(self, s_init, s_next):
        self.transitions[s_init][s_next] += 1

    def remove_transition(self, s_init, s_next):
        if s_init in self.transitions and s_next in self.transitions[s_init]:
            del self.transitions[s_init][s_next]

    def set_state(self, state):
        if state in self.transitions:
            self.present_state = self.transitions[state]
        raise Exception("No such state %s present" % state)

    def next_state(self):
        if len(self.transitions[self.present_state]) == 0:
            raise Exception("Cannot transition from state %s" \
                    % self.present_state)
        size = 0
        for k, v in self.transitions[self.present_state].iteritems():
           size += v
        selection = random.randrange(0, size + 1)
        for k, v in self.transitions.iteritems():
            if selection <= v:
                self.present_state = k
                return k

    def random_state(self):
        self.present_state = \
            self.transitions[random.randrange(0, len(self.transitions))]

