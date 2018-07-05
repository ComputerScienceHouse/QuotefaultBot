from app import _ldap

def resolve_name(uid: str) -> str:
    try:
        member = _ldap.get_member(uid, uid=True)
        return member.cn + '(' + uid + ')'
    except:
        return uid

