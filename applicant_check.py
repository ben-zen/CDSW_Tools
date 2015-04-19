# Copyright (C) 2015 Ben Lewis
# Licensed under the MIT license
# Tool for checking if an applicant (using their email address) was accepted to
# a CDSW session, based on the session file.

import argparse
import cdsw
import os
import pickle
import sys

parser = argparse.ArgumentParser()

parser.add_argument("SessionFile", help="The file used to check if an e-mail address was present.")
parser.add_argument("ApplicantAddress", help="The e-mail address being checked.")

args = parser.parse_args()

if not os.path.isfile(args.SessionFile):
    print("No session file at {0}.".format(args.SessionFile))
    sys.exit(os.EX_IOERR)
elif not os.access(args.SessionFile, os.R_OK):
    print("Cannot read session file at {0}.".format(args.SessionFile))
    sys.exit(os.EX_IOERR)

data_file = open(args.SessionFile, "rb")
session_data = pickle.load(data_file)
data_file.close()

try:
    applicant_status = session_data.Get_applicant_status(args.ApplicantAddress)
    if applicant_status is cdsw.ApplicantStatus.Accepted:
        print("Accepted!")
    else:
        print("Waitlisted for this session.")
except ma as MissingAddressException:
    print("The email address {0} was not found in the session.".format(ma.EmailAddress))
