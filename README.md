
## Gov UK Data Lookup

Given the URL to a transparency publication on gov.uk, turns it into
a CKAN style dataset dictionary.

### Installation

1. Clone this repository into a folder
2. Create a virtualenv (and activate it)
3. python setup.py develop

You will need to have a C compiler and libxml2 installed for this to 
work (because of LXML)


### Usage

From the command line, you can try converting a URL to a dict by 
using 

```
scrape_govuk --url <URL to a transparency publication page>
```

For use in a python app you should use .

```python
from govuk_datalookup import fetch

dataset = fetch.process_url("https://gov.uk/....")
```
