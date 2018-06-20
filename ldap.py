import csh_ldap
from app import app

ldap = csh_ldap.CSHLDAP(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'])

def resolve_name(uid: str) -> str:
    try:
        member = ldap.get_member(uid, uid=True)
        return member.cn + '(' + uid + ')'
    except:
        return uid

