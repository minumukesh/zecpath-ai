class ATSAPIException(Exception):

    def __init__(
        self,
        error_code,
        message,
        status_code=400
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ResumeNotFoundError(ATSAPIException):

    def __init__(self, resume_id):
        super().__init__(
            "RESUME_NOT_FOUND",
            f"Resume '{resume_id}' was not found.",
            404
        )


class JobNotFoundError(ATSAPIException):

    def __init__(self, job_id):
        super().__init__(
            "JOB_NOT_FOUND",
            f"Job '{job_id}' was not found.",
            404
        )


class InvalidResumeError(ATSAPIException):

    def __init__(self, message):
        super().__init__(
            "INVALID_RESUME",
            message,
            400
        )


class UnsupportedFileError(ATSAPIException):

    def __init__(self, filename):
        super().__init__(
            "UNSUPPORTED_FILE_TYPE",
            f"Unsupported file type: '{filename}'. Only TXT files are supported.",
            415
        )
