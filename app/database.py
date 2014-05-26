# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# SQLALCHEMY_DATABASE_URI = 'sqlite:///anarcho.db'
#
# engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     import app.models
#
#     Base.metadata.create_all(bind=engine)
#     print('Database initialized...')
