import pytest
from sqlalchemy.orm.scoping import scoped_session

from lab6.app.models import Course, Review, User
from lab6.app.repositories.review_repository import ReviewRepository


def test_get_by_id(review_repository: ReviewRepository, test_review: Review):
    review = review_repository.get_by_id(test_review.id)

    assert review is not None
    assert review.id == test_review.id
    assert review.text == test_review.text
    assert review.rating == test_review.rating


def test_get_all(review_repository: ReviewRepository, test_review: Review):
    reviews = review_repository.get_all()

    assert reviews is not None
    assert len(reviews) >= 1
    assert any(r.id == test_review.id for r in reviews)


def test_get_by_course_id_newest(
    review_repository: ReviewRepository,
    test_course: Course,
    multiple_reviews: list[Review],
):
    paginated_reviews = review_repository.get_by_course_id(
        test_course.id, sort="newest"
    )

    assert paginated_reviews.items is not None
    assert len(paginated_reviews.items) >= 5

    for i in range(len(paginated_reviews.items) - 1):
        assert (
            paginated_reviews.items[i].created_at
            >= paginated_reviews.items[i + 1].created_at
        )


def test_get_by_course_id_positive(
    review_repository: ReviewRepository,
    test_course: Course,
    multiple_reviews: list[Review],
):
    paginated_reviews = review_repository.get_by_course_id(
        test_course.id, sort="positive"
    )

    assert paginated_reviews.items is not None
    assert len(paginated_reviews.items) >= 5

    for i in range(len(paginated_reviews.items) - 1):
        assert (
            paginated_reviews.items[i].rating
            >= paginated_reviews.items[i + 1].rating
        )


def test_get_by_course_id_negative(
    review_repository: ReviewRepository,
    test_course: Course,
    multiple_reviews: list[Review],
):
    paginated_reviews = review_repository.get_by_course_id(
        test_course.id, sort="negative"
    )

    assert paginated_reviews.items is not None
    assert len(paginated_reviews.items) >= 5

    for i in range(len(paginated_reviews.items) - 1):
        assert (
            paginated_reviews.items[i].rating
            <= paginated_reviews.items[i + 1].rating
        )


def test_get_by_course_id_pagination(
    review_repository: ReviewRepository,
    test_course: Course,
    multiple_reviews: list[Review],
):
    paginated_reviews = review_repository.get_by_course_id(
        test_course.id, page=1, per_page=2
    )

    assert paginated_reviews.items is not None
    assert len(paginated_reviews.items) == 2
    assert paginated_reviews.pages == 3


def test_get_latest_by_course_id(
    review_repository: ReviewRepository,
    test_course: Course,
    multiple_reviews: list[Review],
):
    latest_reviews = review_repository.get_latest_by_course_id(
        test_course.id, limit=3
    )

    assert latest_reviews is not None
    assert len(latest_reviews) == 3

    for i in range(len(latest_reviews) - 1):
        assert latest_reviews[i].created_at >= latest_reviews[i + 1].created_at


def test_get_by_user_and_course(
    review_repository: ReviewRepository,
    test_user: User,
    test_course: Course,
    test_review: Review,
):
    review = review_repository.get_by_user_and_course(
        test_user.id, test_course.id
    )

    assert review is not None
    assert review.user_id == test_user.id
    assert review.course_id == test_course.id


def test_create(
    review_repository: ReviewRepository,
    test_user: User,
    test_course: Course,
    db_session: scoped_session,
):
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    review_rating = 5
    review_text = "Great Course!"
    new_review = review_repository.create(
        user_id=test_user.id,
        course_id=test_course.id,
        rating=review_rating,
        text=review_text,
    )

    db_session.refresh(test_course)

    assert new_review is not None
    assert new_review.user_id == test_user.id
    assert new_review.course_id == test_course.id
    assert new_review.rating == review_rating
    assert new_review.text == review_text

    assert test_course.rating_sum == initial_rating_sum + review_rating
    assert test_course.rating_num == initial_rating_num + 1


def test_update(
    review_repository: ReviewRepository,
    test_review: Review,
    test_course: Course,
    db_session: scoped_session,
):
    initial_rating_sum = test_course.rating_sum

    review = review_repository.get_by_id(test_review.id)
    initial_review_rating = review.rating

    review_rating = 5
    review_text = "Excellent Course!"
    review_repository.update(
        review_id=test_review.id, new_rating=review_rating, new_text=review_text
    )

    db_session.refresh(test_course)
    db_session.refresh(test_review)

    assert test_review.rating == review_rating
    assert test_review.text == review_text

    assert (
        test_course.rating_sum
        == initial_rating_sum + review_rating - initial_review_rating
    )


def test_update_nonexistent_review(review_repository, test_review):
    with pytest.raises(Exception) as err:
        review_repository.update(
            review_id=test_review.id + 1,
            new_rating=5,
            new_text="Обновленный отзыв",
        )

    assert "Ошибка при изменении отзыва: Отзыв не найден" in str(err)


def test_delete(review_repository, test_review, test_course, db_session):
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num
    review_id = test_review.id
    review_rating = test_review.rating

    review_repository.delete(review_id)

    db_session.refresh(test_course)

    deleted_review = review_repository.get_by_id(review_id)
    assert deleted_review is None

    assert test_course.rating_sum == initial_rating_sum - review_rating
    assert test_course.rating_num == initial_rating_num - 1


def test_delete_nonexistent_review(review_repository, test_review):
    with pytest.raises(Exception) as err:
        review_repository.delete(test_review.id + 1)

    assert "Ошибка при удалении отзыва: Отзыв не найден" in str(err)
