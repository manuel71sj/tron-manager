import logging as logger

from django.utils.deprecation import MiddlewareMixin

log = logger.getLogger(__name__)


class RequestLogMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        logger.info(
            '[user.trace] user: %s(%s), uri: [%s]%s paramMap: %s, body: %s'
            % (request.user, request.user._id,
               request.method,
               request.path,
               request.GET,
               request.POST))
