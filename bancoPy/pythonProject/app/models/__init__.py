"""
Database Models for SINPE Banking System
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_accounts = db.relationship(
        "UserAccount", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30), unique=True, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="CRC")
    balance = db.Column(db.Numeric(15, 2), default=Decimal("0.00"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_accounts = db.relationship(
        "UserAccount", back_populates="account", cascade="all, delete-orphan"
    )
    phone_links = db.relationship(
        "PhoneLink", back_populates="account", cascade="all, delete-orphan"
    )
    sent_transactions = db.relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account",
    )
    received_transactions = db.relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account",
    )

    def to_dict(self):
        # Get the first linked user ID if available
        user_id = None
        if self.user_accounts and len(self.user_accounts) > 0:
            user_id = self.user_accounts[0].user_id

        return {
            "id": self.id,
            "number": self.number,
            "iban": f"CR210152{self.number}",  # Generate IBAN from account number
            "account_type": "savings",  # Default account type
            "currency": self.currency,
            "balance": float(self.balance),
            "user_id": user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class UserAccount(db.Model):
    __tablename__ = "user_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="user_accounts")
    account = db.relationship("Account", back_populates="user_accounts")

    __table_args__ = (db.UniqueConstraint("user_id", "account_id"),)


class PhoneLink(db.Model):
    __tablename__ = "phone_links"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(
        db.String(30), db.ForeignKey("accounts.number"), unique=True, nullable=False
    )
    phone = db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    account = db.relationship("Account", back_populates="phone_links")

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SinpeSubscription(db.Model):
    __tablename__ = "sinpe_subscription"

    sinpe_number = db.Column(db.String(20), primary_key=True)
    sinpe_bank_code = db.Column(db.String(100), nullable=False)
    sinpe_client_name = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "sinpe_number": self.sinpe_number,
            "sinpe_bank_code": self.sinpe_bank_code,
            "sinpe_client_name": self.sinpe_client_name,
        }


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), unique=True, nullable=False)
    from_account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), nullable=True
    )  # Can be null for external
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="CRC")
    status = db.Column(db.String(20), default="pending")
    description = db.Column(db.String(255))
    sender_phone = db.Column(db.String(15))
    receiver_phone = db.Column(db.String(15))
    sender_info = db.Column(db.String(255))  # For external transfers
    receiver_info = db.Column(db.String(255))  # For external transfers
    external_bank_code = db.Column(db.String(10))  # Bank code for external transfers
    transaction_type = db.Column(
        db.String(30), default="internal"
    )  # internal, sinpe_incoming, sinpe_outgoing, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    from_account = db.relationship(
        "Account", foreign_keys=[from_account_id], back_populates="sent_transactions"
    )
    to_account = db.relationship(
        "Account", foreign_keys=[to_account_id], back_populates="received_transactions"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status,
            "description": self.description,
            "sender_phone": self.sender_phone,
            "receiver_phone": self.receiver_phone,
            "sender_info": self.sender_info,
            "receiver_info": self.receiver_info,
            "external_bank_code": self.external_bank_code,
            "transaction_type": self.transaction_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Currency(db.Model):
    __tablename__ = "currencies"

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(50))

    def to_dict(self):
        return {"code": self.code, "name": self.name}
