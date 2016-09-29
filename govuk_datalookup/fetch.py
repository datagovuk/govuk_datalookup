from urlparse import urljoin

import requests
import requests_cache

from lxml.etree import HTMLParser

requests_cache.install_cache('scraper_cache')


def get_title(dom):
    """ Find the dataset title in the DOM and return it """
    return dom.cssselect('.inner-heading h1')[0].text

def get_notes(dom):
    """
    Find the description in the DOM and return it.  If we find the
    extra section near the bottom of govuk pages then we will append it
    after two newlines
    """
    notes = dom.cssselect('.summary p')[0].text

    extra_notes = dom.cssselect('.body .govspeak p')
    if extra_notes:
        notes += u'\n\n' + extra_notes[0].text

    return notes

def get_owner_org(dom):
    """ Get the gov.uk shortname for the publishing organisation """
    return dom.cssselect('.from a')[0].get('href').split('/')[-1]

def get_extra_meta(dom):
    meta = dom.cssselect('dl.primary-metadata')[0]

    # Pull child elements in pairs
    #for dt, dd in map(None, *([iter(meta)] * 2)):
    #    if dt.text == 'Published:':
    #        pass
    #    elif dt.text == 'Updated:':
    #        pass
    return {}

def parse_html(name, html):
    """
    Parse the provided html to find a dataset
    """
    parser = HTMLParser(encoding="UTF-8")
    try:
        parser.feed(html)
        dom = parser.close()
    except:
        return {}

    dataset = {
        u'name' : name,
        u'title': get_title(dom),
        u'notes': get_notes(dom),

        u'owner_org': get_owner_org(dom),
        u'resources':  parse_resources(dom),
    }

    dataset.update(get_extra_meta(dom))

    return dataset


def parse_resources(dom):
    """
    Parse anything that looks like an attachment into a list of CKAN
    style resources.

    Finding the title is straightforward, but often it also contains a link
    to the document instead of a separate download link.  We handle both cases
    by looking for the link and using it as the url of the resource.
    """
    resources = []

    attachments = dom.cssselect('.attachment-details')
    for attachment in attachments:
        resource = {}
        title = attachment.cssselect('.title')
        if not title[0].text:
            title = attachment.cssselect('.title a')
            resource[u'url'] = urljoin('https://gov.uk',  title[0].get('href'))

        resource[u'description'] = title[0].text

        links = attachment.cssselect('.metadata .download a')
        if links:
            resource[u'url'] = urljoin('https://gov.uk', links[0].get('href'))
        resource[u'format'] = resource[u'url'].split('.')[-1].upper()

        resources.append(resource)

    return resources


def process_url(url):
    """
    Fetch the provided URL content and parse it to build a
    CKAN style dataset
    """
    print "Processing {}".format(url)

    response = requests.get(url)
    if not response.status_code == 200:
        return None

    name = url.split('/')[-1]
    return parse_html(name, response.content)

