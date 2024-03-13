class License:
    def __init__(self):
        self.title = None
        self.id = None
        self.description = None
        self.permissions = {
            "commercial-use": 0,
            "distribution": 0,
            "modifications": 0,
            "private-use": 0,
            "patent-use": 0,
            "sublicense": 0,
        }
        self.conditions = {
            "include-copyright": 0,
            "document-changes": 0,
            "disclose-source": 0,
            "network-use-disclose": 0,
            "same-license": 0,
        }
        self.limitations = {"liability": 0, "warranty": 0, "trademark-use": 0}

    def set_info(self, conditions, limitations, permissions, title, description, id):
        for cond in conditions:
            self.conditions[cond] = 1
        for perm in permissions:
            self.permissions[perm] = 1
        for lim in limitations:
            self.limitations[lim] = 1
        self.all_rights = self.conditions.copy()
        self.all_rights.update(self.permissions)
        self.all_rights.update(self.limitations)

        self.id = id
        self.title = title
        self.description = description

    def print_info(self):
        print(self.permissions)
        print(self.limitations)
        print(self.conditions)
        print(self.id)
        print(self.title)
        print(self.description)
