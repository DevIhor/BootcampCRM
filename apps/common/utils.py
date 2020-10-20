def base_concrete_model(abstract, instance):
    """
    Used in methods of abstract models to find the super-most concrete (non abstract) model in the inheritance chain
    that inherits from the given abstract model. This is so the methods in the abstract model can query data
    consistently across the correct concrete model.
    """
    for cls in reversed(instance.__class__.__mro__):
        if issubclass(cls, abstract) and not cls._meta.abstract:
            return cls
    return instance.__class__
