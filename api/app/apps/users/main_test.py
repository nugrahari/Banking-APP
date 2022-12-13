from .main import app
from libs import tests

client = tests.MyTestClient(app)


def test_get_root(admin1_token, user1_data, user2_data, user3_data):
    _, status = client.get_parsed('/')
    assert status == 403
    response, status = client.get_parsed('/', auth=admin1_token)
    assert status == 200

    data = response.get('data')
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert len(data) == 3


def test_post_user(admin1_token):
    user = tests.UserTest(
        phone_number='+6281234567892', name='Hari Nugraha', email_address='harin262@gmail.com',
        tax_id='123458', address="Banjar", password='123456', password2='123456', role='user')

    _, status = client.post_parsed('/', json=user.dict())
    assert status == 403

    user_test = user.copy()
    user_test.phone_number = '+6281234567890'  # Test Unique Phone number
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 400

    user_test = user.copy()
    user_test.name = 'Hari Nugraha 99'  # Test Only alfabeth name
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    user_test = user.copy()
    user_test.initial_deposit = 10  # Test minimal deposit
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    user_test = user.copy()
    user_test.initial_deposit = 7082.689  # Test max decimal number after point
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    user_test = user.copy()
    user_test.tax_id = 'ABCDEF'  # Test Tax must numuber
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    user_test = user.copy()
    user_test.tax_id = '1234569'  # Test maximum digit tax
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    user_test = user.copy()
    user_test.tax_id = '000111'  # Test unique tax
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 400

    user_test = user.copy()
    user_test.email_address = 'harin262gmail.com'  # Test valid email_address
    _, status = client.post_parsed(
        '/', json=user_test.dict(), auth=admin1_token)
    assert status == 422

    response, status = client.post_parsed(
        '/', json=user.dict(), auth=admin1_token)
    assert status == 201

    data_user = response.get('data')

    assert data_user['name'] == 'Hari Nugraha'
    assert data_user['phone_number'] == '+6281234567892'
    assert data_user['email_address'] == 'harin262@gmail.com'
    assert data_user['tax_id'] == '123458'
    assert data_user['address'] == 'Banjar'
    assert data_user['role'] == 'user'
    assert 'account_number' in data_user


def test_get_balance_details(admin1_token, user1_data):

    _, status = client.get_parsed(F"/balance-details/{user1_data.get('id')}")
    assert status == 403
    _, status = client.get_parsed(
        F'/balance-details/6e59d10d-973d-43ee-b526-199474090255', auth=admin1_token)
    assert status == 404
    response, status = client.get_parsed(
        F"/balance-details/{user1_data['id']}", auth=admin1_token)
    assert status == 200

    assert 'name' in response.get('data')
    assert 'phone_number' in response.get('data')
    assert 'email_address' in response.get('data')
    assert 'address' in response.get('data')
    assert 'total_balance' in response.get('data')
    assert response.get('data').get('name') == user1_data['name']
    assert response.get('data').get(
        'email_address') == user1_data['email_address']
    assert response.get('data').get('address') == user1_data['address']
    assert response.get('data').get(
        'phone_number') == user1_data['phone_number']
    assert response.get('data').get('total_balance') == 8005.42


def test_post_withdraw(admin1_token, user1_data):

    response, status = client.get_parsed(
        F"/balance-details/{user1_data['id']}", auth=admin1_token)
    assert status == 200
    assert response.get('data').get('total_balance') == 8005.42

    form_data = {
        'user_id': '6e59d10d-973d-43ee-b526-199474090255', 'amount': 100}
    _, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 404

    form_data['user_id'] = user1_data['id']
    form_data['amount'] = 0
    _, status = client.post_parsed(F"/transactions/withdraw", json=form_data)
    assert status == 403

    _, status = client.post_parsed(
        F"/transactions/withdraw", auth=admin1_token)
    assert status == 422

    _, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 422

    form_data['amount'] = 500.852
    _, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 422

    form_data['amount'] = 500
    response, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 200
    assert response.get('previous_balance') == 8005.42
    assert response.get('total_balance') == 7505.42

    form_data['amount'] = 501
    response, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 200
    assert response.get('previous_balance') == 7505.42
    assert response.get('total_balance') == 6994.42

    form_data['amount'] = 5001
    response, status = client.post_parsed(
        F"/transactions/withdraw", json=form_data, auth=admin1_token)
    assert status == 200
    assert response.get('previous_balance') == 6994.42
    assert response.get('total_balance') == 1973.42

    user_data = response.get('user_data')
    assert 'id' in user_data
    assert 'account_number' in user_data
    assert 'name' in user_data

    transaction_data = response.get('transaction_data')
    assert 'id' in transaction_data
    assert 'amount' in transaction_data

    assert 'previous_balance' in response
    assert 'total_balance' in response

    response, status = client.get_parsed(
        F"/balance-details/{user1_data['id']}", auth=admin1_token)
    assert status == 200
    assert response.get('data').get('total_balance') == 1973.42


def test_post_deposit(admin1_token, user1_data):

    response, status = client.get_parsed(
        F"/balance-details/{user1_data['id']}", auth=admin1_token)
    assert status == 200
    assert response.get('data').get('total_balance') == 8005.42

    form_data = {
        'user_id': '6e59d10d-973d-43ee-b526-199474090255', 'amount': 700}
    _, status = client.post_parsed(
        F"/transactions/deposit", json=form_data, auth=admin1_token)
    assert status == 404

    form_data['user_id'] = user1_data['id']
    form_data['amount'] = 0
    _, status = client.post_parsed(F"/transactions/deposit", json=form_data)
    assert status == 403

    _, status = client.post_parsed(F"/transactions/deposit", auth=admin1_token)
    assert status == 422

    _, status = client.post_parsed(
        F"/transactions/deposit", json=form_data, auth=admin1_token)
    assert status == 422

    form_data['amount'] = 500.852
    _, status = client.post_parsed(
        F"/transactions/deposit", json=form_data, auth=admin1_token)
    assert status == 422

    form_data['amount'] = 1500
    response, status = client.post_parsed(
        F"/transactions/deposit", json=form_data, auth=admin1_token)
    assert status == 200
    assert response.get('previous_balance') == 8005.42
    assert response.get('total_balance') == 9505.42

    user_data = response.get('user_data')
    assert 'id' in user_data
    assert 'account_number' in user_data
    assert 'name' in user_data

    transaction_data = response.get('transaction_data')
    assert 'id' in transaction_data
    assert 'amount' in transaction_data

    assert 'previous_balance' in response
    assert 'total_balance' in response

    response, status = client.get_parsed(
        F"/balance-details/{user1_data['id']}", auth=admin1_token)
    assert status == 200
    assert response.get('data').get('total_balance') == 9505.42
