from datetime import datetime

from flask_sqlalchemy.extension import Pagination
from sqlalchemy import desc, func

from lab5.base.accessor import BaseAccessor
from lab5.user.models import User
from lab5.visit.models import VisitLog


class VisitAccessor(BaseAccessor):
    def add_visit(self, path: str, user_id: int | None = None) -> VisitLog:
        error_text = "Ошибка при добавлении записи в журнал: "

        try:
            visit_log = VisitLog(
                path=path, user_id=user_id, created_at=datetime.now()
            )
            self.app.db.session.add(visit_log)
            self.app.db.session.commit()
        except Exception as err:
            self.app.db.session.rollback()
            raise Exception(error_text + str(err)) from err
        else:
            return visit_log

    def get_visits(
        self, page: int = 1, per_page: int = 10, user_id: int | None = None
    ) -> tuple[list[tuple[VisitLog, User]], Pagination]:
        base_query = self.app.db.session.query(VisitLog)

        if user_id is not None:
            base_query = base_query.filter(VisitLog.user_id == user_id)

        base_query = base_query.order_by(desc(VisitLog.created_at))

        pagination = self.app.db.paginate(
            base_query, page=page, per_page=per_page
        )

        visit_ids = [visit.id for visit in pagination.items]

        if not visit_ids:
            return [], pagination

        joined_query = (
            self.app.db.session.query(VisitLog, User)
            .outerjoin(User, VisitLog.user_id == User.id)
            .filter(VisitLog.id.in_(visit_ids))
            .order_by(desc(VisitLog.created_at))
        )

        items = joined_query.all()

        return items, pagination

    def get_page_stats(self):
        return (
            self.app.db.session.query(
                VisitLog.path, func.count(VisitLog.id).label("count")
            )
            .group_by(VisitLog.path)
            .order_by(desc("count"))
            .all()
        )

    def get_user_stats(
        self,
    ):
        user_stats = (
            self.app.db.session.query(
                User.id,
                User.last_name,
                User.first_name,
                User.middle_name,
                func.count(VisitLog.id).label("count"),
            )
            .outerjoin(User, VisitLog.user_id == User.id)
            .filter(VisitLog.user_id.isnot(None))
            .group_by(
                User.id, User.last_name, User.first_name, User.middle_name
            )
            .order_by(desc("count"))
            .all()
        )

        anon_count = (
            self.app.db.session.query(func.count(VisitLog.id))
            .filter(VisitLog.user_id.is_(None))
            .scalar()
            or 0
        )

        if anon_count > 0:
            user_stats = list(user_stats)
            user_stats.append(
                (
                    None,
                    None,
                    None,
                    None,
                    anon_count,
                )
            )

        return user_stats
