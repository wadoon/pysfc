from collections import defaultdict

__author__ = 'weigl'


class SFC(object):
    TRANSITIONS = []
    STATES = []

    def __init__(self):
        self._states = dict()
        self._transitions = defaultdict(list)

        self._old_states = set()
        self._current_states = set()

        self._build_states()
        self._build_transition()


    def _build_states(self):
        empty_fn = lambda: None

        def getfn(name):
            if hasattr(self, name):
                return getattr(self, name)
            else:
                return empty_fn


        self._current_states.add(self.STATES[0])

        for s in self.STATES:
            a = (getfn(s + "_entry"), getfn(s + "_active"), getfn(s + "_exit"))
            self._states[s] = a

    def _build_transition(self):
        plain_transitions = self.TRANSITIONS

        true = lambda: True

        def parse_states(string):
            states = string.split("|")
            return frozenset(states)

        for t in plain_transitions:
            if len(t) == 2:
                start, stop = t
                fname = "guard_%s_%s" % t
            else:
                start, stop, fname = t

            if isinstance(fname, str) and hasattr(self, fname):
                fn = getattr(self, fname)
            elif callable(fname):
                fn = fname
            else:
                fn = true

            self._transitions[parse_states(start)].append((parse_states(stop), fn))

    @property
    def states(self):
        return self._states

    @property
    def transitions(self):
        return self._transitions

    def _execute(self, states, idx):
        for s in states:
            actions = self._states[s]
            a = actions[idx]
            print "Execute: %s(%d)" % (s, idx)
            a()


    def __call__(self):
        new_states = self._current_states - self._old_states

        self._execute(new_states, 0)
        self._execute(self._current_states, 1)

        self._old_states = frozenset(self._current_states)
        states = set(self._current_states)
        self._current_states.clear()



        for start, seq in self._transitions.items():
            if len(states) == 0:
                break

            if start <= states:
                for target, guard in seq:
                    if guard():
                        self._current_states |= target
                        states -= start

        self._current_states |= states

        left_states = self._old_states - self._current_states

        self._execute(left_states, 2)
