from otree.api import *
import time

doc = """
Instructions and Comprehension Questions for the baseline pgg
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg_base_instrucs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_PERIODS = 20
    ENDOWMENT = 10.00


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# Function for Comp Q for Player Class

def make_comprehension_question(label):
    """
    Reduces code repetition for creation of comprehension questions
    :param label: the message to be displayed to participants for a given question
    :return: an input field that can be displayed on a page that participants can interact with
    """
    return models.FloatField(label=label)


class Player(BasePlayer):

    # Comprehension Questions
    comprehension_question_one = make_comprehension_question("In each period, how many tokens will you"
                                                             " receive that you can decide how to invest to"
                                                             " your Group's Joint Account and your Personal Account?")
    comprehension_question_two = models.IntegerField(
        choices=[
            [1, 'True'],
            [2, 'False'],
        ], label="True or False",
        widget=widgets.RadioSelect
    )
    comprehension_question_three_a = models.FloatField(
        label="What is the minimum amount you can invest in your group's"
              " joint account?")
    comprehension_question_three_b = models.FloatField(
        label="What is the maximum amount you can invest in your group's"
              " joint account?")

    # Qs Regarding Earnings
    comprehension_question_four_a = make_comprehension_question("What are your earnings from the Group's Joint"
                                                                " Account?")
    comprehension_question_four_b = make_comprehension_question("With the specified investment to your Group's Joint "
                                                                "Account, how much do you invest to your Personal "
                                                                " Account?")
    comprehension_question_four_c = make_comprehension_question("What are your Period Earnings?")

    # Time to answer questions
    time_to_answer = models.IntegerField(initial=300)  # 5 minutes

    # Time Tracking
    start_time = models.FloatField(initial=0)

    time_spent_instrucs = models.FloatField(initial=0)

    time_spent_compqs = models.FloatField(initial=0)

    # Error Tracking
    num_errors_q_one = models.IntegerField(initial=0)

    num_errors_q_two = models.IntegerField(initial=0)

    num_errors_q_three_a = models.IntegerField(initial=0)
    num_errors_q_three_b = models.IntegerField(initial=0)

    num_errors_q_four_a = models.IntegerField(initial=0)
    num_errors_q_four_b = models.IntegerField(initial=0)
    num_errors_q_four_c = models.IntegerField(initial=0)


# PAGES


class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Save instructions time
        player.time_spent_instrucs = time.time() - player.start_time
        # reset start_time to time next page
        player.start_time = time.time()
        if player.time_spent_compqs is None:
            player.time_spent_compqs = 0


class ComprehensionQuestions(Page):

    form_model = 'player'
    form_fields = ['comprehension_question_one', 'comprehension_question_two',
                   'comprehension_question_three_a', 'comprehension_question_three_b',
                   'comprehension_question_four_a', 'comprehension_question_four_b',
                   'comprehension_question_four_c']
    timer_text = 'Time left to complete the quiz'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_one'] != 10:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_one += 1
            return 'Reconsider your answer to question one. In each period you will receive 10 tokens that you can choose to invest to your group account or' \
                   ' your personal account.'
        if values['comprehension_question_two'] != 1:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_two += 1
            return 'Reconsider your answer to question two. The participants in your group are the same for all periods.'
        if values['comprehension_question_three_a'] != 0:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_three_a += 1
            return 'Reconsider your answer to question three A. Your minimum investment to your group account would be investing nothing – 0 tokens – in a period.'
        if values['comprehension_question_three_b'] != 10:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_three_b += 1
            return 'Reconsider your answer to question three B. Each period you receive 10 tokens that you choose how to invest between your Personal Account, and' \
                   ' your group. At most you could invest all 10 tokens to one account.'
        if values['comprehension_question_four_a'] != 11:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_a += 1
            return 'Reconsider your answer to question four A: You invested 5.5 tokens to the Joint Account and your other group' \
                   ' members invested 16.5 tokens. Your Individual Share is the sum of these two multiplied by 0.5.'
        if values['comprehension_question_four_b'] != 4.5:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_b += 1
            return 'Reconsider your answer to question four B: Your Personal Account is the tokens you receive each ' \
                   'period (10 tokens) minus your investment to the Joint Account (5.5 tokens in this example).'
        if values['comprehension_question_four_c'] != 15.5:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_compqs += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_c += 1
            return 'Reconsider your answer to question four C: Your Period Earnings are the sum of your earnings from the Joint Account' \
                   ' and your Personal Account. (If you answered four A and B correctly, sum those two answers).'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_compqs += elapsed_time


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions,
                 ComprehensionQuestions,
                 Results,
                 ResultsWaitPage]
