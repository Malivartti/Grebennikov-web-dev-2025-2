import re

import pytest
from flask import url_for


def test_create_review(
    test_client, test_course, test_user, review_repository, db_session
):
    initial_reviews_count = len(review_repository.get_all())
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    review_rating = 4
    review_text = "Great course!"

    response = test_client.post(
        url_for("courses.create_review", course_id=test_course.id),
        data={"rating": review_rating, "text": review_text},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Отзыв успешно добавлен" in response.text

    db_session.refresh(test_course)
    reviews = review_repository.get_all()
    assert len(reviews) == initial_reviews_count + 1

    new_review = review_repository.get_by_user_and_course(
        test_user.id, test_course.id
    )
    assert new_review is not None
    assert new_review.rating == review_rating
    assert new_review.text == review_text

    assert test_course.rating_sum == initial_rating_sum + review_rating
    assert test_course.rating_num == initial_rating_num + 1


def test_create_rating_error(
    test_client, test_course, test_user, review_repository, db_session
):
    initial_reviews_count = len(review_repository.get_all())
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    response = test_client.post(
        url_for("courses.create_review", course_id=test_course.id),
        data={"rating": 6, "text": "Invalid rating"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Некорректная оценка" in response.text

    db_session.refresh(test_course)
    reviews = review_repository.get_all()
    assert len(reviews) == initial_reviews_count

    review = review_repository.get_by_user_and_course(
        test_user.id, test_course.id
    )
    assert review is None

    assert test_course.rating_sum == initial_rating_sum
    assert test_course.rating_num == initial_rating_num


def test_create_text_error(
    test_client, test_course, test_user, review_repository, db_session
):
    initial_reviews_count = len(review_repository.get_all())
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    response = test_client.post(
        url_for("courses.create_review", course_id=test_course.id),
        data={"rating": 3, "text": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Текст отзыва не может быть пустым" in response.text

    db_session.refresh(test_course)
    reviews = review_repository.get_all()
    assert len(reviews) == initial_reviews_count

    review = review_repository.get_by_user_and_course(
        test_user.id, test_course.id
    )
    assert review is None

    assert test_course.rating_sum == initial_rating_sum
    assert test_course.rating_num == initial_rating_num


def test_create_double_error(
    test_client, test_course, test_user, review_repository, db_session
):
    test_client.post(
        url_for("courses.create_review", course_id=test_course.id),
        data={"rating": 5, "text": "Another review"},
        follow_redirects=True,
    )

    initial_reviews_count = len(review_repository.get_all())
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    response = test_client.post(
        url_for("courses.create_review", course_id=test_course.id),
        data={"rating": 4, "text": "Duplicate review"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Вы уже оставили отзыв для этого курса" in response.text

    db_session.refresh(test_course)
    reviews = review_repository.get_all()
    assert len(reviews) == initial_reviews_count

    existing_review = review_repository.get_by_user_and_course(
        test_user.id, test_course.id
    )
    assert existing_review is not None
    assert existing_review.rating == 5
    assert existing_review.text == "Another review"

    assert test_course.rating_sum == initial_rating_sum
    assert test_course.rating_num == initial_rating_num


def test_update_review(
    test_client, test_course, test_review, review_repository, db_session
):
    # Проверяем начальное состояние
    initial_rating = test_review.rating
    initial_rating_sum = test_course.rating_sum

    review_rating = 3

    response = test_client.post(
        url_for(
            "courses.update_review",
            course_id=test_course.id,
            review_id=test_review.id,
        ),
        data={"rating": review_rating, "text": "Updated review text"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Отзыв успешно обновлен" in response.text

    db_session.refresh(test_review)
    db_session.refresh(test_course)

    assert test_review.rating == review_rating
    assert test_review.text == "Updated review text"

    assert (
        test_course.rating_sum
        == initial_rating_sum + review_rating - initial_rating
    )


def test_update_review_rating_error(
    test_client, test_course, test_review, db_session
):
    initial_rating = test_review.rating
    initial_text = test_review.text
    initial_rating_sum = test_course.rating_sum

    response = test_client.post(
        url_for(
            "courses.update_review",
            course_id=test_course.id,
            review_id=test_review.id,
        ),
        data={"rating": -1, "text": "Invalid rating update"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Некорректная оценка" in response.text

    db_session.refresh(test_review)
    db_session.refresh(test_course)

    assert test_review.rating == initial_rating
    assert test_review.text == initial_text

    assert test_course.rating_sum == initial_rating_sum


def test_update_review_text_error(
    test_client, test_course, test_review, db_session
):
    initial_rating = test_review.rating
    initial_text = test_review.text
    initial_rating_sum = test_course.rating_sum

    response = test_client.post(
        url_for(
            "courses.update_review",
            course_id=test_course.id,
            review_id=test_review.id,
        ),
        data={"rating": 4, "text": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Текст отзыва не может быть пустым" in response.text

    db_session.refresh(test_review)
    db_session.refresh(test_course)

    assert test_review.rating == initial_rating
    assert test_review.text == initial_text

    assert test_course.rating_sum == initial_rating_sum


def test_delete_review(
    test_client, test_course, test_review, review_repository, db_session
):
    review_id = test_review.id
    review_rating = test_review.rating
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    response = test_client.post(
        url_for(
            "courses.delete_review",
            course_id=test_course.id,
            review_id=test_review.id,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Отзыв успешно удален" in response.text

    db_session.refresh(test_course)
    deleted_review = review_repository.get_by_id(review_id)
    assert deleted_review is None

    assert test_course.rating_sum == initial_rating_sum - review_rating
    assert test_course.rating_num == initial_rating_num - 1


def test_delete_review_another_client(
    test_client2, test_course, test_review, review_repository, db_session
):
    review_id = test_review.id
    initial_rating = test_review.rating
    initial_text = test_review.text
    initial_rating_sum = test_course.rating_sum
    initial_rating_num = test_course.rating_num

    response = test_client2.post(
        url_for(
            "courses.delete_review",
            course_id=test_course.id,
            review_id=test_review.id,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 403

    db_session.refresh(test_course)
    existing_review = review_repository.get_by_id(review_id)
    assert existing_review is not None
    assert existing_review.rating == initial_rating
    assert existing_review.text == initial_text

    assert test_course.rating_sum == initial_rating_sum
    assert test_course.rating_num == initial_rating_num


def test_reviews_page_display(
    test_client, test_course, multiple_reviews, captured_templates
):
    with captured_templates as templates:
        response = test_client.get(
            url_for("courses.reviews", course_id=test_course.id)
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "courses/reviews.html"
        assert "course" in context
        assert context["course"].id == test_course.id
        assert "reviews" in context
        assert len(context["reviews"]) > 0


@pytest.mark.parametrize("sort_type", ["newest", "positive", "negative"])
def test_reviews_sorting(
    test_client, test_course, multiple_reviews, review_repository, sort_type
):
    def extract_review_texts_from_html(html):
        pattern = re.compile(
            r'<p class="card-text review-text">\s*(.*?)\s*</p>', re.DOTALL
        )
        return [match.strip() for match in pattern.findall(html)]

    response = test_client.get(
        url_for("courses.reviews", course_id=test_course.id, sort=sort_type)
    )
    assert response.status_code == 200

    html_text = extract_review_texts_from_html(response.text)
    db_text = [
        el.text
        for el in review_repository.get_by_course_id(
            test_course.id, sort=sort_type, page=1
        )
    ]
    assert html_text == db_text


def test_course_show_with_reviews(
    test_client, test_course, multiple_reviews, captured_templates
):
    with captured_templates as templates:
        response = test_client.get(
            url_for("courses.show", course_id=test_course.id)
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]

        assert template.name == "courses/show.html"
        assert "course" in context
        assert context["course"].id == test_course.id
        assert "latest_reviews" in context
        assert "user_review" in context


def test_review_form_display_for_authenticated_user(test_client, test_course):
    response = test_client.get(
        url_for("courses.show", course_id=test_course.id)
    )

    assert response.status_code == 200
    content = response.get_data(as_text=True)
    assert "Оставить отзыв" in content
    assert "form" in content
    assert "rating" in content
    assert "text" in content


def test_nonexistent_course_review_creation(test_client, test_course):
    response = test_client.post(
        url_for("courses.create_review", course_id=test_course.id + 1),
        data={"rating": 4, "text": "Great course!"},
        follow_redirects=True,
    )
    assert response.status_code == 404


def test_nonexistent_review_update(test_client, test_course, test_review):
    response = test_client.post(
        url_for(
            "courses.update_review",
            course_id=test_course.id,
            review_id=test_review.id + 1,
        ),
        data={"rating": 3, "text": "Updated review text"},
        follow_redirects=True,
    )
    assert response.status_code == 403


def test_nonexistent_review_delete(test_client, test_course, test_review):
    response = test_client.post(
        url_for(
            "courses.delete_review",
            course_id=test_course.id,
            review_id=test_review.id + 1,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 403
