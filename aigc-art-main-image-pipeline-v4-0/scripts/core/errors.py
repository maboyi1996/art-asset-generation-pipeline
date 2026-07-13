"""Shared V4 pipeline exceptions."""

class PipelineError(Exception):
    """Base error with a stable machine code."""
    code = "pipeline_error"

    def __init__(self, message: str, *, artifact_id: str = "", record_id: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.artifact_id = artifact_id
        self.record_id = record_id

    def as_dict(self) -> dict:
        value = {"code": self.code, "message": self.message}
        if self.artifact_id:
            value["artifact_id"] = self.artifact_id
        if self.record_id:
            value["record_id"] = self.record_id
        return value

class ContractError(PipelineError):
    code = "contract_error"

class InputError(PipelineError):
    code = "input_error"

class ValidationError(PipelineError):
    code = "validation_error"

class IntegrityError(PipelineError):
    code = "integrity_error"
