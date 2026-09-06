from app import schemas
from typing import List


def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts")

    def validate(post):
        return schemas.PostWithVotes(**post)

    posts_map = map(validate, res.json())
    print(list(posts_map))

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200


def test_unauthorized_user_get_all_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 200


