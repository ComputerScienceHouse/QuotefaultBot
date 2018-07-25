_ldap = None

def init(ldap):
    global _ldap
    _ldap = ldap

def resolve_name(uid: str) -> str:
    try:
        member = _ldap.get_member(uid, uid=True)
        return member.displayname
    except: # pylint: disable=bare-except
        return uid
