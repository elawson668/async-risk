from asyncrisk.models import *
import functools


def db_transaction(f):
    """
        A function wrapper used to wrap database-transaction methods. Performs a DB commit after performing
        operation of f, which should be a DB transaction (select, update, insert).
    :param f:
    :return:
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        db.session.commit()
        return r

    return wrapper


@db_transaction
def save(record):
    db.session.add(record)


@db_transaction
def save_all(records):
    db.session.add_all(records)

