from sqlalchemy import select

from lab6.app.models import Course, Review


class ReviewRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, review_id):
        return self.db.session.get(Review, review_id)

    def get_all(self):
        return self.db.session.query(Review).all()

    def get_by_course_id(self, course_id, sort="newest", page=1, per_page=10):
        query = select(Review).filter(Review.course_id == course_id)

        if sort == "newest":
            query = query.order_by(Review.created_at.desc())
        elif sort == "positive":
            query = query.order_by(
                Review.rating.desc(), Review.created_at.desc()
            )
        elif sort == "negative":
            query = query.order_by(
                Review.rating.asc(), Review.created_at.desc()
            )

        return self.db.paginate(query, page=page, per_page=per_page)

    def get_latest_by_course_id(self, course_id, limit=5):
        return (
            self.db.session.query(Review)
            .filter(Review.course_id == course_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_user_and_course(self, user_id, course_id):
        return (
            self.db.session.query(Review)
            .filter(Review.user_id == user_id, Review.course_id == course_id)
            .first()
        )

    def create(self, user_id, course_id, rating, text):
        error_text = "Ошибка при создании отзыва: "

        try:
            review = Review(
                user_id=user_id, course_id=course_id, rating=rating, text=text
            )

            course = self.db.session.get(Course, course_id)

            course.rating_sum += int(rating)
            course.rating_num += 1

            self.db.session.add(review)
            self.db.session.commit()
        except Exception as err:
            self.db.session.rollback()
            raise Exception(error_text + str(err)) from err
        else:
            return review

    def update(self, review_id, new_rating, new_text):
        error_text = "Ошибка при изменении отзыва: "
        review = self.get_by_id(review_id)
        if not review:
            raise Exception(error_text + "Отзыв не найден")

        try:
            old_rating = review.rating
            review.rating = new_rating
            review.text = new_text

            course = self.db.session.get(Course, review.course_id)
            course.rating_sum = course.rating_sum - old_rating + new_rating

            self.db.session.commit()
        except Exception as err:
            self.db.session.rollback()
            raise Exception(error_text + str(err)) from err

    def delete(self, review_id):
        error_text = "Ошибка при удалении отзыва: "
        review = self.get_by_id(review_id)
        if not review:
            raise Exception(error_text + "Отзыв не найден")

        try:
            course = self.db.session.get(Course, review.course_id)
            course.rating_sum -= review.rating
            course.rating_num -= 1

            self.db.session.delete(review)
            self.db.session.commit()
        except Exception as err:
            self.db.session.rollback()
            raise Exception(error_text + str(err)) from err
