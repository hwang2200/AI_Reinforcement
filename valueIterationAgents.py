# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        for i in range(self.iterations):
            #Out-of-place iteration
            tempValues = util.Counter()

            states = self.mdp.getStates()
            #print(states)
            for state in states:
                #Handle if terminal state, because it stores -inf otherwise
                if self.mdp.isTerminal(state):
                    tempValues[state] = 0
                #Find max q value for each action
                else:
                    qValue = float("-inf")
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        qValue = max(qValue, self.computeQValueFromValues(state, action))
                    tempValues[state] = qValue
            self.values = tempValues
        #print(self.values)

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        qValue = 0
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for stateAndProb in statesAndProbs:
            reward = self.mdp.getReward(state, action, stateAndProb[0])
            #print(reward)
            nextStateValue = self.getValue(stateAndProb[0])
            #print(nextStateValue)
            #print(stateAndProb[1])
            qValue += stateAndProb[1] * (reward + (self.discount * nextStateValue))
        #print(qValue)
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        bestAction = None
        actions = self.mdp.getPossibleActions(state)
        #print(actions)

        #If terminal state, return none
        if self.mdp.isTerminal(state):
            return bestAction
        else:
            qValue = float("-inf")
            actions = self.mdp.getPossibleActions(state)
            #If no legal actions, return none
            if len(actions) == 0:
                return bestAction
            else:
                for action in actions:
                    #Return action associated with max qValue
                    if self.computeQValueFromValues(state, action) > qValue:
                        qValue = self.computeQValueFromValues(state, action)
                        bestAction = action
        return bestAction


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()
        index = 0
        for i in range(self.iterations):
            state = states[index]
            #Handle if terminal state, because it stores -inf otherwise
            if self.mdp.isTerminal(state):
                self.values[state] = 0
            #Find max q value for each action
            else:
                qValue = float("-inf")
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    qValue = max(qValue, self.computeQValueFromValues(state, action))
                self.values[state] = qValue
            index += 1
            if index > len(states) - 1:
                index = 0
        #self.values = tempValues


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

