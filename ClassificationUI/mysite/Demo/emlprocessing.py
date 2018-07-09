import email
class EML:
    def __init__(self):
        self.msg=''
        self.name=''
        self.subject=''
        self.body=''
        self.from_=''
        self.to=''
    def parse_eml(self,name):
        self.msg=email.message_from_file(open(name,'r'))
        self.subject=self.msg.__getitem__('subject')
        self.from_=self.msg.__getitem__('From')
        self.to=self.msg.__getitem__('To')
        if self.msg.is_multipart():
            for payload in self.msg.get_payload():
                if payload.get_content_maintype()=='text':
                    self.body=payload.get_payload()
        else:
            self.body=''

        self.name=name
if __name__=='__main__':
    eml=EML()
    eml.parse_eml('./Dataset/3.eml')
    print(eml.name)
    print(eml.subject)
    print(eml.body)
    print(eml.to)
    print(eml.from_)