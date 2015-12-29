# -*- coding: utf-8 -*-

import json
import logging


def makeanswer(answ, **kwargs):
    r = { 'errno' : 0, 'error': 'OK', 'details': '',}
    r.update(answ)
    r.update(kwargs)
    return r


def makeerror(errno, errcls, error, details=''):
    r = { 'error_type': errcls, 'error_text': error, 'error_details': details, 'error_level': 'fatal', }
    return errno, makeanswer(r, errno=errno, error=error, details=details)


def returnstatus(func):
    def wrapped(self, *args, **kwargs):
        self.set_header('Server', self.application.server.engine.server_name)

        r = func(self, *args, **kwargs)

        if isinstance(r, int):
            self.send_error(status_code=r)
            return None

        if isinstance(r, (list, tuple)):
            logging.warning("RETURN ANSWER: %s" % json.dumps(makeanswer(r[1])))
            self.send_error(status_code=r[0], body=json.dumps(makeanswer(r[1])) )
            return None

        r = makeanswer(r)
        self.write(json.dumps(r))
        self.finish()

        
    return wrapped



