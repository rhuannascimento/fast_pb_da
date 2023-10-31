O objetivo principal deste código é preencher a tabela de fato "fato_vendas" com informações de vendas consolidadas, obtidas a partir das tabelas de dimensão. A tabela fato permite que a empresa responda a uma variedade de perguntas de negócios e analise os dados de vendas de diferentes perspectivas.

## Estrutura das Tabelas

- As tabelas de dimensão (dimensao_pedido, dimensao_cliente, dimensao_produto, dimensao_pagamento e dimensao_order_item) armazenam informações detalhadas sobre pedidos, clientes, produtos, pagamentos e itens de pedido.
- A tabela de fato "fato_vendas" contém dados agregados de vendas, incluindo o valor total da venda, a data do pedido e a classificação do cliente.

## Principais Perguntas Resolvidas

- O Data Warehouse permite responder a várias perguntas de negócios, como:
  1. Qual é o valor total das vendas por categoria de produto?
  2. Quais são os produtos mais vendidos em uma determinada região (cidade ou estado)?
  3. Qual é a média de pagamentos parcelados por mês?
  4. Como o score de avaliação dos clientes afeta as vendas?

A aplicação desse código é essencial para a empresa, pois permite obter insights valiosos que podem ajudar a otimizar as operações, identificar oportunidades de crescimento e melhorar a experiência do cliente.

## Configuração do Docker

Para criar um ambiente isolado e eficiente para o desenvolvimento e execução deste projeto, utilizamos o Docker para a implantação de contêineres. A configuração do Docker foi essencial para garantir a consistência e a portabilidade do ambiente de desenvolvimento.

Dentro do arquivo `docker-compose.yml`, definimos os seguintes serviços:

- **Postgres:** Configuramos um contêiner PostgreSQL que é usado para armazenar as tabelas do Data Warehouse. Especificamos o nome do usuário, senha e o nome do banco de dados que serão usados. Mapeamos a porta 5432 do contêiner para a porta 5432 do host local para que seja possível acessar o banco de dados a partir da máquina hospedeira. Também configuramos um volume para persistir os dados do PostgreSQL, garantindo que os dados não sejam perdidos quando o contêiner for reiniciado.

- **MongoDB:** Configuramos um contêiner MongoDB que é usado para armazenar dados específicos do MongoDB, como as informações de revisão (review) de pedidos. Mapeamos a porta 27017 do contêiner para a porta 27017 do host local. Além disso, usamos um volume para inicializar o banco de dados MongoDB com um script JavaScript personalizado que está localizado no arquivo `init.js`.

- **Python App:** Configuramos um contêiner para executar o código Python responsável pela extração, transformação e carregamento (ETL) dos dados nas tabelas do Data Warehouse. Este contêiner depende dos contêineres PostgreSQL e MongoDB para garantir que os serviços estejam disponíveis quando o código for executado. Mapeamos volumes para compartilhar o código-fonte e os dados de entrada com o contêiner.

A configuração de rede denominada "minha-rede" permite que os contêineres se comuniquem entre si e com o host local.
