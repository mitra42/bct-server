# the module contains the client and server process to manage ids

import hashlib
import string
import random
import time
import logging
import datetime

logger = logging.getLogger(__name__)

def hash_seed(seed):
    return hashlib.sha1(seed.encode()).hexdigest()


def fold_hash(hash40):
    return "%X" % (int(hash40[:20], 16) ^ int(hash40[20:], 16))


def random_ascii(length):
    # noinspection PyUnusedLocal
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])


def new_seed(seed_string=None):
    if not seed_string:
        seed_string = random_ascii(8)
    return hash_seed(seed_string)  # first hash_seed is to get size same as updates

def get_provider_seed_string(provider_id, test_id, pin):
    # Return X a string that can be calculated by an infected person or test provider but noone else
    return hash_seed(provider_id + test_id + pin)

def get_id_for_provider(provider_seed_string):
    # Generate an id that the provider can also generate
    return hash_seed(provider_seed_string + "TESTING").upper()

# This group of functions centralize the process and cryptography for seed -> replacement_token -> update_token

# Generate Replacement token from seed + n (which should increment)
# Requirements - none reversible, cannot be used to find the seed, or any other replacement_token
def replacement_token(seed, n):
    return hash_seed(seed + str(n))


# Generate Update Token from Replacement Token
# Requirements: Not reversible, confirmable
# i.e. updateToken(rt) == ut shows that you possess the original rt used to create ut
def get_update_token(rt):
        return fold_hash(hash_seed(rt))

# Check that the rt is a correct rt for the ut.
def confirm_update_token(ut, rt):
    return get_update_token(rt) == ut


# override_time_for_testing is a variable that CAN be set in testing mode (useful in testing so we remove randomness and allow tests
# without sleeping)
override_time_for_testing = False


# Return time in floating seconds,
# Can be overridden, but strange that it goes through a global variable ! )
def current_time():
    global override_time_for_testing
    if override_time_for_testing:
        return override_time_for_testing
    else:
        return time.time()


def set_current_time_for_testing(floating_seconds):
    global override_time_for_testing
    override_time_for_testing = floating_seconds
    return


def inc_current_time_for_testing(delta_seconds=1):
    global override_time_for_testing
    override_time_for_testing += delta_seconds
    return


def unix_time_from_iso(iso_string):
    """ convert an iso 8601 time to floating seconds since epoch """
    return datetime.datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp()


def iso_time_from_seconds_since_epoch(seconds_since_epoch):
    return datetime.datetime.utcfromtimestamp(seconds_since_epoch).isoformat() + 'Z'
