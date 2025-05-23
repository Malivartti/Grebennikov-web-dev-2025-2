from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from lab6.app.models import db
from lab6.app.repositories import (
    CategoryRepository,
    CourseRepository,
    ImageRepository,
    ReviewRepository,
    UserRepository,
)

user_repository = UserRepository(db)
course_repository = CourseRepository(db)
category_repository = CategoryRepository(db)
image_repository = ImageRepository(db)
review_repository = ReviewRepository(db)

bp = Blueprint("courses", __name__, url_prefix="/courses")

COURSE_PARAMS = ["author_id", "name", "category_id", "short_desc", "full_desc"]


def params():
    return {p: request.form.get(p) or None for p in COURSE_PARAMS}


def search_params():
    return {
        "name": request.args.get("name"),
        "category_ids": [x for x in request.args.getlist("category_ids") if x],
    }


@bp.route("/")
def index():
    pagination = course_repository.get_pagination_info(**search_params())
    courses = course_repository.get_all_courses(pagination=pagination)
    categories = category_repository.get_all_categories()
    return render_template(
        "courses/index.html",
        courses=courses,
        categories=categories,
        pagination=pagination,
        search_params=search_params(),
    )


@bp.route("/new")
@login_required
def new():
    course = course_repository.new_course()
    categories = category_repository.get_all_categories()
    users = user_repository.get_all_users()
    return render_template(
        "courses/new.html", categories=categories, users=users, course=course
    )


@bp.route("/create", methods=["POST"])
@login_required
def create():
    f = request.files.get("background_img")
    img = None
    course = None

    try:
        if f and f.filename:
            img = image_repository.add_image(f)

        image_id = img.id if img else None
        course = course_repository.add_course(
            **params(), background_image_id=image_id
        )
    except IntegrityError as err:
        flash(
            "Возникла ошибка при записи данных в БД."
            f" Проверьте корректность введённых данных. ({err})",
            "danger",
        )
        categories = category_repository.get_all_categories()
        users = user_repository.get_all_users()
        return render_template(
            "courses/new.html",
            categories=categories,
            users=users,
            course=course,
        )

    flash(f"Курс {course.name} был успешно добавлен!", "success")

    return redirect(url_for("courses.index"))


@bp.route("/<int:course_id>")
def show(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)

    latest_reviews = review_repository.get_latest_by_course_id(course_id, 5)

    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_by_user_and_course(
            current_user.id, course_id
        )

    return render_template(
        "courses/show.html",
        course=course,
        latest_reviews=latest_reviews,
        user_review=user_review,
    )


@bp.route("/<int:course_id>/reviews")
def reviews(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)

    sort = request.args.get("sort", "newest")
    page = request.args.get("page", 1, type=int)

    pagination = review_repository.get_by_course_id(course_id, sort, page)

    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_by_user_and_course(
            current_user.id, course_id
        )

    return render_template(
        "courses/reviews.html",
        course=course,
        reviews=pagination.items,
        pagination=pagination,
        sort=sort,
        user_review=user_review,
    )


@bp.route("/<int:course_id>/reviews/create", methods=["POST"])
@login_required
def create_review(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)

    next_page = request.form.get("next") or url_for(
        "courses.show", course_id=course_id
    )

    existing_review = review_repository.get_by_user_and_course(
        current_user.id, course_id
    )
    if existing_review:
        flash("Вы уже оставили отзыв для этого курса", "warning")
        return redirect(next_page)

    rating = request.form.get("rating", type=int)
    text = request.form.get("text")

    if rating is None or rating < 0 or rating > 5:
        flash("Некорректная оценка", "danger")
        return redirect(next_page)

    if not text:
        flash("Текст отзыва не может быть пустым", "danger")
        return redirect(next_page)

    try:
        review_repository.create(current_user.id, course_id, rating, text)
        flash("Отзыв успешно добавлен", "success")
    except Exception as err:
        flash(str(err), "danger")

    return redirect(next_page)


@bp.route("/<int:course_id>/reviews/<int:review_id>/update", methods=["POST"])
@login_required
def update_review(course_id, review_id):
    review = review_repository.get_by_id(review_id)
    if not review or review.user_id != current_user.id:
        abort(403)

    next_page = request.form.get("next") or url_for(
        "courses.show", course_id=course_id
    )

    rating = request.form.get("rating", type=int)
    text = request.form.get("text")

    if rating is None or rating < 0 or rating > 5:
        flash("Некорректная оценка", "danger")
        return redirect(next_page)

    if not text:
        flash("Текст отзыва не может быть пустым", "danger")
        return redirect(next_page)

    try:
        review_repository.update(review_id, rating, text)
        flash("Отзыв успешно обновлен", "success")
    except Exception as err:
        flash(str(err), "danger")

    return redirect(next_page)


@bp.route("/<int:course_id>/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(course_id, review_id):
    review = review_repository.get_by_id(review_id)

    if not review or review.user_id != current_user.id:
        abort(403)

    next_page = request.form.get("next") or url_for(
        "courses.show", course_id=course_id
    )

    try:
        review_repository.delete(review_id)
        flash("Отзыв успешно удален", "success")
    except Exception as err:
        flash(str(err), "danger")

    return redirect(next_page)
