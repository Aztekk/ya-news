from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf
from pytest_django.asserts import assertRedirects
from django.test.client import Client

pytestmark = pytest.mark.django_db


HOME_URL = lf('home_url')
LOGIN_URL = lf('users_login_url')
LOGOUT_URL = lf('users_logout_url')
SINGUP_URL = lf('users_singnup_url')
DETAIL_URL = lf('news_detail_url')
EDIT_URL = lf('news_edit_url')
DELETE_URL = lf('news_delete_url')
NOT_AUTHOR_CLIENT = lf('not_author_client')
AUTHOR_CLIENT = lf('author_client')
CLIENT_NOT_AUTHORIZATION = Client()


@pytest.mark.parametrize(
    'name, client_test, expected_status',
    ((HOME_URL, CLIENT_NOT_AUTHORIZATION, HTTPStatus.OK),
     (LOGIN_URL, CLIENT_NOT_AUTHORIZATION, HTTPStatus.OK),
     (LOGOUT_URL, CLIENT_NOT_AUTHORIZATION, HTTPStatus.METHOD_NOT_ALLOWED),
     (SINGUP_URL, CLIENT_NOT_AUTHORIZATION, HTTPStatus.OK),
     (DETAIL_URL, CLIENT_NOT_AUTHORIZATION, HTTPStatus.OK),
     (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
     (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
     (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
     (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK))
)
def test_pages_availability_for_different_user(client_test,
                                               name,
                                               expected_status):
    response = client_test.get(name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (DELETE_URL, EDIT_URL),
)
def test_redirect_for_anonymous_client(client, name, users_login_url):
    expected_url = f'{users_login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
