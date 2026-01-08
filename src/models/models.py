from datetime import date
from sqlalchemy import Date, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from src.config.database import Base
from config.database import Base
from config.settings import settings

class User(Base):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mongo_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False, default=settings.COMMON_PASSWORD)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    migrado: Mapped[bool] = mapped_column(default=True, nullable=True)
    
    
    def __str__(self) -> str:
        return (f"User(id={self.id}, mongo_id='{self.mongo_id}', username='{self.username}', "
                f"password={self.password}, email='{self.email}', first_name='{self.first_name}', "
                f"last_name={self.last_name}, migrado={self.migrado})")
    
    
class Role(Base):
    
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    
class UserRole(Base):
    
    __tablename__ = "users_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship("User")
    role: Mapped["Role"] = relationship("Role")
    
    
class Income(Base):
    
    __tablename__ = "incomes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mongo_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    migrado: Mapped[bool] = mapped_column(default=True, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    create_at: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User")
    
    
class HistoricalIncome(Base):
    
    __tablename__ = "historical_incomes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mongo_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    migrado: Mapped[bool] = mapped_column(default=True, nullable=True)
    total_amount_income: Mapped[float] = mapped_column(nullable=False)
    total_amount_exit: Mapped[float] = mapped_column(nullable=False)
    total_amount_dollar_income: Mapped[float] = mapped_column(nullable=False)
    total_amount_dollar_exit: Mapped[float] = mapped_column(nullable=False)
    total_amount_dollar_oficial: Mapped[float] = mapped_column(nullable=False)
    total_amount_dollar_free: Mapped[float] = mapped_column(nullable=False)
    total_income_items: Mapped[int] = mapped_column(Integer, nullable=False)
    total_exit_items: Mapped[int] = mapped_column(Integer, nullable=False)
    create_at: Mapped[date] = mapped_column(Date, nullable=False)
    last_update_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User")
    
    def __str__(self) -> str:
        return (f"HistoricalIncome(id={self.id}, mongo_id='{self.mongo_id}', migrado={self.migrado}, "
                f"total_amount_income={self.total_amount_income}, total_amount_exit={self.total_amount_exit}, "
                f"total_amount_dollar_income={self.total_amount_dollar_income}, "
                f"total_amount_dollar_exit={self.total_amount_dollar_exit}, "
                f"total_amount_dollar_oficial={self.total_amount_dollar_oficial}, "
                f"total_amount_dollar_free={self.total_amount_dollar_free}, "
                f"total_income_items={self.total_income_items}, "
                f"total_exit_items={self.total_exit_items}, "
                f"create_at={self.create_at}, "
                f"last_update_date={self.last_update_date}, "
                f"user_id={self.user_id}, "
                f"user={self.user})")
    

class DollarOp(Base):
    
    __tablename__ = "dollar_ops"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mongo_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    migrado: Mapped[bool] = mapped_column(default=True, nullable=True)
    dollar_value_peso: Mapped[float] = mapped_column(nullable=False)
    dollar_op: Mapped[float] = mapped_column(nullable=False)
    total_pesos: Mapped[float] = mapped_column(nullable=False)
    dollar_acum: Mapped[float] = mapped_column(nullable=False)
    observations: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    create_at: Mapped[date] = mapped_column(Date, nullable=False)   
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User")