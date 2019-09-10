import re


class InvalidVersionError(Exception):
    pass

class VersionNotFoundError(Exception):
    pass

class ApiVersion(object):
    versions = {}

    @classmethod
    def coerce_to_version(cls, version):
        try:
            return cls.versions[version]
        except KeyError:
            raise VersionNotFoundError

    @classmethod
    def define_version(cls, version):
        cls.versions[version.name] = version
        return version

    @classmethod
    def define_known_versions(cls):
        cls.define_version(Unstable())
        cls.define_version(Release('2019-04'))
        cls.define_version(Release('2019-07'))
        cls.define_version(Release('2019-10'))
        cls.define_version(Release('2020-01'))

    @classmethod
    def clear_defined_versions(cls):
        cls.versions = {}

    @property
    def numeric_version(self):
        return self._numeric_version

    @property
    def name(self):
        return self._name

    def api_path(self, site):
        return site + self._path

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.numeric_version == int(other.numeric_version)


class Release(ApiVersion):
    FORMAT = re.compile('^\d{4}-\d{2}$')
    API_PREFIX = '/admin/api'

    def __init__(self, version_number):
        if not self.FORMAT.match(version_number):
            raise InvalidVersionError
        self._name = version_number
        self._numeric_version = int(version_number.replace('-', ''))
        self._path = '%s/%s' % (self.API_PREFIX, version_number)

    @property
    def stable(self):
        return True


class Unstable(ApiVersion):
    def __init__(self):
        self._name = 'unstable'
        self._numeric_version = 9000000
        self._path =  '/admin/api/unstable'

    @property
    def stable(self):
        return False


ApiVersion.define_known_versions()
