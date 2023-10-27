import mailbox
from core.gmail_mailbox_message import GmailMboxMessage

mbox_obj = mailbox.mbox('data/Messages.mbox')

num_entries = len(mbox_obj)

for idx, email_obj in enumerate(mbox_obj):
    email_data = GmailMboxMessage(email_obj)
    email_data.parse_email()
    print('Parsing email {0} of {1}'.format(idx, num_entries))