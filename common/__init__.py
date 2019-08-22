def tostring(c):
    c.__str__ = lambda c: "%s(%s)" % (
    c.__class__.__name__,
    ", ".join(str(v) for v in c.__dict__.values())
    )

    return c