import nfc
import binascii
import requests
from requests import HTTPError 
import os
from dotenv import load_dotenv

NFC_READER_ID = "usb:054c:06c3"
load_dotenv()
app_url = os.environ["APP_URL"]

class NFCReader:
    def on_connect(self, tag):
        idm = binascii.hexlify(tag._nfcid).decode()
        return self.on_read(idm)
    
    def on_read(self, idm):
        return True

    def read(self):
        clf = nfc.ContactlessFrontend(NFC_READER_ID)
        try:
            clf.connect(rdwr={"on-connect": self.on_connect})
        finally:
            clf.close()
    
    

class TestNFCReader(NFCReader):
    
    def on_read(self, idm):
        print(f"iDm detected: {idm}")
        try:
            response = requests.post(f"{app_url}/touch", data={"nfc_iDm":str(idm)})
            print(response.content)
            if response.status_code != 200:
                print(f"[nfcReader]:connection with server doesn't success.\n {response.status_code=}") 
        except HTTPError as e:
            pass
            print(e)
        return True

    @classmethod
    def run_forever(cls):
        client = cls()
        while True:
            client.read() 
        

if __name__ == "__main__":
    TestNFCReader.run_forever()