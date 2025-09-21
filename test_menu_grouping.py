#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script per verificare il raggruppamento del menu per categoria
"""

def test_menu_grouping():
    print("🧪 Test raggruppamento menu per categoria...")
    
    # Sample menu items con diverse categorie
    sample_menu_items = [
        {'nome': 'COCKTAIL DI BENVENUTO', 'categoria': 'Aperitivo', 'descrizione': 'Cocktail per gli ospiti'},
        {'nome': 'PROSCIUTTO E MELONE', 'categoria': 'Antipasti', 'descrizione': 'Antipasto classico'},
        {'nome': 'PASTA AL POMODORO', 'categoria': 'Primi', 'descrizione': 'Primo piatto tradizionale'},
        {'nome': 'TIRAMISU', 'categoria': 'Dolci', 'descrizione': 'Dolce della casa'},
        {'nome': 'FOCACCIA', 'categoria': 'Pane', 'descrizione': 'Pane fresco'},
        {'nome': 'VITELLO TONNATO', 'categoria': 'Secondi', 'descrizione': 'Secondo piatto'},
    ]
    
    # Test grouping logic
    menu_by_category = {}
    for item in sample_menu_items:
        categoria = item.get('categoria', 'Altro')
        if categoria not in menu_by_category:
            menu_by_category[categoria] = []
        menu_by_category[categoria].append(item)
    
    print(f"✅ Raggruppati {len(sample_menu_items)} elementi in {len(menu_by_category)} categorie")
    
    # Ordine categorie
    category_order = [
        'Aperitivo', 'Antipasti', 'Primi', 'Secondi', 
        'Contorni', 'Pasticceria Salata', 'Pane', 
        'Dolci', 'Frutta', 'Bevande', 'Altro'
    ]
    
    print("\n📋 Anteprima raggruppamento:")
    for categoria in category_order:
        if categoria in menu_by_category and menu_by_category[categoria]:
            print(f"\n🔵 {categoria.upper()}")
            for item in menu_by_category[categoria]:
                print(f"   • {item['nome']}")
    
    print("\n🎉 Test completato!")
    return True

if __name__ == "__main__":
    test_menu_grouping()
