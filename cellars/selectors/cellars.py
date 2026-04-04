def get_user_cellars(*, user):
    """Get all cellars for a user."""
    cellars = user.cellars.all()
    return cellars
