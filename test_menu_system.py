#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script per il nuovo sistema di menu persistente
"""

import sys
sys.path.append('/home/grigolet/cernbox/personal/code/homelette-preventivi')

# Import delle funzioni del menu
from preventivi_app import load_menu_items, save_menu_items, add_new_menu_item

def test_menu_functions():
    print("🧪 Test del sistema di menu persistente...")
    
    # Test 1: Caricamento menu predefiniti
    print("\n1️⃣ Test caricamento menu...")
    menu_items = load_menu_items()
    print(f"✅ Caricati {len(menu_items)} elementi del menu")
    
    # Mostra alcuni elementi
    print("\n📋 Primi 3 elementi del menu:")
    for i, (nome, dettagli) in enumerate(list(menu_items.items())[:3]):
        print(f"   • {nome} ({dettagli['categoria']})")
    
    # Test 2: Aggiunta di un nuovo elemento
    print("\n2️⃣ Test aggiunta nuovo elemento...")
    test_nome = "TEST PIATTO TEMPORANEO"
    test_categoria = "Test"
    test_descrizione = "Questo è un piatto di test che verrà rimosso"
    
    updated_menu = add_new_menu_item(test_nome, test_categoria, test_descrizione)
    
    if test_nome.upper() in updated_menu:
        print(f"✅ Elemento '{test_nome}' aggiunto con successo")
    else:
        print(f"❌ Errore nell'aggiunta dell'elemento '{test_nome}'")
    
    # Test 3: Verifica persistenza
    print("\n3️⃣ Test persistenza...")
    reloaded_menu = load_menu_items()
    
    if test_nome.upper() in reloaded_menu:
        print("✅ Il nuovo elemento è persistente")
        
        # Cleanup: rimuovi l'elemento di test
        del reloaded_menu[test_nome.upper()]
        save_menu_items(reloaded_menu)
        print("🧹 Elemento di test rimosso")
    else:
        print("❌ Problema con la persistenza")
    
    print("\n🎉 Test completati!")
    print(f"📊 Database menu contiene {len(reloaded_menu)} elementi")

if __name__ == "__main__":
    test_menu_functions()
