def test_get_user_by_id(user_accessor, test_user):
    user = user_accessor.get_user_by_id(test_user.id)
    assert user is not None
    assert user.id == test_user.id
    assert user.login == test_user.login


def test_get_user_by_login(user_accessor, test_user):
    user = user_accessor.get_user_by_login(test_user.login)
    assert user is not None
    assert user.id == test_user.id
    assert user.login == test_user.login


def test_get_users(user_accessor, test_user):
    users = user_accessor.get_users()
    assert len(users) >= 1
    assert any(u.id == test_user.id for u in users)


def test_get_role(user_accessor, test_role):
    role = user_accessor.get_role_by_id(test_role.id)
    assert role.id == test_role.id


def test_get_roles(user_accessor, test_roles):
    roles = user_accessor.get_roles()
    assert roles == test_roles


def test_create_user(user_accessor, db_session):
    user_data = {
        "login": "newuser",
        "password": "password123",
        "last_name": "New",
        "first_name": "User",
        "middle_name": "Test",
    }

    new_user = user_accessor.create_user(user_data)
    assert new_user.id is not None
    assert new_user.login == "newuser"

    fetched_user = user_accessor.get_user_by_login("newuser")
    assert fetched_user is not None
    assert fetched_user.id == new_user.id


def test_update_user(user_accessor, test_user):
    updates = {"last_name": "Updated", "first_name": "Name"}

    user_accessor.update_user(test_user.id, updates)

    updated_user = user_accessor.get_user_by_id(test_user.id)
    assert updated_user.last_name == "Updated"
    assert updated_user.first_name == "Name"


def test_delete_user(user_accessor, db_session):
    user_data = {
        "login": "delete_me",
        "password": "password123",
        "last_name": "Delete",
        "first_name": "Me",
    }

    user_to_delete = user_accessor.create_user(user_data)
    user_id = user_to_delete.id

    user_accessor.delete_user(user_id)

    deleted_user = user_accessor.get_user_by_id(user_id)
    assert deleted_user is None


def test_password_hashing_and_verification(user_accessor):
    password = "securepassword"
    hashed = user_accessor.hash_password(password)

    assert hashed != password

    assert user_accessor.verify_password(password, hashed) is True

    assert user_accessor.verify_password("wrongpassword", hashed) is False
