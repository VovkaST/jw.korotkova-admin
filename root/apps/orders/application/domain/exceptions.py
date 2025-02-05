from root.core.application.domain.exceptions import BaseError, ErrorType
from root.core.utils import gettext_lazy as _


class ValidationError(BaseError):
    type = ErrorType.INVALID
    code = "validation_error"
    message = _("Validation error")


class OrderWorkflowError(BaseError):
    type = ErrorType.INVALID
    code = "order_workflow_error"
    message = _("Wrong workflow status")
