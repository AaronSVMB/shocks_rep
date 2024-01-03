from otree.api import *
import time
import math

doc = """
Questionnaire for the base and additive random public goods game
"""

class C(BaseConstants):
    NAME_IN_URL = 'survey_base'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    password_to_start = models.StringField()

    # Demographic // Basic Qs

    major = models.IntegerField(
        choices=[
            [1, 'Math, Engineering, or the Physical Sciences'],
            [2, 'Business or Economics'],
            [3, 'English, Foreign Languages, or Classics'],
            [4, 'Humanities'],
            [5, 'Other']
        ],
        label='1. What is your major?',
        widget=widgets.RadioSelect
    )

    gender = models.IntegerField(
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, "Other"]
        ],
        label="2. What is your gender?",
        widget=widgets.RadioSelect
    )

    grade = models.IntegerField(
        choices=[
            [1, 'Freshman'],
            [2, 'Sophomore'],
            [3, 'Junior'],
            [4, 'Senior'],
            [5, 'Graduate']
        ],
        label="3. What year are you in?",
        widget=widgets.RadioSelect
    )

    # Short-Answer Qs

    personal_versus_group = models.LongStringField(label="4. In a few sentences, please explain what led you to invest"
                                                         " more or less of your endowment in your personal account"
                                                         " versus the group account. Be as specific as possible.")

    change = models.LongStringField(label="5. In a few sentences, please explain what led you to change how much you"
                                          " invested in the group account over time. Be  as specific as possible.")

    # Scale

    reason_own = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would maximize my own overall earnings."
    )

    reason_group = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would maximize the group's overall earnings."
    )

    reason_conditional = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would encourage other group members to make large investments"
              " to the group account."
    )

    reason_experiment = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I experimented with different levels of investment in the group account to see how it would affect what"
              " the other members invested."
    )

    reason_adjust = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I adjusted my own investment to the group account based on what the other members were investing in the"
              " group account."
    )

    reason_future_rounds = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="The size of my investment in the group account influenced how much the other group members invested in"
              " the following period."
    )

    # 7 Decision-Making Style

    decision_style_facts = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Never'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='When making important decisions I focus on facts and logic.'
    )

    decision_style_feelings = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Never'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='When making important decisions I trust my feelings and intuition.'
    )

    decision_style_religious = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Never'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='When making important decisions I consult with religious or spiritual leaders.'
    )

    decision_style_family = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Almost Never']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="When making important decisions, I consult with one or more family members."
    )

    # Final

    clarity = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree']
        ],
        label='8. The instructions for the experiment were clear and easy to follow',
        widget=widgets.RadioSelectHorizontal
    )

    suggestions = models.LongStringField(label='9. Thank you for completing this experiment. We value your feedback, '
                                            'so please use the following text box for comments or suggestions')

    # Track Time

    start_time = models.FloatField(initial=0)

    time_spent_survey_one = models.FloatField(initial=0)

    time_spent_survey_two = models.FloatField(initial=0)

    time_spent_survey_three = models.FloatField(initial=0)

    time_spent_survey_four = models.FloatField(initial=0)


# PAGES
class ThankYou(Page):
    form_model = 'player'
    form_fields = ['password_to_start']

    def error_message(player: Player, values):
        if values['password_to_start'] != 'Questionnaire':
            return 'Check your spelling or ask the experimenter for help'

    def vars_for_template(self):
        # Assuming that payoffs have been accumulated in participant.payoff
        total_earnings_no_show_up = self.participant.payoff
        rounded_earnings_no_show_up = math.ceil(total_earnings_no_show_up)
        total_earnings = self.participant.payoff_plus_participation_fee()
        # Round up to the nearest dollar
        rounded_earnings = math.ceil(total_earnings)

        self.participant.payoff = math.ceil(self.participant.payoff)

        return {
            'rounded_earnings_no_show_up': rounded_earnings_no_show_up,
            'rounded_earnings': rounded_earnings,
        }


class SurveyOne(Page):
    form_model = 'player'
    form_fields = ['major', 'gender', 'grade', 'personal_versus_group', 'change']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_one = time.time() - player.start_time  # Save invest decision time spent


class SurveyTwo(Page):
    form_model = 'player'
    form_fields = ['reason_own', 'reason_group', 'reason_conditional',
                   'reason_experiment', 'reason_adjust', 'reason_future_rounds']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_two = time.time() - player.start_time  # Save invest decision time spent


class SurveyThree(Page):
    form_model = 'player'
    form_fields = ['decision_style_facts', 'decision_style_feelings',
                   'decision_style_family', 'decision_style_religious']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_three = time.time() - player.start_time  # Save invest decision time spent


class SurveyFour(Page):
    form_model = 'player'
    form_fields = ['clarity', 'suggestions']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_four = time.time() - player.start_time  # Save invest decision time spent


class EndPage(Page):
    pass


page_sequence = [ThankYou,
                 SurveyOne,
                 SurveyTwo,
                 SurveyThree,
                 SurveyFour,
                 EndPage]
