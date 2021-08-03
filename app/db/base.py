# Import all the models, so the Base has them befor being
# imported by Alembic
from app.db.base_class import Base
from app.models.tweet import Tweet
from app.models.user import User
