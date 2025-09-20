#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/grigolet/cernbox/personal/code/homelette-preventivi')

def test_word_document():
    """Test the Word document generation with sample data"""
    
    # Import the function from the main app
    from preventivi_app import create_word_document
    
    # Sample data for testing
    test_data = {
        'riferimento': 'Test Cliente',
        'destinatario': 'Mario Rossi',
        'luogo': 'Villa Test',
        'data_ora': 'Sabato 15 Giugno 2024 ore 19,30',
        'tipologia_servizio': 'COCKTAIL di benvenuto e apericena',
        'numero_persone': 50,
        'tipologia_buffet': 'Buffet e servizio',
        'bicchieri': 'Calici da vino in materiali ecocompatibili usa e getta',
        'posate': 'Acciaio leggero',
        'stoviglie': 'Ceramica e materiali ecocompatibili usa e getta',
        'acqua': 'Esclusa / da definire',
        'vini': 'Esclusi / da definire',
        'servizio': 'Incluso',
        'prezzo_persona': 28.0,
        'costo_cameriere': 200.0,
        'note': 'Evento di prova per testare la formattazione del documento.',
        'menu_items': [
            {
                'nome': 'COCKTAIL DI BENVENUTO',
                'categoria': 'Aperitivo',
                'descrizione': 'Cocktail di benvenuto per gli ospiti',
                'prezzo': 5.0
            },
            {
                'nome': 'PROSCIUTTO DI PARMA E MELONE SU PANE AI CEREALI',
                'categoria': 'Antipasti',
                'descrizione': 'Prosciutto di Parma e melone serviti su pane ai cereali',
                'prezzo': 12.0
            }
        ]
    }
    
    try:
        print("Generando documento di test...")
        doc = create_word_document(test_data)
        
        # Salva il documento di test
        filename = '/home/grigolet/cernbox/personal/code/homelette-preventivi/test_preventivo.docx'
        doc.save(filename)
        
        print(f"✅ Documento di test generato con successo: {filename}")
        print("Il documento include:")
        print("- Logo Homelette (se disponibile)")
        print("- Subtitle 'Primum manducare, deinde filosofare' in blu cobalto")
        print("- Linea decorativa orizzontale")
        print("- Font size migliorati per elementi in grassetto")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nella generazione del documento: {e}")
        return False

if __name__ == "__main__":
    test_word_document()