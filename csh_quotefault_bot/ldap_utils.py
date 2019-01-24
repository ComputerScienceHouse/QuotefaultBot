import ldap
import srvlookup

_BASE = "cn=users,cn=accounts,dc=csh,dc=rit,dc=edu"

class LDAPUtils:

    def __init__(self, bind_dn, bind_pw):
        uris = ''.join(['ldaps://' + srv.hostname + "," for srv in  srvlookup.lookup('ldap', 'tcp', 'csh.rit.edu')])
        self._ldap = ldap.ldapobject.ReconnectLDAPObject(uris)
        self._ldap.simple_bind_s(bind_dn, bind_pw)


    def validate_uid(self, csh_uid):
        """
        Checks that a uid is valid.
        Returns:
            ('ok', {'name': 'Name (uid)'})
            ('failure', {})
        """
        search_result = self._ldap.search_s(_BASE, ldap.SCOPE_SUBTREE, "(uid=%s)" % csh_uid, ['displayname'])
        if len(search_result) != 1:
            return ('failure', {})
        name = search_result[0][1]['displayname'][0].decode("utf-8")
        return ('ok', {'name':name})


    def verify_slack_uid(self, slack_uid):
        """
        Verifies a slack uid is tied to a member object.
        Returns:
            (status, {'uid' : str, 'cn' : str})
        where status is 'ok' or 'failure'
        """
        search_result = self._ldap.search_s(_BASE, ldap.SCOPE_SUBTREE, "(slackuid=%s)" % slack_uid, ['uid', 'cn'])
        if len(search_result) != 1:
            return ('failure', {})
        uid = search_result[0][1]['uid'][0].decode("utf-8")
        cn = search_result[0][1]['cn'][0].decode("utf-8")
        return ('ok', {'uid':uid, 'cn':cn})
