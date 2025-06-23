from typing import TYPE_CHECKING, cast

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from exam.animal.models import AnimalStatus, Sex
from exam.animal.schemas import AnimalListParams, CreateAnimal, UpdateAnimal
from exam.auth import check_rights
from exam.user.types import Right

if TYPE_CHECKING:
    from exam.app import Application

    current_app = cast(Application, current_app)

bp = Blueprint("animal", __name__, url_prefix="/animals")

sexes = [
    {"value": Sex.MALE, "label": "Мужской"},
    {"value": Sex.FEMALE, "label": "Женский"},
]
statuses = [
    {"value": AnimalStatus.AVAILABLE, "label": "Доступен для усыновления"},
    {"value": AnimalStatus.ADOPTION, "label": "В процессе усыновления"},
    {"value": AnimalStatus.ADOPTED, "label": "Усыновлен"},
]


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search")
    sex = request.args.get("sex")
    status = request.args.get("status")

    params = AnimalListParams(
        page=page,
        per_page=per_page,
        search=search,
        sex=Sex(sex) if sex else None,
        status=AnimalStatus(status) if status else None,
    )

    result = current_app.store.animal.get_animals(params=params)

    return render_template(
        "animals/index.html",
        animals=result["data"],
        total_count=result["count"],
        page=page,
        per_page=per_page,
        search=search,
        selected_sex=sex,
        selected_status=status,
        sexes=sexes,
        statuses=statuses,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
@check_rights([Right.ANIMAL_CREATE])
def create():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            breed = request.form.get("breed", "").strip()
            description = request.form.get("description", "").strip()
            age_months = request.form.get("age_months")
            sex = request.form.get("sex")

            if not all([name, breed, description, age_months, sex]):
                flash("Все поля являются обязательными", "danger")
                return render_template(
                    "animals/form.html",
                    title="Добавить животное",
                    sexes=sexes,
                )

            try:
                age_months = int(age_months)
                if age_months < 1:
                    raise ValueError("Возраст должен быть больше 0")
            except ValueError:
                flash("Возраст должен быть положительным числом", "danger")
                return render_template(
                    "animals/form.html",
                    title="Добавить животное",
                    sexes=sexes,
                )
            files = request.files.getlist("images")
            images_data = []
            if files and files[0].filename:
                for file in files:
                    if file.filename:
                        filename = current_app.store.file.save_file(file=file)
                        images_data.append(
                            {
                                "filename": filename,
                                "mime_type": file.mimetype,
                                "animal_id": None,
                            }
                        )

            create_animal_data = CreateAnimal(
                name=name,
                description=description,
                age_months=age_months,
                breed=breed,
                sex=Sex(sex),
            )

            animal = current_app.store.animal.create_animal_with_images(
                create_animal=create_animal_data, images_data=images_data
            )

            flash("Животное успешно добавлено!", "success")
            return redirect(url_for("animal.view", id=animal.id))

        except Exception as e:
            flash(f"Ошибка при создании: {e}", "danger")
            current_app.logger.exception("Ошибка при создании животного")

    return render_template(
        "animals/form.html",
        title="Добавить животное",
        sexes=sexes,
    )


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
@check_rights([Right.ANIMAL_UPDATE])
def update(id):
    animal = current_app.store.animal.get_animal_by_id(animal_id=id)
    if not animal:
        flash("Животное не найдено", "error")
        return redirect(url_for("animal.index"))

    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            breed = request.form.get("breed", "").strip()
            description = request.form.get("description", "").strip()
            age_months = request.form.get("age_months")
            sex = request.form.get("sex")

            if not all([name, breed, description, age_months, sex]):
                flash("Все поля являются обязательными", "danger")
                return render_template(
                    "animals/form.html",
                    title="Редактировать животное",
                    animal=animal,
                    sexes=sexes,
                )

            try:
                age_months = int(age_months)
                if age_months < 1:
                    raise ValueError("Возраст должен быть больше 0")
            except ValueError:
                flash("Возраст должен быть положительным числом", "danger")
                return render_template(
                    "animals/form.html",
                    title="Редактировать животное",
                    animal=animal,
                    sexes=sexes,
                )

            update_animal_data = UpdateAnimal(
                id=id,
                name=name,
                description=description,
                age_months=age_months,
                breed=breed,
                sex=Sex(sex),
            )

            updated_animal = current_app.store.animal.update_animal(
                update_animal=update_animal_data
            )

            if updated_animal:
                flash("Животное успешно обновлено!", "success")
                return redirect(url_for("animal.view", id=id))

            flash("Ошибка при обновлении", "danger")

        except Exception as e:
            flash(f"Ошибка при обновлении: {e}", "danger")
            current_app.logger.exception(
                "Ошибка при обновлении животного %s", id
            )
            return render_template(
                "animals/form.html",
                title="Редактировать животное",
                animal=animal,
                sexes=sexes,
            )

    return render_template(
        "animals/form.html",
        title="Редактировать животное",
        animal=animal,
        sexes=sexes,
    )


@bp.route("/<int:id>")
def view(id):
    animal = current_app.store.animal.get_animal_by_id(animal_id=id)
    if not animal:
        flash("Животное не найдено", "danger")
        return redirect(url_for("animal.index"))

    adoptions = []
    adoption_page = 1
    adoption_per_page = 5
    adoption_total_count = 0

    if check_rights([Right.ADOPTION_MANAGE]):
        adoption_page = request.args.get("adoption_page", 1, type=int)
        adoption_per_page = request.args.get("adoption_per_page", 5, type=int)

        adoption_result = current_app.store.adoption.get_adoptions_by_animal_id(
            animal_id=id, page=adoption_page, per_page=adoption_per_page
        )

        adoptions = adoption_result["data"]
        adoption_total_count = adoption_result["count"]

    user_adoption = None
    if current_user.is_authenticated and check_rights([Right.ADOPTION_CREATE]):
        user_adoption = current_app.store.adoption.get_user_adoption_for_animal(
            user_id=current_user.id, animal_id=id
        )

    return render_template(
        "animals/view.html",
        animal=animal,
        adoptions=adoptions,
        adoption_page=adoption_page,
        adoption_per_page=adoption_per_page,
        adoption_total_count=adoption_total_count,
        user_adoption=user_adoption,
    )


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@check_rights([Right.ANIMAL_DELETE])
def delete(id):
    animal = current_app.store.animal.get_animal_by_id(animal_id=id)
    if not animal:
        flash("Животное не найдено", "error")
        return redirect(url_for("animal.index"))

    try:
        result = current_app.store.animal.delete_animal(animal_id=id)
        if result:
            flash("Животное успешно удалено", "success")
        else:
            flash("Ошибка при удалении животного", "danger")
    except Exception as e:
        flash(f"Ошибка при удалении: {e}", "danger")
        current_app.logger.exception("Ошибка при удалении животного %s", id)

    return redirect(url_for("animal.index"))


@bp.route("/<int:animal_id>/images/<int:image_id>/delete", methods=["POST"])
@login_required
@check_rights([Right.ANIMAL_UPDATE])
def delete_image(animal_id, image_id):
    animal = current_app.store.animal.get_animal_by_id(animal_id=animal_id)
    if not animal:
        flash("Животное не найдено", "error")
        return redirect(url_for("animal.index"))

    try:
        result = current_app.store.animal.delete_image(image_id=image_id)
        if result:
            flash("Изображение успешно удалено", "success")
        else:
            flash("Ошибка при удалении изображения", "danger")
    except Exception as e:
        flash(f"Ошибка при удалении изображения: {e}", "danger")
        current_app.logger.exception(
            "Ошибка при удалении изображения %s", image_id
        )

    return redirect(url_for("animal.view", id=animal_id))


@bp.route("/<int:id>/adoptions", methods=["POST"])
@login_required
@check_rights([Right.ADOPTION_CREATE])
def create_adoption(id):
    animal = current_app.store.animal.get_animal_by_id(animal_id=id)
    if not animal:
        flash("Животное не найдено", "error")
        return redirect(url_for("animal.index"))

    existing_adoption = current_app.store.adoption.get_user_adoption_for_animal(
        user_id=current_user.id, animal_id=id
    )
    if existing_adoption:
        flash("Вы уже подали заявку на это животное", "warning")
        return redirect(url_for("animal.view", id=id))

    contact = request.form.get("contact", "").strip()
    if not contact:
        flash("Контактные данные обязательны", "danger")
        return redirect(url_for("animal.view", id=id))

    try:
        current_app.store.adoption.create_adoption(
            animal_id=id, user_id=current_user.id, contact=contact
        )
        flash("Заявка успешно подана!", "success")
    except Exception:
        flash("Ошибка при подаче заявки", "danger")
        current_app.logger.exception("Ошибка создания заявки")

    return redirect(url_for("animal.view", id=id))


@bp.route("/adoptions/<int:adoption_id>/accept", methods=["POST"])
@login_required
@check_rights([Right.ADOPTION_MANAGE])
def accept_adoption(adoption_id):
    try:
        result = current_app.store.adoption.accept_adoption(
            adoption_id=adoption_id
        )
        if result:
            flash("Заявка принята!", "success")
        else:
            flash("Заявка не найдена", "danger")
    except Exception:
        flash("Ошибка при принятии заявки", "danger")
        current_app.logger.exception("Ошибка принятия заявки %s", adoption_id)

    return redirect(request.referrer or url_for("animal.index"))


@bp.route("/adoptions/<int:adoption_id>/reject", methods=["POST"])
@login_required
@check_rights([Right.ADOPTION_MANAGE])
def reject_adoption(adoption_id):
    try:
        result = current_app.store.adoption.reject_adoption(
            adoption_id=adoption_id
        )
        if result:
            flash("Заявка отклонена", "success")
        else:
            flash("Заявка не найдена", "danger")
    except Exception:
        flash("Ошибка при отклонении заявки", "danger")
        current_app.logger.exception("Ошибка отклонения заявки %s", adoption_id)

    return redirect(request.referrer or url_for("animal.index"))
