from django.apps import AppConfig


class UamConfig(AppConfig):
    name = 'UAM'

    def ready(self):
    	import UAM.signals
