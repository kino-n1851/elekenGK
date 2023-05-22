from django.apps import AppConfig
from multiprocessing import Process
import discordBot
#from MyNfcReader import TestNFCReader


class ElekengkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elekenGK'
    
    def ready(self):
        #nfc_ps = Process(target=TestNFCReader.run_forever)
        #discord_ps = Process(target=discordBot.run)
        #nfc_ps.start()
        #discord_ps.start()
        #print("end")
        return