from .main import *


def init_db():
    Base.metadata.create_all(bind=engine)

    User.query.delete()

    entities = [
        User(user_cd='u-001'),
        User(user_cd='u-002'),
        User(user_cd='u-003'),
        User(user_cd='u-004'),
        User(user_cd='u-005'),
    ]

    session.add_all(entities)
    session.commit()


if __name__ == '__main__':
    init_db()
