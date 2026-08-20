# 📊 Análise de E-commerce Brasileiro — SQL + Python

Criei um projeto de modelagem de banco de dados e análise exploratória usando o dataset público da Olist, tendo dados reais de uma empresa. O banco foi modelado do zero (sem importar um schema pronto), via ETL em Python e explorado com queries SQL para responder perguntas reais de negócio.

## 🗂️ Sobre os dados

Contém informações reais e anonimizadas de ~100 mil pedidos feitos entre 2016 e 2018 em múltiplos marketplaces no Brasil, tendo as tabelas clientes, pedidos, itens, produtos, vendedores, pagamentos, avaliações e geolocalização.

Durante o processo de ETL, tive problemas com o dataset original que vale a pena citar:

- **814 registros duplicados** de `review_id` na tabela de avaliações, tratados com remoção de duplicidade na hora de rodar o código. Sem isso, a `PRIMARY KEY` da tabela `order_reviews` não estava sendo válida.
- **Erro de nomes em colunas** do dataset original (ex: `product_name_lenght`, com erro de digitação mantido de propósito para evitar outros problemas com os dados brutos, enquanto `product_length_cm` segue a grafia correta, sendo corrigida em outra parte do código).
- A tabela `geolocation` não possui uma chave primária natural, já que contém mais de uma coordenada que pode ter o mesmo prefixo de CEP, portanto não teve necessidade de ter PK, funcionando como tabela de apoio.

## 🧱 Modelagem — Diagrama ER

O schema foi feito em 9 tabelas, com chaves primárias, simples e compostas, e chaves estrangeiras definidas manualmente.

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : realiza
    ORDERS ||--o{ ORDER_ITEMS : contem
    ORDERS ||--o{ ORDER_PAYMENTS : pago_por
    ORDERS ||--o{ ORDER_REVIEWS : avaliado_por
    PRODUCTS ||--o{ ORDER_ITEMS : vendido_como
    SELLERS ||--o{ ORDER_ITEMS : vendido_por
    PRODUCTS }o--|| PRODUCT_CATEGORY_NAME_TRANSLATION : categorizado_por

    CUSTOMERS {
        text customer_id PK
        text customer_unique_id
        integer customer_zip_code_prefix
        text customer_city
        text customer_state
    }
    ORDERS {
        text order_id PK
        text customer_id FK
        text order_status
        text order_purchase_timestamp
    }
    ORDER_ITEMS {
        text order_id PK_FK
        integer order_item_id PK
        text product_id FK
        text seller_id FK
        real price
        real freight_value
    }
    PRODUCTS {
        text product_id PK
        text product_category_name
        integer product_weight_g
    }
    SELLERS {
        text seller_id PK
        text seller_city
        text seller_state
    }
    ORDER_PAYMENTS {
        text order_id PK_FK
        integer payment_sequential PK
        text payment_type
        real payment_value
    }
    ORDER_REVIEWS {
        text review_id PK
        text order_id FK
        integer review_score
    }
    PRODUCT_CATEGORY_NAME_TRANSLATION {
        text product_category_name PK
        text product_category_name_english
    }
```

> A tabela `geolocation` não aparece no diagrama por não possuir chave primária nem chave estrangeira, ela se relaciona com `customers` e `sellers` apenas pelo valor de `zip_code_prefix`, sem vínculo declarado no schema original da Olist.

## 🛠️ Tecnologias

- **SQLite** — banco de dados escolhido
- **Python / Pandas / SQLite3** — ETL dos dados brutos para o banco
- **SQL** — modelagem (DDL) e análise (JOINs, agregações, GROUP BY)
- **DB Browser for SQLite** — interface visual escolhida

## ▶️ Como rodar o projeto

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/NOME-DO-REPO.git
cd NOME-DO-REPO

# 2. Instale as dependências
pip install pandas

# 3. Baixe o dataset da Olist no Kaggle e extraia na pasta /archive
# https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

# 4. Crie o schema do banco
# Abra o arquivo schema.sql no DB Browser for SQLite (ou sqlite3 via terminal) e execute

# 5. Rode o ETL para popular as tabelas
python etl.py
```

## 📈 Queries analíticas e insights

### 1. Faturamento total por estado

Query com `JOIN` entre `orders`, `customers` e `order_items`, agregada por estado.

| Estado | Faturamento (R$) |
|---|---|
| SP | 5.202.955,05 |
| RJ | 1.824.092,67 |
| MG | 1.585.308,03 |
| RS | 750.304,02 |
| PR | 683.083,76 |

**Insight**: São Paulo concentra sozinho quase 3x o faturamento do segundo colocado Rio de Janeiro, refletindo diretamente com a densidade populacional e econômica do estado.

### 2. Faturamento e volume de pedidos por cidade

| Cidade | Faturamento (R$) | Pedidos |
|---|---|---|
| São Paulo | 1.914.924,54 | 15.402 |
| Rio de Janeiro | 992.538,86 | 6.834 |
| Belo Horizonte | 355.611,13 | 2.750 |
| Brasília | 301.920,25 | 2.116 |
| Curitiba | 211.738,06 | 1.510 |

### 3. Faturamento e quantidade vendida por categoria de produto

| Categoria | Qtd. vendida | Faturamento (R$) |
|---|---|---|
| beleza_saude | 9.670 | 1.258.681,34 |
| relogios_presentes | 5.991 | 1.205.005,68 |
| cama_mesa_banho | 11.115 | 1.036.988,68 |
| esporte_lazer | 8.641 | 988.048,97 |

**Insight**: a categoria com maior faturamento (`beleza_saude`) não é a que mais vende em quantidade — a categoria `cama_mesa_banho` vende 15% mais itens, mas fatura menos. Isso indica um ticket médio por item significativamente maior em beleza/saúde e relógios/presentes.

## 🤖 Sobre o uso de IA neste projeto

Parte deste projeto foi desenvolvida com apoio de um assistente de IA (Claude), videoaulas para entender alguns comandos e estudo individual, usado principalmente para:

- Revisar o código e ajudar na hora sobre bugs que não entendia como resolver
- Maior entendimento sobre chaves primárias, chaves compostas, normalização
- Auxílio pontual na escrita do tratamento de duplicatas no script de ETL

A decisão de modelagem de cada tabela, a escrita da maior parte do SQL e Python, o encontro de erros e a interpretação dos resultados foram feitas por mim, com o assistente atuando como um copilot para ajuda e estudo — meu primeiro projeto de banco de dados relacional construído do zero.

## 📌 Próximos passos

- [ ] Visualizações gráficas dos resultados (matplotlib/seaborn)
- [ ] Query de segmentação de clientes (RFM)
- [ ] Publicação dos insights no LinkedIn
