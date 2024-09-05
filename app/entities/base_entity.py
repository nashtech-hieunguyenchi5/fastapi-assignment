from sqlalchemy import Column, Time

class BaseEntity:
    
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
