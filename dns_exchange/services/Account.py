from dns_exchange.db_models.redis.User import User


class Account:
    def __init__(self):
        new_user = User()
        self.address = new_user.address
        self.seed_phrase = new_user.seed_phrase
        self.assets = new_user.assets
        self.is_admin = new_user.is_admin

        # TODO: Also add self.auth_token and auto-login when creating Account
