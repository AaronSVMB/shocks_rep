from os import environ
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rooms_file_path = os.path.join(BASE_DIR, '_rooms', 'rooms.txt')

SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods'],
    #     num_demo_participants=3,
    # ),
    dict(name='pgg_base_full',
         display_name='pgg_base_full_experiment',
         app_sequence=['pgg_base_instrucs', 'pgg_base', 'risk_elicitation', 'survey_base'],
         num_demo_participants=8),
    dict(name='pgg_additive_random_full',
             display_name='pgg_additive_random_full_experiment',
             app_sequence=['pgg_additive_random_instrucs', 'pgg_additive', 'risk_elicitation', 'survey_additive_ambiguous'],
             num_demo_participants=8),
    dict(name='pgg_additive_ambig_full',
             display_name='pgg_additive_ambiguous_full_experiment',
             app_sequence=['pgg_additive_ambiguous_instrucs', 'pgg_additive', 'risk_elicitation', 'survey_additive_ambiguous'],
             num_demo_participants=8),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=10.00, doc=""
)

ROOMS = [
    dict(
        name='gmu_lab',
        display_name='Experimental Sessions',
        participant_label_file=rooms_file_path,
        use_secure_urls=False,
    ),
]

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'TestPassword'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6869605823954'
