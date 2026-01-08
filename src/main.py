from typing import Optional
from config.database import database_settings, Base, engine
from config.settings import settings
from config.logging_config import setup_logger
from models.models import User
from services.api_service import api_service
from migrator.user_migrator import user_migrator
from migrator.historical_migrator import historical_migrator
from migrator.income_migrator import income_migrator
from migrator.dollar_migration import dollar_migrator
from dependencies.dependency import get_db
import asyncio

logger = setup_logger(__name__)

Base.metadata.create_all(bind=engine)

logger.info("Starting application...")
logger.info(f"Database Host: {database_settings.MYSQL_HOST}")
logger.info(f"Database Port: {database_settings.MYSQL_PORT}")
logger.info(f"Database User: {database_settings.MYSQL_USER}")
logger.info(f"Database Password: {database_settings.MYSQL_PASSWORD}")
logger.info(f"Database Name: {database_settings.MYSQL_DATABASE}")

usernames = settings.USERNAMES.split(',')
passwords = settings.PASSWORD.split(',')

for username, password in zip(usernames, passwords):
    try:
        login_response: Optional[dict] = asyncio.run(api_service.login(username=username, password=password))
        if not login_response:
            raise Exception("Login failed")
        
        with next(get_db()) as db:        
           # INIT USER MIGRATION
            logger.info("Migrating user...")
            logger.info(f"Migrating user: {username}")
            user: Optional[User] = user_migrator.migrate(db=db, data=login_response) # type: ignore
            # END USER MIGRATION
            if user:
                logger.info("User migrated successfully.")
                # INIT HISTORICAL MIGRATION
                logger.info("Migrating historical data...")
                historical_response = asyncio.run(
                    api_service.get_historical_by_user(access_token=login_response['accessToken']) # type: ignore
                )
                historical_migrator.migrate(db=db, data=historical_response, user=user) # type: ignore
                logger.info("Historical data migrated successfully.")   
                # END HISTORICAL MIGRATION
                
                # INIT INCOME MIGRATION
                logger.info("Migrating incomes...")
                income_response = asyncio.run(
                    api_service.get_incomes_by_user(access_token=login_response['accessToken']) # type: ignore
                )

                status = income_migrator.migrate(db=db, data=income_response, user=user)
                if not status:
                    logger.error("Error during incomes migration.")
                    raise Exception("Ocurred an error during incomes migration")
                logger.info("Incomes migrated successfully.")
                # END INCOME MIGRATION
                
                # INIT DOLLAR MIGRATION
                logger.info("Migrating dollars transactions...")
                dollars_ops = asyncio.run(
                    api_service.get_dollars_transactions_by_user(access_token=login_response['accessToken']) # type: ignore
                )

                status = dollar_migrator.migrate(db=db, data=dollars_ops, user=user)
                if not status:
                    logger.error("Error during dollar ops migration.")
                    raise Exception("Ocurred an error during dollar ops migration")
                logger.info("Dollar transactions migrated successfully.")
                #END DOLLAR MIGRATION
    except Exception as e:
        logger.error(f"Error ----- {e}")

logger.info("Migration completed successfully.")