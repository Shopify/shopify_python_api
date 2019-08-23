from pyactiveresource.collection import Collection

from six.moves.urllib.parse import urlparse, parse_qs

class PaginatedCollection(Collection):
    """
    A subclass of Collection which allows cycling through pages of
    data through cursor-based pagination.
    """

    def __init__(self, *args, **kwargs):
        """If given a Collection object as an argument, inherit its metadata."""

        metadata = kwargs.pop("metadata", None)
        obj = args[0]
        if isinstance(obj, Collection):
            if metadata:
                metadata.update(obj.metadata)
            else:
                metadata = obj.metadata
            super(PaginatedCollection, self).__init__(obj, metadata=metadata)
        else:
            super(PaginatedCollection, self).__init__(metadata=metadata or {},
                                                      *args, **kwargs)

        self._next = None
        self._previous = None
        self._current_iter = None

    def _check_pagination_metadata(self):
        if not ("pagination" in self.metadata
                and "resource_class" in self.metadata):
            raise AttributeError("Cursor-based pagination requires "
                                 "\"pagination\" and \"resource_class\" "
                                 "attributes in the metadata.")

    def _get_query_params(self, url):
        """Returns a dictionary of query arguments for the given URL."""
        parsed_url = urlparse(url)
        query_dict = parse_qs(parsed_url.query)

        # pyactiveresource.util.to_query considers list items to be multiple
        # query items and so appends a [] to them which is wrong, because it
        # fails to consider lists with a length of 1 (which is always returned
        # from parse_qs). We need to flatten the items.
        return {
            k: v[0] for k, v in query_dict.items()
        }

    def previous(self, **extra_params):
        """Returns the previous page of items.

        Args:
            extra_params: Any extra parameters passed to find().
        Returns:
            A PaginatedCollection object with the new data set.
        """
        if self._previous:
            return self._previous

        self._check_pagination_metadata()

        pagination = self.metadata["pagination"]
        if not "previous" in pagination:
            raise IndexError("No previous page")

        Resource = self.metadata["resource_class"]
        query_params = self._get_query_params(pagination["previous"])
        query_params.update(extra_params)
        self._previous = Resource.find(id_=None, from_=None, **query_params)
        return self._previous

    def next(self, **extra_params):
        """Returns the next page of items.

        Args:
            extra_params: Any extra parameters passed to find().
        Returns:
            A PaginatedCollection object with the new data set.
        """
        if self._next:
            return self._next

        self._check_pagination_metadata()

        pagination = self.metadata["pagination"]
        if not "next" in pagination:
            raise IndexError("No next page")

        Resource = self.metadata["resource_class"]
        query_params = self._get_query_params(pagination["next"])
        query_params.update(extra_params)
        self._next = Resource.find(id_=None, from_=None, **query_params)
        return self._next

    def __iter__(self):
        """Iterates through all items, also fetching other pages."""
        yield from super(PaginatedCollection, self).__iter__()

        try:
            if not self._current_iter:
                self._current_iter = self
            self._current_iter = self.next()
            yield from self._current_iter
        except IndexError:
            return

    def __len__(self):
        """If fetched count all the pages."""

        if self._next:
            count = len(self._next)
        else:
            count = 0
        return count + super(PaginatedCollection, self).__len__()
