from models import db, Task, User


class TaskRepository:
    @staticmethod
    def get_all_tasks():
        return Task.query.all()

    @staticmethod
    def get_task_by_id(task_id):
        return Task.query.get(task_id)

    @staticmethod
    def add_task(task_data):
        new_task = Task(**task_data)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def updated_task(task_id, task_data):
        task = Task.query.get(task_id)
        if task:
            for k, v in task.items():
                setattr(task, k, v)
            db.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return task


class UserRepository:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def add_user(user_data):
        new_user = User(**user_data)
        db.session.add(new_user)
        sb.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, user_data):
        user = User.query.get(user_id)
        if user:
            for k, v in user.items():
                setattr(user, k, v)
            db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
