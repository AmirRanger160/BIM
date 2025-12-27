from app.database import SessionLocal
from app.models.models import User

db = SessionLocal()
db.query(User).filter(User.username == 'admin').delete()
db.commit()
print("✓ Admin user deleted")
