from enum import StrEnum, auto


class AdoptionStatus(StrEnum):
    PENDING = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    REJECTED_ADOPTED = auto()


adoption_status_label: dict[AdoptionStatus, str] = {
    AdoptionStatus.PENDING: "Ожидает расмотрения",
    AdoptionStatus.ACCEPTED: "Принята",
    AdoptionStatus.REJECTED: "Отклонена",
    AdoptionStatus.REJECTED_ADOPTED: "Отклонена (из-за усыновления)",
}
