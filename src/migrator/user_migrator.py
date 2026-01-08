from typing import Optional, Sequence, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from dependencies.dependency import get_db
from models.models import Role, User, UserRole
from config.logging_config import setup_logger
from config.settings import settings
import bcrypt

logger = setup_logger(__name__)

class UserMigrator():
    
    def migrate(self, db: Session, data: dict) -> User | None:
        # Check if the user exists
        existing_user = self._exists_user_by_email(db=db, email=data['email'])
        if existing_user:
            logger.info(f"User with email {data['email']} already exists. Skipping migration.")
            return None
    
        user: User = User(
            mongo_id=data['id'],
            username=data['username'],
            password=bcrypt.hashpw(settings.COMMON_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            email=data['email'],
            first_name=data['nombre'],
            last_name=data['apellido']
        )
        
        try:
            logger.info(f"User before save in database -> {user.__str__()}")
            db.add(user)
            db.flush()
            
            roles_names: Sequence[str] = data.get('roles', [])
            roles = self._get_roles_by_names(db=db, names=roles_names)
            
            user_roles: list[UserRole] = []
            for role in roles:
                user_roles.append(UserRole(user_id=user.id, role_id=role.id, user=user, role=role))
                
            db.add_all(user_roles)
            db.commit()
            db.refresh(user)
            logger.info(f"User after save in database -> {user.__str__()}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error migrating user {data['email']}: {e}")
            return None
                
    def _exists_user_by_email(self, db: Session, email: str) -> Optional[User]:
        db = next(get_db())
        return db.query(User).filter(User.email == email).first()
    
    def _get_roles_by_names(self, db: Session, names: Sequence[str]) -> List[Role]: # type: ignore
        if not names:
            return []
        stmt = select(Role).where(Role.role.in_(names))
        return list(db.scalars(stmt))
    
user_migrator = UserMigrator()