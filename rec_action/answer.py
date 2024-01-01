import logging
from rec_action.rec_action import RecAction
from state.state_manager import StateManager
from user_intent.inquire import Inquire
from state.message import Message
from rec_action.response_type.answer_prompt_based_resp import AnswerPromptBasedResponse

logger = logging.getLogger('answer')


class Answer(RecAction):
    """
    Class representing Answer recommender action.

    :param answer_response: object used to generate the response
    :param priority_score_range: range of priority score for this rec action
    """
    _answer_response: AnswerPromptBasedResponse

    def __init__(self, answer_response: AnswerPromptBasedResponse, priority_score_range: tuple[float, float] = (1, 10)) -> None:
        super().__init__(priority_score_range)
        self._answer_response = answer_response

    def get_name(self) -> str:
        """
        Returns the name of this recommender action.

        :return: name of this recommender action
        """
        return "Answer"

    def get_description(self) -> str:
        """
        Returns the description of this recommender action.

        :return: description of this recommender action
        """
        return "Recommender answers the question issued by the user"

    def get_priority_score(self, state_manager: StateManager) -> float:
        """
        Returns the score representing how much this is appropriate recommender action for the current conversation.

        :param state_manager: current state representing the conversation
        :return: score representing how much this is appropriate recommender action for the current conversation.
        """
        if state_manager.get("unsatisfied_goals") is not None:
            for goal in state_manager.get("unsatisfied_goals"):
                if isinstance(goal["user_intent"], Inquire):
                    return self.priority_score_range[0] + goal["utterance_index"] / len(state_manager.get("conv_history")) * (self.priority_score_range[1] - self.priority_score_range[0])
        return self.priority_score_range[0] - 1

    def get_response(self, state_manager: StateManager) -> str | None:
        """
        Return recommender's response corresponding to this action.

        :param state_manager: current state representing the conversation
        :return: recommender's response corresponding to this action
        """
        return self._answer_response.get(state_manager)

    def is_response_hard_coded(self) -> bool:
        """
        Returns whether hard coded response exists or not.

        :return: whether hard coded response exists or not.
        """
        return False

    def update_state(self, state_manager: StateManager, response: str, **kwargs) -> None:
        """
        Updates the state based off of recommenders response

        :param state_manager: current state representing the conversation
        :param response: recommender response msg that is returned to the user
        :param kwargs: misc. arguments
        """
        message = Message("recommender", response)
        state_manager.update_conv_history(message)