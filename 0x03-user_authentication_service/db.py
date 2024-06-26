#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates user
        Parameters:
          email (str): User email
          hashed_password (str): Hashed user password
        Returns:
          User object
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds and returns first row found in the `users` table.
        """
        attributes = []
        values = []
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
            attributes.append(getattr(User, key))
            values.append(value)

        result = self._session.query(User).filter(
                tuple_(*attributes).in_([tuple(values)])
            ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user based on user id.
        Parameters:
          user_id (int): User id
        Returns:
          None
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            setattr(user, key, value)
        self._session.commit()
