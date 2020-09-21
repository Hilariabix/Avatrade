from django.apps import AppConfig


class SocialNetworkConfig(AppConfig):
    name = 'avatrade.social_network'

    hunter = {
        'url': 'https://api.hunter.io/v2',
        'key': 'bc5dbf086ec7cb2bb9da0c006bec81a2c7b6f654',
    }

    clearbit = {
        'key': 'sk_9a4ce672414f180880ba4e87aba8c4c7'
    }
