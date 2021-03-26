import re
import sys

if sys.version_info[0] < 3:  # Backwards compatibility for python < v3.0.0
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

HOSTNAME_PATTERN = r"[a-z0-9][a-z0-9-]*[a-z0-9]"


def sanitize_shop_domain(shop_domain, myshopify_domain="myshopify.com"):
    name = str(shop_domain or "").lower().strip()
    if myshopify_domain not in name and "." not in name:
        name += ".{domain}".format(domain=myshopify_domain)
    name = re.sub(r"https?://", "", name)

    uri = urlparse("http://{hostname}".format(hostname=name))
    if re.match(r"{h}\.{d}$".format(h=HOSTNAME_PATTERN, d=re.escape(myshopify_domain)), uri.netloc):
        return uri.netloc
