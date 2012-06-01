__author__ = 'leifj'

from django.conf import settings

def asgard_sp_config(request=None):
    host = "localhost"
    if request != None:
        host = request.get_host().replace(":","-")
    return {
        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': 'https://keybucket.app.nordu.net/saml2/sp/metadata',
        # directory with attribute mapping
        "attribute_map_dir" : "%s/saml2/attributemaps" % settings.BASE_DIR,
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp' : {
                'name': 'KeyBucket',
                'endpoints': {
                    # url and binding to the assertion consumer service view
                    # do not change the binding osettingsr service name
                    'assertion_consumer_service': [
                        ('https://keybucket.app.nordu.net/saml2/sp/acs/',
                         BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        ('https://keybucket.app.nordu.net/saml2/sp/ls/',
                         BINDING_HTTP_REDIRECT),
                    ],
                    },
                # attributes that this project need to identify a user
                'required_attributes': ['eduPersonPrincipalName','displayName'],
                }
        },

        # where the remote metadata is stored
        'metadata': { 'remote': [{'url':'http://md.swamid.se/md/swamid-idp.xml',
                                  'cert':'%s/saml2/credentials/md-signer.crt'}] },

        # set to 1 to output debugging information
        'debug': 1,

        # certificate
        "key_file" : "%s/%s.key" % (settings.SSL_KEY_DIR,host),
        "cert_file" : "%s/%s.crt" % (settings.SSL_CRT_DIR,host),
        # own metadata settings
        'contact_person': [
                {'given_name': 'Leif',
                 'sur_name': 'Johansson',
                 'company': 'NORDUnet',
                 'email_address': 'leifj@nordu.net',
                 'contact_type': 'technical'},
                {'given_name': 'Johan',
                 'sur_name': 'Berggren',
                 'company': 'NORDUnet',
                 'email_address': 'jbn@nordu.net',
                 'contact_type': 'technical'},
        ],
        # you can set multilanguage information here
        'organization': {
            'name': [('NORDUNet', 'en')],
            'display_name': [('NORDUnet A/S', 'en')],
            'url': [('http://www.nordu.net', 'en')],
            },
        'valid_for': 24,  # how long is our metadata valid
    }