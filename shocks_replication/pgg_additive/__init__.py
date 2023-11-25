from otree.api import *
import time, random

doc = """
Single group public goods game with additive shocks, played for finite number of rounds
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg_additive'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 20
    ENDOWMENT = 10.00
    MULTIPLIER = 2  # Aidin used 1.6
    RATE = 25  # 25 'points' is one dollar | Aidin used 20
    ADJUSTMENT = 5  # +/-5


class Subsession(BaseSubsession):
    def creating_session(self):
        """
        Randomly forms groups for the single group PGG experiment, partner's treatment so groupings are static for the
        duration of the experiment.
        :return: groupings for the duration of this app
        """
        if self.round_number == 1:
            Subsession.group_randomly()  # Previous had 'fixed_id_in_group=True' will see what this changes
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    total_investment = models.FloatField()
    individual_share = models.FloatField()

    realized_adjustment = models.FloatField()


class Player(BasePlayer):
    """investment = models.CurrencyField(
            min=0, max=C.ENDOWMENT, label="How much will you invest to your Group's Joint Account?"
        )"""
    investment = models.FloatField(min=0.00, max=C.ENDOWMENT, decimal_places=2,
                                   label="How much will you invest to your group's joint account?")

    personal_account = models.FloatField()
    # For history table for each player
    indiv_share = models.FloatField()
    tot_invest = models.FloatField()

    # Track decision time
    start_time = models.FloatField(initial=0)

    time_spent_invest = models.FloatField(initial=0)

    time_spent_results = models.FloatField(initial=0)

    time_spent_cumulative_results = models.FloatField(initial=0)

    # Error Tracking

    num_errors_decimal_invest = models.IntegerField(initial=0)

    num_errors_max_invest = models.IntegerField(initial=0)

    num_errors_min_invest = models.IntegerField(initial=0)

    # Payoff to Display

    payoff_to_display = models.FloatField(intial=0)


# Functions


def set_payoffs(group: Group):
    players = group.get_players()
    investments = [p.investment for p in players]
    group.total_investment = sum(investments)
    group.individual_share = (
            group.total_investment * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )

    # Additive Shock
    groups = groups = group.subsession.get_groups()
    for g in groups:
        if random.random() <= 0.5:
            g.realized_adjustment = C.ADJUSTMENT
        else:
            g.realized_adjustment = -C.ADJUSTMENT

    for p in players:
        p.payoff = (C.ENDOWMENT - p.investment + group.individual_share + group.realized_adjustment) / C.RATE
        # Since we are using decimals and oTree points must be Integers I cannot use their points feature
        p.payoff_to_display = C.ENDOWMENT - p.investment + group.individual_share + group.realized_adjustment
        p.personal_account = C.ENDOWMENT - p.investment
        p.indiv_share = group.individual_share
        p.tot_invest = group.total_investment






# PAGES
class Invest(Page):
    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def error_message(player: Player, values):
        if values['investment'] != round(values['investment'], 2):
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_invest += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_decimal_invest += 1
            return 'Your investment can have up to two numbers after the decimal (#.##).'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_invest = time.time() - player.start_time  # Save invest decision time spent




class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_results = time.time() - player.start_time  # Save results time spent


class CumulativeResults(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        cumulative_payoff = sum([p.payoff_to_display for p in player.in_all_rounds() if p.payoff_to_display])

        return {'cumulative_payoff': cumulative_payoff}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_cumulative_results = time.time() - player.start_time  # Save cumulative results time spent


page_sequence = [Invest,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
