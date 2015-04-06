"""
@package transition
This describes how a transition looks
"""
class Transition:
    """
    @brief Transitions are used in the DFSM to show transition functions
    """
    def __init__(self, start_state, input, next_state):
        """
        @brief The Constructor

        @param[in] start_state An int representing the state the DFSM should be in for this transition
        @param[in] input A string that is 1 char long representing the input needed for transition function
        @param[in] next_state An int that represents the state the the DFSM should be in after transition occurs
        """
        self.start_state = start_state
        self.input = input
        self.next_state = next_state

    
