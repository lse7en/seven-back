from src.tasks.frinds_tasks import friend_extra_check
from src.tasks.group_logs import save_log as save_log_task


from fastapi import Request, BackgroundTasks


class BackgroundTasksWrapper:
    def __init__(self, request: Request, background_tasks: BackgroundTasks):
        self.session_factory = request.app.state.session_factory
        self.background_tasks = background_tasks

    def add_task(self, func, *args, **kwargs):
        self.background_tasks.add_task(
            func, session_factory=self.session_factory, **kwargs
        )

    def save_log(self, user_id: int, command: str, tag):
        self.add_task(save_log_task, user_id=user_id, command=command, tag=tag)

    def friend_extra_check(self, user_id: int, current_status, task):
        self.add_task(friend_extra_check, user_id=user_id, current_status=current_status, task=task)
