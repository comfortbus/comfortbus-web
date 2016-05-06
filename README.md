Comfort Bus
===========
Backend do Projeto de ESS.
Alunos:

* Douglas Vasconcelos

* Gabriel Vasconcelos

* Gilberto Sousa

* Marcus Vinicius Silva

Dependências
------------
Para o correto funcionamento, são necessários

* Banco de dados PostgreSQL configurado

* Python 2.7

* [PIP](https://pip.pypa.io/en/stable/)

* [virtualenv](https://virtualenv.pypa.io/en/latest/)

É aconselhado que esse código seja rodado em ambiente UNIX. Na Wiki do projeto o processo de montagem das dependências é explicado mais detalhadamente a questão do banco de dados e do virtualenv.

Configurando o ambiente (_.env_)
--------------------------------
Com todas as dependências devidamente instaladas e banco de dados configurado, você precisará ter um arquivo _.env_ contendo os campos presentes no [.env-example](.env-example) para que a aplicação possa ler configurações locais.

Por exemplo:

    DATABASE_URL="postgres://usuario:senha@localhost:5432/comfortbus"
Onde você colocaria seu usuário do postgres onde está escrito `usuario`, sua senha em `senha`, o endereço do banco (`localhost` para banco de dados local, `5432` sendo a porta padrão) e o nome do banco que você criou para a aplicação no lugar de `comfortbus`.

O intúito do _.env_ é manter um arquivo que não será versionado pelo git que centralize informações pertinentes ao ambiente (_env_ ironment) em que se roda o projeto.

Instalando as dependências
--------------------------
Para instalar as dependencias, basta rodar o comando

    make requirements
E através do PIP, todas as dependências serão instaladas.

Rodando o servidor
------------------
Antes de rodar o servidor, você precisa ativar um ambiente virtual (_virtualenv_) que estará associado ao projeto. Depois, você precisa sincronizar o banco de dados com as tabelas do projeto. Para isso, basta rodar o comando

    make dev db
Para rodar o servidor em seu ambiente, você pode utilizar o comando

    make dev runserver
Que rodará seu código em ambiente de desenvolvimento (Que tem auxílios como o setting `DEBUG = True`).

Para maior escalabilidade, você pode optar por rodar

    make dev gunicorn
Ou ainda

    make prod gunicorn
Que faria sua máquina rodar como o servidor de produção na heroku.

Uma vez que o servidor esteja rodando, basta acessar [este link](http://localhost:8000/):

`http://localhost:8000/`

Versão em Produção
------------------
O código contido na master desse repositório é o mesmo que está rodando na heroku.

Veja a [Versão em produção do Comfort Bus](https://comfortbus.herokuapp.com/)