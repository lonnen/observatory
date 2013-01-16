from werkzeug.exceptions import HTTPException


class FailedDependency(HTTPException):
    code = 424
    description = "The request failed due to failure of a previous request."
    name = "Failed Dependency"

    def get_response(self, environment):
        resp = super(FailedDependency, self).get_response(environment)
        resp.status = "%s %s" % (self.code, self.name.upper())
        return resp
