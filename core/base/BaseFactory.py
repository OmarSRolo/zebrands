import factory


class BaseFactoryModel(factory.django.DjangoModelFactory):
    is_deleted: bool = False
    is_active: bool = True


class CoreFactory(factory.DictFactory):
    ...


class BaseFactory(CoreFactory):
    is_deleted: bool = False
    is_active: bool = True
