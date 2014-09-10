"""More demo code analyzing PGP Survey data.

Prints to stdout a list of all huIDs that have completed the PGP Participant
Survey and all twelve Trait and Disease surveys.
"""

import pgp_survey

SURVEYS_DIR = 'surveys_20140910'

# Input trait surveys and list of traits.
trait_surveys, trait_survey_traits = pgp_survey.get_trait_surveys(SURVEYS_DIR)

# Input participant survey.
participant_survey = pgp_survey.get_participant_survey(SURVEYS_DIR)

# Use splat to get the intersection of sets returned by get_huIDs().
in_all_surveys = trait_surveys[0].get_huIDs().intersection(
    *[x.get_huIDs() for x in trait_surveys])
huID_list = list(in_all_surveys)
huID_list.sort()

# Output participant ID and 'Y' for every trait a participant has.
for huID in huID_list:
    if huID in participant_survey.by_huID:
        print huID
