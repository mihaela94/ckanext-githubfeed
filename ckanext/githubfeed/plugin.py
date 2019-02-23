import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import requests
import json

def gettasks(params = {'state': 'open'}):

    # print 'In gettasks'

    url = toolkit.config.get('ckan.githubfeed.requesturl', 'https://api.github.com/repos/code4romania/ckanext-dataportaltheme/issues')

    # print url

    r = requests.get(url=url, params=params)

    obj = json.loads(r.text)

    return obj

    # return url


class GithubfeedPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fantastic', 'githubfeed')

    def get_helpers(self):
        return {'githubfeed_gettasks': gettasks,
                'githubfeed_getallissuesurl': toolkit.config.get('ckan.githubfeed.allissuesurl', 'https://github.com/orgs/code4romania/projects/12')
                }
