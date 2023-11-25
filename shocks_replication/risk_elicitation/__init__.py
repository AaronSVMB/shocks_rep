from otree.api import *
import random, time

doc = """
Holt Laury Risk Elicitation
"""


class C(BaseConstants):
    NAME_IN_URL = 'RiskElicitation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    LOTTERY_A_LOW = 1  # 1 dollar with current conversion #TODO Change these values with this exp.s conversion rate
    LOTTERY_A_HIGH = 3  # 3 dollars with current conversion
    LOTTERY_B_LOW = 0.1  # 10 cents with current conversion
    LOTTERY_B_HIGH = 5  # 5 dollars with current conversion


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# Functions

def make_lottery_option(label):
    return models.IntegerField(
        label=label,
        choices=[
            [1, 'A'],
            [2, 'B']
        ],
        widget=widgets.RadioSelectHorizontal
    )


class Player(BasePlayer):
    lottery_b_one = make_lottery_option("$0.1 with probability 9/10 or $5 with probability 1/10")
    lottery_b_two = make_lottery_option("$0.1 with probability 8/10 or $5 with probability 2/10")
    lottery_b_three = make_lottery_option("$0.1 with probability 7/10 or $5 with probability 3/10")
    lottery_b_four = make_lottery_option("$0.1 with probability 6/10 or $5 with probability 4/10")
    lottery_b_five = make_lottery_option("$0.1 with probability 5/10 or $5 with probability 5/10")
    lottery_b_six = make_lottery_option("$0.1 with probability 4/10 or $5 with probability 6/10")
    lottery_b_seven = make_lottery_option("$0.1 with probability 3/10 or $5 with probability 7/10")
    lottery_b_eight = make_lottery_option("$0.1 with probability 2/10 or $5 with probability 8/10")
    lottery_b_nine = make_lottery_option("$0.1 with probability 1/10 or $5 with probability 9/10")
    lottery_b_ten = make_lottery_option("$0.1 with probability 0/10 or $5 with probability 10/10")

    chosen_lottery = models.IntegerField()
    relevant_choice = models.IntegerField()
    relevant_choice_as_string = models.StringField()

    # Track decision time

    start_time = models.FloatField(initial=0)

    time_spent_lottery = models.FloatField(initial=0)

    time_spent_results = models.FloatField(initial=0)


# Functions for Payoff

def make_lottery_b_dictionary(player: Player):
    lottery_b_dictionary = {
        1: player.lottery_b_one,
        2: player.lottery_b_two,
        3: player.lottery_b_three,
        4: player.lottery_b_four,
        5: player.lottery_b_five,
        6: player.lottery_b_six,
        7: player.lottery_b_seven,
        8: player.lottery_b_eight,
        9: player.lottery_b_nine,
        10: player.lottery_b_ten
    }
    return lottery_b_dictionary


def calc_payoffs(subsession: Subsession):
    players = subsession.get_players()
    for p in players:
        lottery_b_dict = make_lottery_b_dictionary(p)
        lottery_ids = [i + 1 for i in range(len(lottery_b_dict))]
        salient_lottery = random.choice(lottery_ids)
        p.chosen_lottery = salient_lottery
        relevant_decision = lottery_b_dict[salient_lottery]
        p.relevant_choice = relevant_decision
        # store the choice as A or B to be displayed to subjects
        if relevant_decision == 1:
            p.relevant_choice_as_string = 'A'
        else:
            p.relevant_choice_as_string = 'B'
        # Calc payoff via random draw
        if relevant_decision == 1:
            if random.random() < 1 / 2:
                p.payoff = C.LOTTERY_A_LOW
            else:
                p.payoff = C.LOTTERY_A_HIGH
        else:
            if random.random() < (10 - salient_lottery)/10:
                p.payoff = C.LOTTERY_B_LOW
            else:
                p.payoff = C.LOTTERY_B_HIGH


# PAGES


class StartPage(Page):
    pass


class RiskPreference(Page):
    form_model = 'player'
    form_fields = ['lottery_b_one', 'lottery_b_two', 'lottery_b_three', 'lottery_b_four',
                   'lottery_b_five', 'lottery_b_six', 'lottery_b_seven', 'lottery_b_eight',
                   'lottery_b_nine', 'lottery_b_ten']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_lottery = time.time() - player.start_time  # Save invest decision time spent



class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = calc_payoffs


class Results(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    """@staticmethod  # Used for MGPGG not needed here
    def vars_for_template(player: Player):
        return {
            'payoff_in_usd': float(player.payoff) / 50
        }"""

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_results = time.time() - player.start_time  # Save results time spent


page_sequence = [StartPage,
                 RiskPreference,
                 ResultsWaitPage,
                 Results]
