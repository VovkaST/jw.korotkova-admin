class ReadOnlyMixin:
    read_only = False

    def get_readonly_fields(self, request, obj=None) -> list[str]:
        if not self.read_only:
            return super().get_readonly_fields(request, obj)
        fields = list(self.get_fields(request, obj))
        readonly_fields = list(self.readonly_fields)
        return list(set(fields + readonly_fields))

    def has_add_permission(self, request, obj) -> bool:
        if self.read_only:
            return False
        return super().has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if self.read_only:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        if self.read_only:
            return False
        return super().has_delete_permission(request, obj)
