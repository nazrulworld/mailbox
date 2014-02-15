# _*_ coding: utf-8 _*_
import imaplib, email, re
import datetime
from config import application as ap
from flask import g


def login(user=None, password=None, server=None, ssl=None, port=None):
    if user is None:
        user = ap.IMAP_USER
    if password is None:
        password = ap.IMAP_PASSWORD
    if server is None:
        if re.search(r'@gmail\.com', user, re.I) is not None:
            server = ap.IMAP_GOOGLE_SERVER
            port = ap.IMAP_GOOGLE_SSL_PORT

        elif re.search(r'@yahoo\.com', user, re.I) is not None:
            server = ap.IMAP_YAHOO_SERVER
            port = ap.IMAP_YAHOO_SSL_PORT
        elif re.search(r'@(hotmail|live|outlook)\.com', user, re.I) is not None:
            server = ap.IMAP_OUTLOOK_SERVER
            port = ap.IMAP_OUTLOOK_SSL_PORT
        elif re.search(r'@(aol|aim)\.com', user, re.I) is not None:
            server = ap.IMAP_AOL_SERVER
            port = ap.IMAP_AOL_SERVER
    if ssl is None:
        ssl = ap.IMAP_SSL
    imap4 = None
    try:
        if ssl is False:
            imap4 = imaplib.IMAP4(server, port=port)
        else:
            imap4 = imaplib.IMAP4_SSL(server, port=port)
        imap4.login(user, password)
    except imaplib.IMAP4.abort, err:
        print "Error in %s" % err
    except imaplib.IMAP4.readonly, err:
        print "Error in %s" % err
    except imaplib.IMAP4.error, err:
        print "Error in %s" % err
    finally:
        return imap4


def inbox(imap4=None, old=7, max=20, uids=None, body=False):
    if imap4 is None:
        if g.email is not None and g.password is not None and g.imap4 is True:
            imap4 = login(g.email, g.password)
    if imap4 is None:
        return False
    if imap4.state == 'SELECTED':
        imap4.close()
    if imap4.state != 'AUTH':
        return False
    try:
        imap4.select("inbox")
        if uids is None:
            date = (datetime.date.today() - datetime.timedelta(int(old))).strftime("%d-%b-%Y")
            status, uids = imap4.uid('search', None, '(SENTSINCE {date})'.format(date=date))
        if uids is not None:
            uids = uids[0].replace(' ', ',')
            if uids[-1] == ',':
                # Make sure no ended comma
                uids = uids[:-1]
            if body:
                rfc822 = '(RFC822)'
            else:
                rfc822 = '(RFC822.HEADER)'
            status, data = imap4.uid('fetch', uids, rfc822)
            lst = []
            for i, m in enumerate(data):
                if i % 2 == 0:
                    em = email.message_from_string(m[1])
                    tmp = email.utils.parseaddr(em.get('To', None))
                    em.__delitem__('To')
                    em.__setitem__('To', tmp)
                    tmp = email.utils.parseaddr(em.get('From', None))
                    em.__delitem__('From')
                    em.__setitem__('From', tmp)
                    if body:
                        _body = None
                        main_type = em.get_content_maintype()
                        if main_type == 'multipart':
                            for part in em.get_payload():
                                if part.get_content_maintype() == 'text':
                                    _body = part.get_payload()
                        elif main_type == 'text':
                            _body = em.get_payload()
                        em.__delitem__('Body')
                        em.__setitem__('Body', _body)
                    em.__setitem__('Email_Meta', m[0])
                    lst.append(em)
            return lst
    except imap4.abort, er:
        print er
    except imap4.error, er:
        print er