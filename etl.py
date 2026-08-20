import pandas as pd
import sqlite3

conn = sqlite3.connect('ecommerce.bd.db')

tabelas = {
    'olist_customers_dataset.csv': 'customers',
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_products_dataset.csv': 'products',
    'olist_sellers_dataset.csv': 'sellers',
    'olist_order_payments_dataset.csv': 'order_payments',
    'olist_order_reviews_dataset.csv': 'order_reviews',
    'olist_geolocation_dataset.csv': 'geolocation',
    'product_category_name_translation.csv': 'product_category_name_translation'
}

for arquivo_csv, nome_tabela in tabelas.items():
    # Verifica se a tabela já tem dados
    contagem_atual = conn.execute(f"SELECT COUNT(*) FROM {nome_tabela}").fetchone()[0]

    if contagem_atual > 0:
        print(f"{nome_tabela}: já tem {contagem_atual} linhas, pulando.")
        continue  # pula pra próxima tabela do loop, sem inserir de novo

    caminho = f'archive/{arquivo_csv}'
    df = pd.read_csv(caminho)

    # order_reviews tem review_id duplicado no CSV original, removi para evitar bugs
    if nome_tabela == 'order_reviews':
        linhas_antes = len(df)
        df = df.drop_duplicates(subset='review_id', keep='first')
        linhas_depois = len(df)
        print(f"  → Removidas {linhas_antes - linhas_depois} linhas duplicadas de review_id")

    df.to_sql(nome_tabela, conn, if_exists='append', index=False)

    resultado = conn.execute(f"SELECT COUNT(*) FROM {nome_tabela}").fetchone()
    print(f"{nome_tabela}: {resultado[0]} linhas importadas")

conn.commit()
conn.close()
print("Processo concluído!")