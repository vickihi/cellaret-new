from cellars.models import Cellar


def create_cellar(*, name, description, user):
    """Create a cellar for a user."""
    cellar = Cellar.objects.create(name=name, description=description, user=user)

    return cellar
