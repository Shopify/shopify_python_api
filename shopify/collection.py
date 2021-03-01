from pyactiveresource.collection import Collection
from six.moves.urllib.parse import urlparse, parse_qs
import cgi


class PaginatedCollection(Collection):
    """
    A subclass of Collection which allows cycling through pages of
    data through cursor-based pagination.

    :next_page_url contains a url for fetching the next page
    :previous_page_url contains a url for fetching the previous page

    You can use next_page_url and previous_page_url to fetch the next page
    of data by calling Resource.find(from_=page.next_page_url)
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
            super(PaginatedCollection, self).__init__(metadata=metadata or {}, *args, **kwargs)

        if not ("resource_class" in self.metadata):
            raise AttributeError('Cursor-based pagination requires a "resource_class" attribute in the metadata.')

        self.metadata["pagination"] = self.__parse_pagination()
        self.next_page_url = self.metadata["pagination"].get("next", None)
        self.previous_page_url = self.metadata["pagination"].get("previous", None)

        self._next = None
        self._previous = None
        self._current_iter = None
        self._no_iter_next = kwargs.pop("no_iter_next", True)

    def __parse_pagination(self):
        if "headers" not in self.metadata:
            return {}

        values = self.metadata["headers"].get("Link", self.metadata["headers"].get("link", None))
        if values is None:
            return {}

        result = {}
        for value in values.split(", "):
            link, rel = value.split("; ")
            result[rel.split('"')[1]] = link[1:-1]
        return result

    def has_previous_page(self):
        """Returns true if the current page has any previous pages before it."""
        return bool(self.previous_page_url)

    def has_next_page(self):
        """Returns true if the current page has any pages beyond the current position."""
        return bool(self.next_page_url)

    def previous_page(self, no_cache=False):
        """Returns the previous page of items.

        Args:
            no_cache: If true the page will not be cached.
        Returns:
            A PaginatedCollection object with the new data set.
        """
        if self._previous:
            return self._previous
        elif not self.has_previous_page():
            raise IndexError("No previous page")
        return self.__fetch_page(self.previous_page_url, no_cache)

    def next_page(self, no_cache=False):
        """Returns the next page of items.

        Args:
            no_cache: If true the page will not be cached.
        Returns:
            A PaginatedCollection object with the new data set.
        """
        if self._next:
            return self._next
        elif not self.has_next_page():
            raise IndexError("No next page")
        return self.__fetch_page(self.next_page_url, no_cache)

    def __fetch_page(self, url, no_cache=False):
        next = self.metadata["resource_class"].find(from_=url)
        if not no_cache:
            self._next = next
            self._next._previous = self
        next._no_iter_next = self._no_iter_next
        return next

    def __iter__(self):
        """Iterates through all items, also fetching other pages."""
        for item in super(PaginatedCollection, self).__iter__():
            yield item

        if self._no_iter_next:
            return

        try:
            if not self._current_iter:
                self._current_iter = self
            self._current_iter = self.next_page()

            for item in self._current_iter:
                yield item
        except IndexError:
            return

    def __len__(self):
        """If fetched count all the pages."""

        if self._next:
            count = len(self._next)
        else:
            count = 0
        return count + super(PaginatedCollection, self).__len__()


class PaginatedIterator(object):
    """
    This class implements an iterator over paginated collections which aims to
    be more memory-efficient by not keeping more than one page in memory at a
    time.

    >>> from shopify import Product, PaginatedIterator
    >>> for page in PaginatedIterator(Product.find()):
    ...     for item in page:
    ...         do_something(item)
    ...
    # every page and the page items are iterated
    """

    def __init__(self, collection):
        if not isinstance(collection, PaginatedCollection):
            raise TypeError("PaginatedIterator expects a PaginatedCollection instance")
        self.collection = collection
        self.collection._no_iter_next = True

    def __iter__(self):
        """Iterate over pages, returning one page at a time."""
        current_page = self.collection
        while True:
            yield current_page
            try:
                current_page = current_page.next_page(no_cache=True)
            except IndexError:
                return
