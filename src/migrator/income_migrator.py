from datetime import datetime
from sqlalchemy.orm import Session
from models.models import Income, User
from config.logging_config import setup_logger

logger = setup_logger(__name__) 

class IncomeMigrator:
    
    def migrate(self, db: Session, data: list[dict], user: User) -> bool:
        logger.info(f"Number of transactions in Argentina pesos ($) to migrate ---> {len(data)}")
        incomes = []
        for index, d in enumerate(data):
            logger.info(f"Processing transaction {index + 1} of {len(data)}")
            create_at = datetime.fromtimestamp(d['createAt'] / 1000).date()
            income: Income = Income(
                mongo_id=d['id'],
                description=d['descripcion'],
                amount=d['monto'],
                type=d['tipo'],
                create_at=create_at,
                user_id=user.id,
                user=user
            )
            incomes.append(income)

        try:
            db.add_all(incomes)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error occurred: {e}")
            return False
        return True
    
income_migrator = IncomeMigrator()