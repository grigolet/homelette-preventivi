#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import time
import threading
from typing import Dict, Any
import logging
from database import db

logger = logging.getLogger(__name__)

class AutoSaveManager:
    """Manages auto-save functionality with debouncing and offline support"""
    
    def __init__(self, save_delay: float = 2.0):
        self.save_delay = save_delay
        self.pending_saves = {}  # draft_id -> timer
        self.is_online = True
        self.last_connection_check = 0
        self.connection_check_interval = 30  # seconds
        
        # Initialize session state for drafts
        if 'current_draft_id' not in st.session_state:
            st.session_state.current_draft_id = None
        if 'auto_save_status' not in st.session_state:
            st.session_state.auto_save_status = "💾 Pronto"
        if 'last_save_time' not in st.session_state:
            st.session_state.last_save_time = None
    
    def check_connection(self) -> bool:
        """Check if we can access the database (simulate network check)"""
        try:
            # Try a simple database operation
            db.get_database_stats()
            if not self.is_online:
                logger.info("Connection restored, processing offline queue")
                self.is_online = True
                # Process any queued operations
                db.process_offline_queue()
            return True
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            self.is_online = False
            return False
    
    def _should_check_connection(self) -> bool:
        """Check if we should test the connection"""
        current_time = time.time()
        if current_time - self.last_connection_check > self.connection_check_interval:
            self.last_connection_check = current_time
            return True
        return False
    
    def schedule_save(self, data: Dict[str, Any], draft_id: str = None, draft_name: str = None):
        """Schedule an auto-save with debouncing"""
        # Check connection periodically
        if self._should_check_connection():
            self.check_connection()
        
        # Use current draft ID if none provided
        if not draft_id:
            draft_id = st.session_state.get('current_draft_id')
        
        # Cancel any pending save for this draft
        if draft_id in self.pending_saves:
            self.pending_saves[draft_id].cancel()
        
        # Update status
        st.session_state.auto_save_status = "⏳ Salvataggio..."
        
        # Schedule new save
        timer = threading.Timer(self.save_delay, self._execute_save, 
                               args=(data, draft_id, draft_name))
        timer.start()
        self.pending_saves[draft_id] = timer
        
        logger.debug(f"Scheduled save for draft {draft_id} in {self.save_delay} seconds")
    
    def _execute_save(self, data: Dict[str, Any], draft_id: str = None, draft_name: str = None):
        """Execute the actual save operation"""
        try:
            # Compile all current session data
            complete_data = self._compile_session_data(data)
            
            # Perform save
            saved_id = db.save_draft(complete_data, draft_id, draft_name)
            
            # Update session state
            st.session_state.current_draft_id = saved_id
            st.session_state.last_save_time = time.time()
            
            if self.is_online:
                st.session_state.auto_save_status = "✅ Salvato"
            else:
                st.session_state.auto_save_status = "📴 In coda (offline)"
            
            # Clean up timer reference
            if draft_id in self.pending_saves:
                del self.pending_saves[draft_id]
            
            logger.info(f"Auto-save completed for draft {saved_id}")
            
        except Exception as e:
            logger.error(f"Auto-save failed: {e}")
            st.session_state.auto_save_status = "❌ Errore salvataggio"
            
            # Clean up timer reference
            if draft_id in self.pending_saves:
                del self.pending_saves[draft_id]
    
    def _compile_session_data(self, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile all session data into a complete draft"""
        complete_data = {
            'event_data': st.session_state.get('quote_data', {}),
            'menu_items': st.session_state.get('menu_items', []),
            'prezzo_persona': st.session_state.quote_data.get('prezzo_persona', 0),
            'costo_cameriere': st.session_state.quote_data.get('costo_cameriere', 0),
            'numero_persone': st.session_state.quote_data.get('numero_persone', 0)
        }
        
        # Merge additional data
        if additional_data:
            complete_data.update(additional_data)
        
        return complete_data
    
    def force_save(self, data: Dict[str, Any] = None, draft_id: str = None, draft_name: str = None) -> str:
        """Force immediate save without debouncing"""
        try:
            # Cancel any pending save
            if draft_id and draft_id in self.pending_saves:
                self.pending_saves[draft_id].cancel()
                del self.pending_saves[draft_id]
            
            # Compile data
            complete_data = self._compile_session_data(data)
            
            # Save immediately
            saved_id = db.save_draft(complete_data, draft_id, draft_name)
            
            # Update session state
            st.session_state.current_draft_id = saved_id
            st.session_state.last_save_time = time.time()
            
            if self.is_online:
                st.session_state.auto_save_status = "✅ Salvato manualmente"
            else:
                st.session_state.auto_save_status = "📴 In coda (offline)"
            
            logger.info(f"Force save completed for draft {saved_id}")
            return saved_id
            
        except Exception as e:
            logger.error(f"Force save failed: {e}")
            st.session_state.auto_save_status = "❌ Errore salvataggio"
            raise
    
    def load_draft(self, draft_id: str) -> bool:
        """Load a draft into current session"""
        try:
            draft_data = db.load_draft(draft_id)
            if not draft_data:
                return False
            
            # Load data into session state
            st.session_state.quote_data = draft_data.get('event_data', {})
            st.session_state.menu_items = draft_data.get('menu_items', [])
            st.session_state.current_draft_id = draft_id
            
            # Update quote data with pricing info
            if 'prezzo_persona' in draft_data:
                st.session_state.quote_data['prezzo_persona'] = draft_data['prezzo_persona']
            if 'costo_cameriere' in draft_data:
                st.session_state.quote_data['costo_cameriere'] = draft_data['costo_cameriere']
            if 'numero_persone' in draft_data:
                st.session_state.quote_data['numero_persone'] = draft_data['numero_persone']
            
            st.session_state.auto_save_status = "📂 Caricato"
            logger.info(f"Draft {draft_id} loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load draft {draft_id}: {e}")
            st.session_state.auto_save_status = "❌ Errore caricamento"
            return False
    
    def create_new_draft(self) -> str:
        """Create a new empty draft"""
        # Clear current session
        st.session_state.quote_data = {}
        st.session_state.menu_items = []
        st.session_state.current_draft_id = None
        st.session_state.auto_save_status = "✨ Nuovo preventivo"
        
        logger.info("New draft session created")
        return "new"
    
    def get_save_status_display(self) -> str:
        """Get formatted save status for display"""
        status = st.session_state.get('auto_save_status', '💾 Pronto')
        
        # Add timestamp if available
        last_save = st.session_state.get('last_save_time')
        if last_save and 'Salvato' in status:
            time_diff = int(time.time() - last_save)
            if time_diff < 60:
                status += f" ({time_diff}s fa)"
            elif time_diff < 3600:
                status += f" ({time_diff//60}m fa)"
            else:
                status += f" ({time_diff//3600}h fa)"
        
        # Add offline indicator
        if not self.is_online:
            status += " 🔸"
        
        return status
    
    def cleanup_pending_saves(self):
        """Cancel all pending saves"""
        for timer in self.pending_saves.values():
            timer.cancel()
        self.pending_saves.clear()

# Global auto-save manager instance
auto_save = AutoSaveManager()

def trigger_auto_save(field_name: str = None, delay_override: float = None):
    """Convenience function to trigger auto-save from UI components"""
    if delay_override:
        auto_save.save_delay = delay_override
    
    logger.debug(f"Auto-save triggered by field: {field_name}")
    auto_save.schedule_save({
        'trigger_field': field_name,
        'timestamp': time.time()
    })

def create_auto_save_input(label: str, key: str, input_type: str = "text", **kwargs):
    """Create an input widget with auto-save functionality"""
    
    # Map input types to Streamlit widgets
    widget_map = {
        'text': st.text_input,
        'number': st.number_input,
        'date': st.date_input,
        'time': st.time_input,
        'selectbox': st.selectbox,
        'textarea': st.text_area
    }
    
    widget_func = widget_map.get(input_type, st.text_input)
    
    # Add on_change callback for auto-save
    def on_change():
        trigger_auto_save(field_name=key)
    
    # Create widget with auto-save
    return widget_func(
        label,
        key=key,
        on_change=on_change,
        **kwargs
    )
