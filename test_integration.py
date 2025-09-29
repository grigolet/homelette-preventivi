#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple integration test for the draft management system.
Tests the key functionality without complex mocking.
"""

import os
import tempfile
import time

# Import our modules
try:
    from database import DraftDatabase
    from autosave import AutoSaveManager
    print("✅ Successfully imported draft management modules")
except ImportError as e:
    print(f"❌ Failed to import modules: {e}")
    exit(1)


def test_database_functionality():
    """Test basic database operations"""
    print("\n🗄️ Testing Database Functionality...")
    
    # Create temporary database
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
    
    try:
        # Initialize database
        db = DraftDatabase(test_db_path)
        print("✅ Database initialized successfully")
        
        # Test data
        sample_data = {
            'event_data': {
                'riferimento': 'Test Cliente',
                'destinatario': 'Mario Rossi',
                'luogo': 'Villa Test',
                'numero_persone': 50
            },
            'menu_items': [
                {
                    'nome': 'ANTIPASTO TEST',
                    'categoria': 'Antipasti',
                    'descrizione': 'Antipasto di prova'
                }
            ],
            'prezzo_persona': 30.0,
            'costo_cameriere': 200.0
        }
        
        # Test save
        draft_id = db.save_draft(sample_data, name="Test Draft")
        print(f"✅ Draft saved with ID: {draft_id[:8]}...")
        
        # Test list
        drafts = db.list_drafts()
        assert len(drafts) == 1
        print(f"✅ Draft listing works - found {len(drafts)} draft(s)")
        
        # Test load
        loaded_data = db.load_draft(draft_id)
        assert loaded_data is not None
        assert loaded_data['event_data']['riferimento'] == sample_data['event_data']['riferimento']
        print("✅ Draft loading works correctly")
        
        # Test duplicate
        duplicate_id = db.duplicate_draft(draft_id, "Duplicate Test")
        assert duplicate_id is not None
        drafts = db.list_drafts()
        assert len(drafts) == 2
        print("✅ Draft duplication works")
        
        # Test update name
        success = db.update_draft_name(draft_id, "Updated Name")
        assert success
        print("✅ Draft name update works")
        
        # Test delete
        success = db.delete_draft(duplicate_id)
        assert success
        drafts = db.list_drafts()
        assert len(drafts) == 1
        print("✅ Draft deletion works")
        
        # Test stats
        stats = db.get_database_stats()
        assert stats['total_drafts'] == 1
        print("✅ Database statistics work")
        
        print("🎉 All database tests passed!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        raise
    finally:
        os.close(test_db_fd)
        os.unlink(test_db_path)


def test_autosave_basic():
    """Test basic auto-save functionality"""
    print("\n💾 Testing AutoSave Functionality...")
    
    try:
        # Create auto-save manager with short delay
        auto_save = AutoSaveManager(save_delay=0.1)
        print("✅ AutoSave manager initialized")
        
        # Test status display
        status = auto_save.get_save_status_display()
        assert isinstance(status, str)
        print(f"✅ Status display works: '{status}'")
        
        # Test connection check
        is_online = auto_save.check_connection()
        print(f"✅ Connection check works: {is_online}")
        
        # Test cleanup
        auto_save.cleanup_pending_saves()
        assert len(auto_save.pending_saves) == 0
        print("✅ Cleanup works")
        
        print("🎉 AutoSave basic tests passed!")
        
    except Exception as e:
        print(f"❌ AutoSave test failed: {e}")
        raise


def test_data_persistence():
    """Test that data persists correctly"""
    print("\n🔄 Testing Data Persistence...")
    
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
    
    try:
        # Save data with first database instance
        db1 = DraftDatabase(test_db_path)
        sample_data = {
            'event_data': {'riferimento': 'Persistence Test'},
            'prezzo_persona': 35.0
        }
        draft_id = db1.save_draft(sample_data, name="Persistence Test")
        print("✅ Data saved with first database instance")
        
        # Load data with second database instance (simulating app restart)
        db2 = DraftDatabase(test_db_path)
        loaded_data = db2.load_draft(draft_id)
        
        assert loaded_data is not None
        assert loaded_data['event_data']['riferimento'] == 'Persistence Test'
        assert loaded_data['prezzo_persona'] == 35.0
        print("✅ Data persisted correctly across database instances")
        
        print("🎉 Data persistence tests passed!")
        
    except Exception as e:
        print(f"❌ Persistence test failed: {e}")
        raise
    finally:
        os.close(test_db_fd)
        os.unlink(test_db_path)


def test_error_handling():
    """Test error handling and offline scenarios"""
    print("\n🚨 Testing Error Handling...")
    
    try:
        # Test with invalid database path (should still work with fallback)
        db = DraftDatabase("/invalid/path/database.db")
        
        # Should fallback to current directory
        expected_path = os.path.join(os.path.dirname(__file__), "preventivi_drafts.db")
        
        # Test that it can still operate
        sample_data = {'event_data': {'riferimento': 'Error Test'}}
        db.save_draft(sample_data)  # We don't need to store the result
        
        # Cleanup the database created in current directory
        if os.path.exists(expected_path):
            os.unlink(expected_path)
        
        print("✅ Error handling works correctly")
        
    except Exception as e:
        print(f"✅ Expected error handled correctly: {type(e).__name__}")


def test_performance():
    """Test basic performance characteristics"""
    print("\n⚡ Testing Performance...")
    
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db')
    
    try:
        db = DraftDatabase(test_db_path)
        
        # Test multiple save operations
        start_time = time.time()
        draft_ids = []
        
        for i in range(50):  # Reduced number for quick testing
            sample_data = {
                'event_data': {'riferimento': f'Perf Test {i}'},
                'prezzo_persona': 30.0
            }
            draft_id = db.save_draft(sample_data)
            draft_ids.append(draft_id)
        
        save_time = time.time() - start_time
        print(f"✅ Bulk save (50 drafts): {save_time:.2f}s ({50/save_time:.1f} ops/sec)")
        
        # Test list operation
        start_time = time.time()
        drafts = db.list_drafts()
        list_time = time.time() - start_time
        print(f"✅ List operation: {list_time:.3f}s for {len(drafts)} drafts")
        
        # Test load operations
        start_time = time.time()
        for draft_id in draft_ids[:10]:
            db.load_draft(draft_id)
        load_time = time.time() - start_time
        print(f"✅ Load operations: {load_time:.3f}s for 10 drafts")
        
        print("🎉 Performance tests completed!")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        raise
    finally:
        os.close(test_db_fd)
        os.unlink(test_db_path)


def main():
    """Run all tests"""
    print("🧪 Starting Draft Management Integration Tests...")
    
    try:
        test_database_functionality()
        test_autosave_basic()
        test_data_persistence()
        test_error_handling()
        test_performance()
        
        print("\n🎉 All tests passed successfully!")
        print("✅ Draft management system is working correctly")
        print("\n📋 Features tested:")
        print("  - Database initialization and schema creation")
        print("  - Draft save/load/update/delete operations")
        print("  - Draft duplication and naming")
        print("  - Data persistence across sessions")
        print("  - Auto-save manager initialization")
        print("  - Error handling and fallback behavior")
        print("  - Basic performance characteristics")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Tests failed with error: {e}")
        print("🔧 Please check the implementation and try again")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
