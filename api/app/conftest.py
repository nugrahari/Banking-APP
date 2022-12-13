
import pytest


from libs import db, tests
from apps.users import services as user_services


@pytest.fixture(name="admin1")
def fixture_admin1() -> tests.UserTest:
    return tests.UserTest(
        phone_number='+6281234567890', name='Hari Nugraha', email_address='harin260@gmail.com',
        tax_id='000111', address="Banjar", password='123456', password2='123456', role='administrator')


@pytest.fixture(name="user1")
def fixture_user1() -> tests.UserTest:
    return tests.UserTest(
        phone_number='+6281234567891', name='Hari Nugraha', email_address='harin261@gmail.com',
        tax_id='123457', address="Banjar", password='123456', password2='123456', role='user')


@pytest.fixture(name="user2")
def fixture_user2() -> tests.UserTest:
    return tests.UserTest(
        phone_number='+6281234567892', name='Hari Nugraha', email_address='harin262@gmail.com',
        tax_id='123458', address="Banjar", password='123456', password2='123456', role='user')


@pytest.fixture(name="user3")
def fixture_user3() -> tests.UserTest:
    return tests.UserTest(
        phone_number='+6281234567894', name='Hari Nugraha', email_address='harin263@gmail.com',
        tax_id='123459', address="Banjar", password='123456', password2='123456', role='user')


@pytest.fixture(name="reset_table", autouse=True)
def fixture_reset_table(admin1: tests.UserTest):
    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(bind=db.engine)
    with db.session() as db_:
        user_service = user_services.UserService(db_)
        user_service.register(admin1)

    yield
