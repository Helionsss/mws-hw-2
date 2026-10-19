from uuid import uuid4

from api.rest_api import RestApi


def test_create_patch_get_post_keeps_id_and_untouched_fields():
    api = RestApi()
    original_title = f"autotest post {uuid4()}"
    original_body = f"autotest body {uuid4()}"
    patched_title = f"{original_title} (patched)"

    created_response = api.create_post(original_title, original_body)
    assert created_response.status_code == 201, created_response.text
    created_post = created_response.json()
    post_id = created_post.get("id")
    assert post_id, created_post
    assert created_post.get("title") == original_title, created_post

    patched_response = api.patch_post(post_id, title=patched_title)
    assert patched_response.status_code == 200, patched_response.text
    assert patched_response.json().get("title") == patched_title, patched_response.text

    fetched_response = api.get_post(post_id)
    assert fetched_response.status_code == 200, fetched_response.text
    fetched_post = fetched_response.json()
    assert fetched_post.get("id") == post_id, fetched_post
    assert fetched_post.get("title") == patched_title, fetched_post
    assert fetched_post.get("body") == original_body, fetched_post
