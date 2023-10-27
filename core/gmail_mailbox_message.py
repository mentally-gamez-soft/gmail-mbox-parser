import mailbox
from core.helpers import get_html_text,sanitize_text,is_email

class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data
        self.emails = []

    def add_email(self,text):
        if is_email(text):
            self.emails.append(text)

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        email_text = self.read_email_payload()
        #if email_text[0][2]:
        #    return {'complete_message':email_text, 'readlines':(email_text[0][2]).split('\n')}
        return email_text

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list,tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)

    
def main(*args, **kwargs):
    print('args -----')
    print(args)
    print('-----')

    print('kwargs -----')
    print(kwargs)
    print('-----')

    mbox_obj = mailbox.mbox('data/Messages.mbox')
    num_entries = len(mbox_obj)

    messages = []
    f1 = open("data/" + kwargs['spam'], "w")
    f2 = open("data/" + kwargs['spam_line'], "w")

    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        result = email_data.parse_email()[0][2] 
        print('Parsing email {0} of {1}'.format(idx, num_entries)) 

        if result:
            f1.write('\n')
            # f2.write('\n')
            result1 = '\"spam\","' + sanitize_text(result) + '",\"\",\"\",\"\"\n'
            line_result = ['\"spam\","' + x + '",\"\",\"\",\"\"' + '\n' for x in result.split('\n') ]
            # messages.append(result)
            f1.write(result1)
            for line in line_result:
                f2.write(line)
                email_data.add_email(line)
        else:
            print('None found')

    f1.close()
    f2.close()

    # for msg in messages:
    #     #print(msg[0][2])
    #     print(msg)
    print(email_data.emails)