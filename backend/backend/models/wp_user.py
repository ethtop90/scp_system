class Wp_user:
    def __init__(self, id, username, login_password = None, application_password = None):
        self.id = id
        self.username = username
        self.login_password = login_password
        self.application_password = application_password
    