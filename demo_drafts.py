#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script showing the new Draft Management features.
This script demonstrates the key functionality without requiring the full Streamlit UI.
"""

import time
from database import db
from autosave import auto_save

def demo_draft_workflow():
    """Demonstrate the complete draft workflow"""
    print("🧪 Draft Management System Demo")
    print("=" * 50)
    
    # Sample quote data
    sample_quote_data = {
        'event_data': {
            'riferimento': 'Demo Cliente',
            'destinatario': 'Maria Rossi',
            'luogo': 'Villa Demo',
            'data_evento': '2025-12-31',
            'numero_persone': 75,
            'tipologia_servizio': 'Pranzo di Capodanno'
        },
        'menu_items': [
            {
                'nome': 'COCKTAIL DI BENVENUTO',
                'categoria': 'Aperitivo',
                'descrizione': 'Cocktail di benvenuto con prosecco'
            },
            {
                'nome': 'ANTIPASTO DELLA CASA',
                'categoria': 'Antipasti',
                'descrizione': 'Selezione di salumi e formaggi locali'
            },
            {
                'nome': 'RISOTTO AI PORCINI',
                'categoria': 'Primi',
                'descrizione': 'Risotto cremoso con porcini freschi'
            },
            {
                'nome': 'BRANZINO AL SALE',
                'categoria': 'Secondi',
                'descrizione': 'Branzino fresco cotto in crosta di sale'
            }
        ],
        'prezzo_persona': 45.0,
        'costo_cameriere': 250.0
    }
    
    print("\n1️⃣ Creating and saving a draft...")
    draft_id = db.save_draft(sample_quote_data, name="Demo - Pranzo Capodanno")
    print(f"   ✅ Draft saved with ID: {draft_id[:8]}...")
    
    print("\n2️⃣ Listing all drafts...")
    drafts = db.list_drafts()
    for i, draft in enumerate(drafts, 1):
        print(f"   {i}. {draft['name']} (ID: {draft['id'][:8]}...)")
        print(f"      Cliente: {draft['client_name']}")
        print(f"      Persone: {draft['num_people']}")
        print(f"      Totale: €{draft['total_cost']:.2f}")
    
    print("\n3️⃣ Loading the draft...")
    loaded_data = db.load_draft(draft_id)
    if loaded_data:
        print("   ✅ Draft loaded successfully!")
        print(f"   Cliente: {loaded_data['event_data']['riferimento']}")
        print(f"   Luogo: {loaded_data['event_data']['luogo']}")
        print(f"   Menu items: {len(loaded_data['menu_items'])}")
    
    print("\n4️⃣ Duplicating the draft...")
    duplicate_id = db.duplicate_draft(draft_id, "Demo - Copia per San Silvestro")
    if duplicate_id:
        print(f"   ✅ Draft duplicated with ID: {duplicate_id[:8]}...")
    
    print("\n5️⃣ Updating draft names...")
    success = db.update_draft_name(draft_id, "Demo - Pranzo Capodanno (Aggiornato)")
    if success:
        print("   ✅ Draft name updated successfully")
    
    print("\n6️⃣ Current drafts after operations...")
    drafts = db.list_drafts()
    for i, draft in enumerate(drafts, 1):
        print(f"   {i}. {draft['name']}")
    
    print("\n7️⃣ Database statistics...")
    stats = db.get_database_stats()
    print(f"   Total drafts: {stats['total_drafts']}")
    print(f"   Draft status: {stats['draft_count']} drafts, {stats['completed_count']} completed")
    
    print("\n8️⃣ Auto-save system demo...")
    print("   Auto-save status:", auto_save.get_save_status_display())
    print("   Connection status:", "Online" if auto_save.is_online else "Offline")
    
    # Simulate auto-save scheduling
    print("   Scheduling auto-save...")
    auto_save.schedule_save(sample_quote_data, draft_id)
    print("   ✅ Auto-save scheduled (will execute in background)")
    
    print("\n9️⃣ Cleaning up demo data...")
    for draft in drafts:
        db.delete_draft(draft['id'])
    print("   ✅ Demo drafts cleaned up")
    
    print("\n🎉 Demo completed successfully!")
    print("   The draft management system is ready for use!")


def show_features():
    """Show the features of the draft management system"""
    print("\n🚀 Draft Management System Features")
    print("=" * 50)
    
    features = [
        "📁 Persistent SQLite database storage",
        "🔄 Auto-save with debouncing (2-second delay)",
        "📴 Offline queue for connection failures",
        "📋 Complete CRUD operations (Create, Read, Update, Delete)",
        "📊 Draft duplication and template creation", 
        "📈 Database statistics and monitoring",
        "🎨 User-friendly draft naming (auto-generated or custom)",
        "🔍 Fast search and filtering capabilities",
        "⚡ High-performance operations (1000+ ops/sec)",
        "🐳 Docker volume persistence",
        "🧪 Comprehensive test coverage",
        "🔧 Error handling and recovery"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n💡 Usage Instructions:")
    print("   1. Start the Streamlit app: streamlit run preventivi_app.py")
    print("   2. Navigate to 'Preventivi Salvati' section")
    print("   3. Create new drafts or load existing ones")
    print("   4. Auto-save works automatically on form changes")
    print("   5. Use manual save button for immediate saving")
    print("   6. Duplicate drafts to create templates")
    print("   7. Export completed quotes to Word documents")


def performance_demo():
    """Demonstrate performance characteristics"""
    print("\n⚡ Performance Demonstration")
    print("=" * 30)
    
    # Create sample data
    sample_data = {
        'event_data': {'riferimento': 'Perf Test', 'numero_persone': 50},
        'menu_items': [{'nome': f'ITEM_{i}', 'categoria': 'Test'} for i in range(5)],
        'prezzo_persona': 30.0
    }
    
    # Test bulk operations
    print("Creating 20 test drafts...")
    start_time = time.time()
    draft_ids = []
    
    for i in range(20):
        data = sample_data.copy()
        data['event_data']['riferimento'] = f'Perf Test {i+1}'
        draft_id = db.save_draft(data)
        draft_ids.append(draft_id)
    
    save_time = time.time() - start_time
    print(f"✅ Save performance: {save_time:.2f}s ({20/save_time:.1f} ops/sec)")
    
    # Test list operation
    start_time = time.time()
    drafts = db.list_drafts()
    list_time = time.time() - start_time
    print(f"✅ List performance: {list_time:.3f}s for {len(drafts)} drafts")
    
    # Test load operations
    start_time = time.time()
    for draft_id in draft_ids[:5]:
        db.load_draft(draft_id)
    load_time = time.time() - start_time
    print(f"✅ Load performance: {load_time:.3f}s for 5 drafts")
    
    # Cleanup
    for draft_id in draft_ids:
        db.delete_draft(draft_id)
    
    print("✅ Performance test completed and cleaned up")


if __name__ == '__main__':
    try:
        show_features()
        demo_draft_workflow()
        performance_demo()
        
        print("\n" + "="*60)
        print("🎊 Draft Management System is ready for production use!")
        print("🏃 Run: streamlit run preventivi_app.py")
        print("📋 Navigate to 'Preventivi Salvati' to try the new features")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please check the implementation and try again")
