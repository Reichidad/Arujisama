from arujisama_flask.app import db
from sqlalchemy import Column, ForeignKey


class UserAccount(db.Model):
    __tablename__ = "user_account"
    __table_args__ = {'mysql_collate':'utf8mb4_general_ci'}
    id = Column(db.CHAR(20), nullable=False, primary_key=True, unique=True)
    pw = Column(db.CHAR(70), nullable=False)
    submitdate = Column(db.DateTime, nullable=True)
    current_valid = Column(db.CHAR(1), nullable=False)


    def __init__(self, id, pw, submitdate=None, current_valid="X"):
        self.id = id
        self.pw = pw
        self.submitdate = submitdate
        self.current_valid = current_valid



class UserInfo(db.Model):
    __tablename__ = "user_info"
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}
    id = Column(db.CHAR(20), ForeignKey("user_account.id", ondelete='CASCADE'), nullable=False, primary_key=True)
    name = Column(db.CHAR(30), nullable=False)
    email = Column(db.CHAR(50), nullable=False)
    current_valid = Column(db.CHAR(50), nullable=False)

    def __init__(self, id, name, email, current_valid="X"):
        self.id = id
        self.name = name
        self.email = email
        self.current_valid = current_valid


'''
class CardList(db.Model):
    idx = Column(db.Integer, primary_key=True, nullable=False)
    id = Column(db.CHAR(20), ForeignKey("user_account.id", ondelete='CASCADE'), nullable=False)
    card_title = Column(db.CHAR(50), nullable=False)

    def __init__(self, id, card_title):
        self.id = id
        self.card_title = card_title
'''


class StampBox(db.Model):
    __tablename__ = "stamp_box"
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}
    idx = Column(db.Integer, primary_key=True, nullable=False)
    # card_idx = Column(db.Integer, ForeignKey("card_list.idx", ondelete='CASCADE'), nullable=False)
    id = Column(db.CHAR(20), ForeignKey("user_account.id", ondelete='CASCADE'), nullable=False)
    submitdate = Column(db.DateTime, nullable=False)
    memo = Column(db.CHAR(100), nullable=True)
    validstamp = Column(db.CHAR(1), nullable=False)

    def __init__(self, id, submitdate, memo=None, validstamp='O'):
        self.id = id
        self.submitdate = submitdate
        self.memo = memo
        self.validstamp = validstamp
