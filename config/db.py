from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER_DB = "root"
PASSWORD_DB = ""
HOST_DB = "localhost"
PORT_DB = "3306"
NAME_DB = "lavarenta"

engine = create_engine(
    f"mysql+pymysql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}", echo=True
)

database_conection = engine.connect()

metadata = MetaData()

Base = declarative_base(metadata=metadata)

Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)

    print("Database created")
