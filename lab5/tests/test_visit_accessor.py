import pytest


def test_add_visit_success(visit_accessor, ordinary_user):
    visit_path = "/test-path"
    visit_log = visit_accessor.add_visit(visit_path, ordinary_user.id)

    assert visit_log is not None
    assert visit_log.path == visit_path
    assert visit_log.user_id == ordinary_user.id


def test_add_visit_without_user(visit_accessor, db_session):
    visit_path = "/anonymous-path"
    visit_log = visit_accessor.add_visit(visit_path)

    assert visit_log is not None
    assert visit_log.path == visit_path
    assert visit_log.user_id is None


def test_add_visit_exception(visit_accessor, monkeypatch, db_session):
    def mock_visit_add(*args, **kwargs):
        raise Exception("Ошибка при добавлении записи в журнал: ")

    monkeypatch.setattr(visit_accessor, "add_visit", mock_visit_add)
    with pytest.raises(Exception) as err:  # noqa: PT011
        visit_accessor.add_visit("/test-path", 1)
    assert "Ошибка при добавлении записи в журнал: " in str(err)


def test_get_visits_with_user_filter(visit_accessor, ordinary_user, admin_user):
    visit_accessor.add_visit("/test-path-1", ordinary_user.id)
    visit_accessor.add_visit("/test-path-2", ordinary_user.id)
    visit_accessor.add_visit("/test-path-3", admin_user.id)

    items, _ = visit_accessor.get_visits(
        page=1, per_page=10, user_id=ordinary_user.id
    )
    assert len(items) == 2
    for item in items:
        visit_log, _ = item
        assert visit_log.user_id == ordinary_user.id


def test_get_visits_without_filter(visit_accessor, ordinary_user):
    visit_accessor.add_visit("/page1", ordinary_user.id)
    visit_accessor.add_visit("/page2", None)
    items, _ = visit_accessor.get_visits()
    assert len(items) >= 2
