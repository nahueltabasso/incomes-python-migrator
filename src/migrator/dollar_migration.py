from datetime import datetime
from sqlalchemy.orm import Session
from models.models import User, DollarOp
from config.logging_config import setup_logger  

logger = setup_logger(__name__)

class DollarMigrator:
    
    def migrate(self, db: Session, data: list[dict], user: User) -> bool:
        logger.info(f"Number of transactions in US Dollars (U$D) to migrate ---> {len(data)}")
        dollar_ops = []

        for index, d in enumerate(data):
            logger.info(f"Processing dollar transaction {index + 1} of {len(data)}")
            create_at = datetime.fromtimestamp(d['createAt'] / 1000).date()
            dollar_op: DollarOp = DollarOp(
                mongo_id=d['id'],
                dollar_value_peso=d['valorDolarPeso'],
                dollar_op=d['cantidadDolarCompra'],
                total_pesos=d['totalPesos'],
                dollar_acum=d['dolarAcumulado'],
                observations=d['observacion'] if d['observacion'] else '',
                type=d['tipoOperacion'],
                create_at=create_at,
                user_id=user.id,
                user=user
            ) # type: ignore

            dollar_ops.append(dollar_op)
            
        try:
            db.add_all(dollar_ops)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error occurred: {e}")
            return False
        return True
    
dollar_migrator = DollarMigrator()