from django.core.exceptions import ValidationError as DjangoValidationError

from root.core.application.domain.exceptions import BaseError, ErrorType
from root.core.utils import gettext_lazy as _


class ProductSoldError(BaseError, DjangoValidationError):
    type = ErrorType.INVALID
    code = "product_sold_error"
    message = _("Product already sold in another order")


class ValidationError(BaseError):
    type = ErrorType.INVALID
    code = "validation_error"
    message = _("Validation error")


class OrderWorkflowError(BaseError):
    type = ErrorType.INVALID
    code = "order_workflow_error"
    message = _("Wrong workflow status")
