# SEO Tools CLI

## Installation

Clone the repository using the following command:

`git clone https://github.com/dinokukic/seo-tools-cli`

Afterwards just install it using `pip`

`pip install seo-tools-cli` - from the current folder, or if you navigate to the folder then:

`pip install .`

## Usage

For now the tool doesn't handle the headers very well and depending on the command it might throw and error. Will be corrected for the v0.2.

### Get Status Codes in Bulk

**Input** - One column CSV with a list of URLS _without the header_

`statuscodes yourcsvfile.csv`

### Redirect Validation in Bulk

**Input** - Two-column CSV, one with URL that should be redirected and second with where the user should land

`redirects validate yourcsvfile.csv`

### Validate Email Addresses in Bulk

**Input** - One-column CSV with the list of email addresses to validate

`emailval youremaillist.csv`

### Extract URLs from a Sitemap

`sitemap extract https://example.com/sitemap.xml`

### Scrape Titles and Meta Descriptions

**Input** - One-column CSV with a URL list

`getmetas yoururllist.csv`

### Retrieve Page Speed Insights in Bulk

**Input** - One-column CSV with a URL list + API Key

[Here's a guide on how to get an API Key from Google Cloud Console](https://kb.mainwp.com/docs/create-the-google-pagespeed-api-key/)

`psi m yoururllist.csv YOUR_API_KEY`

### Submit URL via Indexing API

You will need to set up a service account which you will add to your Google Search Console and create a key. [Here's a guide on how to do that](https://developers.google.com/search/apis/indexing-api/v3/prereqs).

**Input** - A URL or One-column CSV with a URL List + path to the JSON Keyfile

#### Submit Single URL

`index s https://example.com/foo KEY_FILE.JSON`

#### Submit Multiple URLs

`index m yoururllist.csv KEY_FILE.JSON`