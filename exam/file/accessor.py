import os
import uuid

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from exam.config import UPLOAD_FOLDER


class FileAccessor:
    def _generate_filename(self, original_filename: str) -> str:
        file_extension = (
            secure_filename(original_filename).rsplit(".", 1)[1].lower()
        )
        return f"{uuid.uuid4().hex}.{file_extension}"

    def save_file(
        self, *, file: FileStorage, filename: str | None = None
    ) -> str:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        if filename is None:
            filename = self._generate_filename(file.filename)

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename

    def delete_file(self, *, filename: str) -> bool:
        if not filename:
            return False

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                current_app.logger.exception(
                    "Не удалось удалить файл %s", file_path
                )
                return False
            else:
                return True
        return True

    def delete_files(self, *, filenames: list) -> dict:
        results = {"success": [], "failed": []}
        for filename in filenames:
            if self.delete_file(filename=filename):
                results["success"].append(filename)
            else:
                results["failed"].append(filename)
        return results
