from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import HistoricalIncome, User
from dependencies.dependency import get_db
from config.logging_config import setup_logger  

logger = setup_logger(__name__)

class HistoricalMigrator:
    
    def migrate(self, db: Session, data: dict, user: User) -> Optional[HistoricalIncome]:
        create_at = datetime.fromtimestamp(data['createAt'] / 1000).date()
        last_update_date = datetime.fromtimestamp(data['fechaUltimaModificacion'] / 1000).date()

        historical: HistoricalIncome = HistoricalIncome(
            mongo_id=data['id'],
            total_amount_income=data['montoTotalIngreso'],
            total_amount_exit=data['montoTotalEgreso'],
            total_amount_dollar_income=data['montoTotalIngresoDolar'],
            total_amount_dollar_exit=data['montoTotalEgresoDolar'],
            total_amount_dollar_oficial=data['montoTotalDolarOficial'],
            total_amount_dollar_free=data['montoTotalDolarLibre'],
            total_income_items=data['itemsTotalIngreso'],
            total_exit_items=data['itemsTotalEgreso'],
            create_at=create_at,
            last_update_date=last_update_date,
            user_id=user.id,
            user=user
        )
        
        try:
            db.add(historical)
            db.commit()
            db.refresh(historical)
            return historical
        except Exception as e:
            db.rollback()
            logger.error(f"Error occurred: {e}")
            return None
            
historical_migrator = HistoricalMigrator()