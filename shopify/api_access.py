import re


class ApiAccess:

    SCOPE_DELIMITER = ","
    IMPLIED_SCOPE_RE = re.compile(r"\A(?P<unauthenticated>unauthenticated_)?write_(?P<resource>.*)\Z")

    def __init__(self, scopes):

        if type(scopes) == str:
            scopes = scopes.split(self.SCOPE_DELIMITER)

        self.__store_scopes(scopes)

    def covers(self, api_access):
        return api_access._compressed_scopes <= self._expanded_scopes

    def __str__(self):
        return self.SCOPE_DELIMITER.join(self._compressed_scopes)

    def __iter__(self):
        return iter(self._compressed_scopes)

    def __eq__(self, other):
        return type(self) == type(other) and self._compressed_scopes == other._compressed_scopes

    def __store_scopes(self, scopes):
        sanitized_scopes = set(list(filter(None, [scope.strip() for scope in scopes])))
        implied_scopes = set([self.__implied_scope(scope) for scope in sanitized_scopes])
        self._compressed_scopes = sanitized_scopes - implied_scopes
        self._expanded_scopes = sanitized_scopes.union(implied_scopes)

    def __implied_scope(self, scope):
        match = self.IMPLIED_SCOPE_RE.match(scope)
        if match:
            return "{unauthenticated}read_{resource}".format(
                unauthenticated="" if match.group("unauthenticated") is None else match.group("unauthenticated"),
                resource=match.group("resource"),
            )
