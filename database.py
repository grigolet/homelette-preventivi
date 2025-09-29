#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DraftDatabase:
    """Database manager for preventivi drafts with offline support"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Try to use data directory if in Docker, otherwise use current directory
            data_dir = "/app/data" if os.path.exists("/app/data") else os.path.dirname(__file__)
            db_path = os.path.join(data_dir, "preventivi_drafts.db")
        
        self.db_path = db_path
        self.offline_queue = []  # Queue for offline operations
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS drafts (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        data TEXT NOT NULL,  -- JSON string
                        status TEXT DEFAULT 'draft',
                        client_name TEXT,
                        event_date TEXT,
                        num_people INTEGER,
                        total_cost REAL
                    )
                """)
                
                # Create index for better performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_drafts_updated 
                    ON drafts(updated_at DESC)
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def _generate_draft_name(self, data: Dict[str, Any]) -> str:
        """Generate automatic draft name based on date and client"""
        today = datetime.now().strftime("%d/%m/%Y")
        client = data.get('event_data', {}).get('riferimento', 'Cliente')
        
        # Clean client name
        client = client.strip()[:20] if client else 'Cliente'
        
        return f"{client} - {today}"
    
    def save_draft(self, data: Dict[str, Any], draft_id: Optional[str] = None, name: Optional[str] = None) -> str:
        """Save draft with auto-generated or custom name"""
        try:
            current_time = datetime.now().isoformat()
            
            if not draft_id:
                draft_id = str(uuid.uuid4())
            
            if not name:
                name = self._generate_draft_name(data)
            
            # Extract searchable fields from data
            event_data = data.get('event_data', {})
            client_name = event_data.get('riferimento', '')
            event_date = event_data.get('data_evento', '')
            num_people = event_data.get('numero_persone', 0)
            total_cost = self._calculate_total_cost(data)
            
            # Convert date if it's a date object
            if hasattr(event_date, 'isoformat'):
                event_date = event_date.isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO drafts 
                    (id, name, created_at, updated_at, data, status, 
                     client_name, event_date, num_people, total_cost)
                    VALUES (?, ?, 
                           COALESCE((SELECT created_at FROM drafts WHERE id = ?), ?),
                           ?, ?, ?, ?, ?, ?, ?)
                """, (
                    draft_id, name, draft_id, current_time, current_time,
                    json.dumps(data, default=str), 'draft',
                    client_name, event_date, num_people, total_cost
                ))
                conn.commit()
            
            logger.info(f"Draft saved successfully: {draft_id}")
            return draft_id
            
        except Exception as e:
            logger.error(f"Failed to save draft: {e}")
            # Add to offline queue if database operation fails
            self.offline_queue.append({
                'operation': 'save',
                'data': data,
                'draft_id': draft_id,
                'name': name,
                'timestamp': current_time
            })
            raise
    
    def load_draft(self, draft_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific draft by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT data FROM drafts WHERE id = ?", 
                    (draft_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return json.loads(row[0])
                return None
                
        except Exception as e:
            logger.error(f"Failed to load draft {draft_id}: {e}")
            return None
    
    def list_drafts(self) -> List[Dict[str, Any]]:
        """List all drafts with metadata"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, name, created_at, updated_at, status,
                           client_name, event_date, num_people, total_cost
                    FROM drafts 
                    ORDER BY updated_at DESC
                """)
                
                drafts = []
                for row in cursor.fetchall():
                    drafts.append({
                        'id': row[0],
                        'name': row[1],
                        'created_at': row[2],
                        'updated_at': row[3],
                        'status': row[4],
                        'client_name': row[5] or '',
                        'event_date': row[6] or '',
                        'num_people': row[7] or 0,
                        'total_cost': row[8] or 0
                    })
                
                return drafts
                
        except Exception as e:
            logger.error(f"Failed to list drafts: {e}")
            return []
    
    def delete_draft(self, draft_id: str) -> bool:
        """Delete a specific draft"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM drafts WHERE id = ?", 
                    (draft_id,)
                )
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Draft deleted successfully: {draft_id}")
                
                return success
                
        except Exception as e:
            logger.error(f"Failed to delete draft {draft_id}: {e}")
            return False
    
    def duplicate_draft(self, draft_id: str, new_name: Optional[str] = None) -> Optional[str]:
        """Duplicate an existing draft"""
        try:
            data = self.load_draft(draft_id)
            if not data:
                return None
            
            # Generate new name if not provided
            if not new_name:
                original_draft = self.get_draft_metadata(draft_id)
                if original_draft:
                    new_name = f"Copia di {original_draft['name']}"
                else:
                    new_name = f"Copia - {datetime.now().strftime('%d/%m/%Y')}"
            
            # Save as new draft
            new_id = self.save_draft(data, name=new_name)
            return new_id
            
        except Exception as e:
            logger.error(f"Failed to duplicate draft {draft_id}: {e}")
            return None
    
    def get_draft_metadata(self, draft_id: str) -> Optional[Dict[str, Any]]:
        """Get draft metadata without loading full data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, name, created_at, updated_at, status,
                           client_name, event_date, num_people, total_cost
                    FROM drafts WHERE id = ?
                """, (draft_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'created_at': row[2],
                        'updated_at': row[3],
                        'status': row[4],
                        'client_name': row[5] or '',
                        'event_date': row[6] or '',
                        'num_people': row[7] or 0,
                        'total_cost': row[8] or 0
                    }
                return None
                
        except Exception as e:
            logger.error(f"Failed to get metadata for draft {draft_id}: {e}")
            return None
    
    def update_draft_name(self, draft_id: str, new_name: str) -> bool:
        """Update draft name"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    UPDATE drafts 
                    SET name = ?, updated_at = ? 
                    WHERE id = ?
                """, (new_name, datetime.now().isoformat(), draft_id))
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Draft name updated: {draft_id}")
                
                return success
                
        except Exception as e:
            logger.error(f"Failed to update draft name {draft_id}: {e}")
            return False
    
    def mark_draft_completed(self, draft_id: str) -> bool:
        """Mark a draft as completed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    UPDATE drafts 
                    SET status = 'completed', updated_at = ? 
                    WHERE id = ?
                """, (datetime.now().isoformat(), draft_id))
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Draft {draft_id} marked as completed")
                
                return success
                
        except Exception as e:
            logger.error(f"Failed to mark draft as completed {draft_id}: {e}")
            return False
    
    def mark_draft_as_draft(self, draft_id: str) -> bool:
        """Mark a completed preventivo back to draft status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    UPDATE drafts 
                    SET status = 'draft', updated_at = ? 
                    WHERE id = ?
                """, (datetime.now().isoformat(), draft_id))
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Draft {draft_id} marked as draft")
                
                return success
                
        except Exception as e:
            logger.error(f"Failed to mark draft as draft {draft_id}: {e}")
            return False
    
    def process_offline_queue(self):
        """Process queued operations from offline mode"""
        if not self.offline_queue:
            return
        
        logger.info(f"Processing {len(self.offline_queue)} offline operations")
        
        processed = []
        for operation in self.offline_queue[:]:  # Copy to avoid modification during iteration
            try:
                if operation['operation'] == 'save':
                    self.save_draft(
                        operation['data'], 
                        operation['draft_id'], 
                        operation['name']
                    )
                processed.append(operation)
                
            except Exception as e:
                logger.warning(f"Failed to process offline operation: {e}")
                # Keep in queue for retry
                continue
        
        # Remove processed operations
        for op in processed:
            self.offline_queue.remove(op)
        
        if processed:
            logger.info(f"Processed {len(processed)} offline operations")
    
    def _calculate_total_cost(self, data: Dict[str, Any]) -> float:
        """Calculate total cost from quote data"""
        try:
            prezzo_persona = data.get('prezzo_persona', 0)
            numero_persone = data.get('numero_persone', 0)
            costo_cameriere = data.get('costo_cameriere', 0)
            
            return (prezzo_persona * numero_persone) + costo_cameriere
        except Exception:
            return 0.0
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM drafts")
                total_drafts = cursor.fetchone()[0]
                
                cursor = conn.execute(
                    "SELECT COUNT(*) FROM drafts WHERE status = 'draft'"
                )
                draft_count = cursor.fetchone()[0]
                
                cursor = conn.execute(
                    "SELECT COUNT(*) FROM drafts WHERE status = 'completed'"
                )
                completed_count = cursor.fetchone()[0]
                
                return {
                    'total_drafts': total_drafts,
                    'draft_count': draft_count,
                    'completed_count': completed_count,
                    'offline_queue_size': len(self.offline_queue)
                }
                
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {
                'total_drafts': 0,
                'draft_count': 0,
                'completed_count': 0,
                'offline_queue_size': len(self.offline_queue)
            }

# Global database instance
db = DraftDatabase()
