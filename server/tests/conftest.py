import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

os.environ["ENV"] = "test"

from ..api.main import app
from ..api.bll.base import Base


@pytest.fixture(scope='session')
def init_db():
    engine = create_engine(os.getenv("DATABASE_URL_TEST_SYNC"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    Base.metadata.create_all(bind=engine)
    session.close()
    engine.dispose()

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(init_db):
    with TestClient(app) as c:
        yield c
