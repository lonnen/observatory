DEBUG = False
LOGGING_CONF = "logging.conf"
LOGGER_NAME = "observatory"

# this is a redis url "redis://localhost:6379"
REDISTOGO_URL = ""


ENVIRONMENTS = {
    # 'name': 'url'
    'prod': 'https://crash-stats.mozilla.com/status/json',
    'stage': 'https://crash-stats.allizom.org/status/json',
    'dev': 'https://crash-stats-dev.allizom.org/status/json'
}
