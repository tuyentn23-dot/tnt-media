"""Database Manager - SQLite with SQLAlchemy ORM"""
import os
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import JSON
from datetime import datetime
import json

Base = declarative_base()


class MediaRecord(Base):
    """Generic media record table"""
    __tablename__ = 'media_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_type = Column(String(50), nullable=False)  # channel, content, ip, campaign
    record_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)  # Full JSON data
    status = Column(String(50), default='active')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "record_type": self.record_type,
            "record_id": self.record_id,
            "name": self.name,
            "data": self.data,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class DatabaseManager:
    """Manages database connections and CRUD operations"""
    
    def __init__(self, db_path: str = "tnt_media.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def create_record(self, record_type: str, record_id: str, name: str, data: Dict[str, Any]) -> MediaRecord:
        """Create a new record"""
        session = self.get_session()
        try:
            record = MediaRecord(
                record_type=record_type,
                record_id=record_id,
                name=name,
                data=data
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        finally:
            session.close()
    
    def get_record(self, record_id: str) -> Optional[MediaRecord]:
        """Get record by ID"""
        session = self.get_session()
        try:
            return session.query(MediaRecord).filter_by(record_id=record_id).first()
        finally:
            session.close()
    
    def get_records_by_type(self, record_type: str) -> List[MediaRecord]:
        """Get all records of a specific type"""
        session = self.get_session()
        try:
            return session.query(MediaRecord).filter_by(record_type=record_type).all()
        finally:
            session.close()
    
    def update_record(self, record_id: str, data: Dict[str, Any], name: Optional[str] = None) -> bool:
        """Update an existing record"""
        session = self.get_session()
        try:
            record = session.query(MediaRecord).filter_by(record_id=record_id).first()
            if record:
                record.data = data
                if name:
                    record.name = name
                record.updated_at = datetime.now()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def delete_record(self, record_id: str) -> bool:
        """Delete a record"""
        session = self.get_session()
        try:
            record = session.query(MediaRecord).filter_by(record_id=record_id).first()
            if record:
                session.delete(record)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_all_records(self) -> List[MediaRecord]:
        """Get all records"""
        session = self.get_session()
        try:
            return session.query(MediaRecord).all()
        finally:
            session.close()
    
    def search_records(self, keyword: str) -> List[MediaRecord]:
        """Search records by name or data"""
        session = self.get_session()
        try:
            return session.query(MediaRecord).filter(
                MediaRecord.name.ilike(f'%{keyword}%')
            ).all()
        finally:
            session.close()
    
    def backup_database(self, backup_path: str = "backups") -> str:
        """Backup database to file"""
        os.makedirs(backup_path, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_path, f'tnt_media_backup_{timestamp}.db')
        
        import shutil
        shutil.copy2(self.db_path, backup_file)
        return backup_file
    
    def export_to_json(self, output_path: str = "backups") -> str:
        """Export all records to JSON"""
        os.makedirs(output_path, exist_ok=True)
        records = self.get_all_records()
        data = {
            "exported_at": datetime.now().isoformat(),
            "count": len(records),
            "records": [r.to_dict() for r in records]
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_path, f'tnt_media_export_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_file
