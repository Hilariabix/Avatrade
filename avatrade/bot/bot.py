import random
import secrets

import logging
import string
import yaml
import requests
import json


BOT_CONFIG_FILE_PATH = 'bot_config.yaml'
PASSWORD_LEN = 20

logger = logging.getLogger(__name__)


def init_logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


class Bot(object):

    def __init__(self, config_path):
        self._users_credentials = {}  # email : {password, access-token, refresh-token}
        config = self._load_configuration(config_path)
        self.hunter = config['hunter']
        self.api = config['social_network']
        self.bot = config['bot']

    @staticmethod
    def _load_configuration(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config


    def get_domain_emails(self, domain):
        url = f'{self.hunter["url"]}/domain-search?domain={domain}&api_key={self.hunter["key"]}'
        response = requests.get(url)

        if response.ok:
            data = json.loads(response.content)
            emails = data['data']['emails']
            valid_emails = [email['value'] for email in emails if email['verification']['status'] == 'valid']
            logger.debug(f'{len(emails)} email addresses found, {len(valid_emails)} are valid')
            return valid_emails
        else:
            response.raise_for_status()

    def create_users_and_posts(self):
        number_of_users = self.bot['number_of_users']
        logger.info(f'Signing up {number_of_users} users')

        emails = self.get_domain_emails(self.bot['email_pool_domain'])

        if number_of_users > len(emails):
            raise RuntimeError(f'Got {len(emails)} valid emails addresses from {self.bot["email_pool_domain"]} domain,'
                               f'but at least {number_of_users} are required according to the configuration.'
                               f'Please change the number_of_users or the email_pool_domain')

        for i in range(number_of_users):
            user_id = self._signup(email=emails[i])
            self.create_user_posts(user_id)

    def _signup(self, email):
        password = self.generate_password()
        url = f'{self.api["url"]}/{self.api["signup"]}/?'
        response = requests.post(url, json={'email': email, 'password': password})

        if not response.ok:
            response.raise_for_status()

        data = json.loads(response.content)
        self._users_credentials[data['user_id']] = {
            'email': email,
            'password': password,
            'access-token': data['access'],
            'refresh-token': data['refresh'],
        }
        return data['user_id']

    def _login(self, email=None, password=None, user_id=None):
        if not ((email and password) or user_id):
            raise RuntimeError('email and password or user_id must be provided')
        if user_id:
            creds = self._users_credentials[user_id]
            email, password = creds['email'], creds['password']

        url = f'{self.api["url"]}/{self.api["login"]}/'
        response = requests.post(url, json={'email': email, 'password': password})

        if not response.ok:
            response.raise_for_status()

        data = json.loads(response.content)
        self._users_credentials[data['user_id']] = {
            'email': email,
            'password': password,
            'access-token': data['access'],
            'refresh-token': data['refresh'],
        }
        return data['user_id']

    def create_user_posts(self, user_id):
        creds = self._users_credentials.get(user_id)
        if not creds:
            return RuntimeError(f'Unknown user {creds["email"]}, please sign it up before trying to create posts in it behalf')

        number_of_posts = random.randint(1, self.bot['max_posts_per_user'] + 1)
        logger.info(f'Creating {number_of_posts} posts on behalf of {creds["email"]}')

        for _ in range(number_of_posts):
            content_length = random.randint(1, self.bot['max_post_content_length'] + 1)
            content = ''.join(random.choices(string.ascii_letters + string.digits, k=content_length))

            url = f'{self.api["url"]}/{self.api["posts"]}/'
            response = requests.post(url, json={'content': content},
                                     headers={'Authorization': f'Bearer {creds["access-token"]}'})

            if not response.ok:
                response.raise_for_status()

    def _get_all_posts(self, user_id=None):
        if user_id is None:
            user_id = list(self._users_credentials.keys())[0]
        token = self._users_credentials[user_id]["access-token"]
        url = f'{self.api["url"]}/{self.api["posts"]}/'
        response = requests.get(url, headers={'Authorization': f'Bearer {token}'})

        if not response.ok:
            response.raise_for_status()

        data = json.loads(response.content)
        return data

    def _like(self, user_id, post_id):
        creds = self._users_credentials.get(user_id)
        url = f'{self.api["url"]}/{self.api["likes"]}/'
        response = requests.post(url, json={'post_id': post_id},
                                 headers={'Authorization': f'Bearer {creds["access-token"]}'})

        if not response.ok:
            response.raise_for_status()
        logger.info(f'{creds["email"]} liked post id {post_id}')

    def create_likes(self):
        posts = self._get_all_posts()
        # Sort users according to posts amount (descending)
        user_ids = self._users_credentials.keys()
        user_posts_count = [(user_id, len(list(filter(lambda p: p['user_id'] == user_id, posts))))
                            for user_id in user_ids]

        sorted_users = sorted(user_posts_count, key=lambda item: item[1], reverse=True)
        for user_id, _ in sorted_users:
            self._login(user_id=user_id)
            posts = self._get_all_posts()
            # user can only like random posts from users who have at least one post with 0 likes
            # users cannot like their own posts
            likable_users = set(post['user_id'] for post in posts if len(post['likes']) == 0)
            likable_posts = list(filter(lambda post: post['user_id'] != user_id and post['user_id'] in likable_users, posts))

            # performs “like” activity until the user reaches max likes
            max_likes = min(self.bot['max_likes_per_user'], len(likable_posts))
            # one user can like a certain post only once
            selected_posts = random.sample(likable_posts, max_likes)
            for post in selected_posts:
                self._like(user_id, post['id'])

    def run(self):
        self.create_users_and_posts()
        self.create_likes()

    @staticmethod
    def generate_password():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(PASSWORD_LEN))


def main():
    init_logger()
    bot = Bot(BOT_CONFIG_FILE_PATH)
    bot.run()


if __name__ == "__main__":
    main()
