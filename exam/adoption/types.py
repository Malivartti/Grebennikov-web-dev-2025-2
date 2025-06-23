from enum import StrEnum


class AdoptionStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REJECTED_ADOPTED = "rejected_adopted"


adoption_status_label: dict[AdoptionStatus, str] = {
    AdoptionStatus.PENDING: "Ожидает расмотрения",
    AdoptionStatus.ACCEPTED: "Принята",
    AdoptionStatus.REJECTED: "Отклонена",
    AdoptionStatus.REJECTED_ADOPTED: "Отклонена (из-за усыновления)",
}
