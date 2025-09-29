#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple draft management module (auto-save functionality removed)
This module now only provides basic utilities for manual draft operations.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)

def get_current_draft_info():
    """Get information about the current draft"""
    if 'current_draft_id' in st.session_state and st.session_state.current_draft_id:
        return {
            'id': st.session_state.current_draft_id,
            'short_id': st.session_state.current_draft_id[:8] + '...'
        }
    return None

def clear_current_draft():
    """Clear the current draft session"""
    if 'current_draft_id' in st.session_state:
        st.session_state.current_draft_id = None
    
    # Also clear the session data if needed
    if hasattr(st.session_state, 'quote_data'):
        st.session_state.quote_data = {}
    if hasattr(st.session_state, 'menu_items'):
        st.session_state.menu_items = []
    
    logger.info("Draft session cleared")

def is_draft_session_active():
    """Check if there is an active draft session"""
    return (st.session_state.get('current_draft_id') is not None and 
            (st.session_state.get('quote_data') or st.session_state.get('menu_items')))

# Legacy compatibility - these functions are no longer used but kept to avoid import errors
class AutoSaveManager:
    """Legacy class kept for compatibility (functionality removed)"""
    
    def __init__(self, save_delay: float = 2.0):
        logger.warning("AutoSaveManager is deprecated and no longer functional")
    
    def get_save_status_display(self):
        return "💾 Salvataggio manuale"

# Legacy instances for compatibility
auto_save = AutoSaveManager()

def trigger_auto_save(*args, **kwargs):
    """Legacy function - no longer performs auto-save"""
    pass

def create_auto_save_input(*args, **kwargs):
    """Legacy function - no longer creates auto-save inputs"""
    # Fall back to regular streamlit input
    return st.text_input(*args, **kwargs)
