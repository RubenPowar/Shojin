# import time
# from itertools import chain
# import email
# import imaplib
# import base64
# import os
# import re
#
# imap_ssl_host = 'outlook.office365.com'
# imap_ssl_port = 993
# username = 'ruben.powar@shojin.co.uk'
# password = 'nyjryt-wytZuw-hiwky4'
#
# # if need to restrict mail search.
# criteria = {}
# uid_max = 0
#
# def search_string(uid_max, criteria):
#     c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
#     return '(%s)' % ' '.join(chain(*c))
#     # Produce search string in IMAP format:
#     #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)
# #Get any attachemt related to the new mail
#
# #Getting the uid_max, only new email are process
#
# #login to the imap
# mail = imaplib.IMAP4_SSL(imap_ssl_host)
# mail.login(username, password)
# #select the folder
# mail.select('inbox')
#
# result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
# uids = [int(s) for s in data[0].split()]
# if uids:
#     uid_max = max(uids)
#     # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.
# #Logout before running the while loop
# print(uid_max)
# mail.logout()
# while 1:
#     mail = imaplib.IMAP4_SSL(imap_ssl_host)
#     mail.login(username, password)
#     mail.select('inbox')
#     result, data = mail.uid('search', None, search_string(uid_max, criteria))
#     uids = [int(s) for s in data[0].split()]
#
#     for uid in uids:
#         # Have to check again because Gmail sometimes does not obey UID criterion.
#         if uid > uid_max:
#             result, data = mail.uid('fetch', str(uid), '(RFC822)')
#             for response_part in data:
#                 if isinstance(response_part, tuple):
#                     #message_from_string can also be use here
#                     print(email.message_from_bytes(response_part[1])) #processing the email here for whatever
#             uid_max = uid
# mail.logout()
# time.sleep(1)

import imaplib, email, getpass
from email import policy

imap_host = 'outlook.office365.com'
imap_user = 'ruben.powar@shojin.co.uk'

# init imap connection
mail = imaplib.IMAP4_SSL(imap_host, 993)
rc, resp = mail.login(imap_user, getpass.getpass())

# select only unread messages from inbox
mail.select('Inbox')
status, data = mail.search(None, '(UNSEEN)')

# for each e-mail messages, print text content
for num in data[0].split():
    # get a single message and parse it by policy.SMTP (RFC compliant)
    status, data = mail.fetch(num, '(RFC822)')
    email_msg = data[0][1]
    email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

    print("\n----- MESSAGE START -----\n")

    print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % (
        str(email_msg['From']),
        str(email_msg['To']),
        str(email_msg['Date']),
        str(email_msg['Subject'] )))

    # print only message parts that contain text data
    for part in email_msg.walk():
        if part.get_content_type() == "text/plain":
            for line in part.get_content().splitlines():
                print(line)

    print("\n----- MESSAGE END -----\n")

#   todo
#       1.get IMAP permissions
#       2.test monitoring of emails
#       3.get attachments
#       4.
#       5.
#       6.
