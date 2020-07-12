class Sync:

    def __init__(self, github_username: str, pat: str):
        self.github_username = ''
        self.pat = ''

    @classmethod
    def sync(cls):
        pass

    def fetch_github_credentials(self):
        pass

    def check_template_update_available(self):
        pass

    def create_new_template(self):
        pass

    def create_pull_request(self):
        pass

    def checkout_original_branch(self):
        pass
