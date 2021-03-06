# -*- coding: utf-8 -*-

import random
import six
from collections import defaultdict
from sortedcollections import ItemSortedDict

import heapq
import pdb

class MarkhovChain(object):

    def __init__(self, transitions=None, random_source=random.SystemRandom()):
        self.transitions = defaultdict(lambda: ItemSortedDict(lambda k, v: (v, k)))
        self.present_state = None
        self.random_gen = random_source
        if transitions is None:
            return
        for s_init, s_next, count in transitions:
            if s_next in self.transitions[s_init]:
                raise Exception("Transition %s -> %s defined multiple"
                        + " times in initializer" % (s_init, s_next))
            self.transitions[s_init][s_next] = count
        if self.present_state not in self.transitions:
            self.present_state = self.random_gen.randrange(0, len(self.transitions))

    def _transition_dump(self):
        dump = {}
        for s, t in self.transitions.items():
            dump[s] = dict(self.transitions[s])
        return dump

    def add_transition(self, s_init, s_next):
        self.transitions[s_init][s_next] = self.transitions[s_init].get(s_next, 0) + 1

    def remove_transition(self, s_init, s_next, all=False):
        if s_init in self.transitions and s_next in self.transitions[s_init]:
            if all or self.transitions[s_init][s_next] == 1:
                del self.transitions[s_init][s_next]
                if len(self.transitions[s_init]) == 0:
                    del self.transitions[s_init]
            else:
                self.transitions[s_init][s_next] -= 1

    def set_state(self, state):
        if self.has_state(state):
            self.present_state = state
        else:
            raise Exception("No such state '%s' present" % state)

    def has_state(self, state):
        return state in self.transitions

    def has_next_state(self, state=None):
        return len(self.transitions[state if state is not None else self.present_state]) == 0

    def next_state(self):
        if self.has_next_state():
            raise Exception("Cannot transition from state \'%s\'" \
                    % self.present_state)
        size = 0
        for k, v in six.iteritems(self.transitions[self.present_state]):
           size += v
        selection = self.random_gen.randint(1, size)
        accumulator = 0
        for k, v in six.iteritems(self.transitions[self.present_state]):
            if selection <= v + accumulator:
                self.present_state = k
                return k
            accumulator += v
        raise Exception("No transition followed from state '{}' ({}/{}, {}). This is a bug." \
            .format(self.present_state, selection, size, self.transitions[self.present_state]))

    def set_random_state(self):
        self.present_state = self.random_gen.sample(self.transitions.keys(), 1)[0]
        return self.present_state

