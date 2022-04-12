import logging as logger

from django.utils.deprecation import MiddlewareMixin

log = logger.getLogger(__name__)


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(
            '[user.trace] user: %s(%s), uri: [%s]%s paramMap: %s, body: %s'
            % (request.user, request.user._id,
               request.method,
               request.path,
               request.GET,
               request.POST))


"""
I|user.trace          |  309|2022-01-11 09:08:11,704|{
"uri":"/api/v2/sample/signup.json",
"paramMap":"{}",
"body":"{password=qwer1234!, phone=010-5487-1222, 
    name=한만철, email=manuel71@thedocent.co.kr}",
"errorCode":"could not execute statement; SQL [n/a]; nested exception is org.hibernate.exception.SQLGrammarException: could not execute statement"}
"""
