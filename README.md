# Flask-SQLAlchemy + PostgreSQLでWebサービスを作成する

- [Flask-SQLAlchemy + PostgreSQLでWebサービスを作成する](#flask-sqlalchemy--postgresql%e3%81%a7web%e3%82%b5%e3%83%bc%e3%83%93%e3%82%b9%e3%82%92%e4%bd%9c%e6%88%90%e3%81%99%e3%82%8b)
  - [はじめに](#%e3%81%af%e3%81%98%e3%82%81%e3%81%ab)
    - [目的](#%e7%9b%ae%e7%9a%84)
    - [実行環境](#%e5%ae%9f%e8%a1%8c%e7%92%b0%e5%a2%83)
    - [ソースコード](#%e3%82%bd%e3%83%bc%e3%82%b9%e3%82%b3%e3%83%bc%e3%83%89)
    - [関連する記事](#%e9%96%a2%e9%80%a3%e3%81%99%e3%82%8b%e8%a8%98%e4%ba%8b)
  - [0. 開発環境の構成](#0-%e9%96%8b%e7%99%ba%e7%92%b0%e5%a2%83%e3%81%ae%e6%a7%8b%e6%88%90)
  - [1. Flask-SQLAlchemyの開発](#1-flask-sqlalchemy%e3%81%ae%e9%96%8b%e7%99%ba)
    - [パッケージのインストール](#%e3%83%91%e3%83%83%e3%82%b1%e3%83%bc%e3%82%b8%e3%81%ae%e3%82%a4%e3%83%b3%e3%82%b9%e3%83%88%e3%83%bc%e3%83%ab)
    - [SQLAlchemyの設定](#sqlalchemy%e3%81%ae%e8%a8%ad%e5%ae%9a)
    - [Modelの作成](#model%e3%81%ae%e4%bd%9c%e6%88%90)
  - [2. PostgreSQLの設定](#2-postgresql%e3%81%ae%e8%a8%ad%e5%ae%9a)
    - [サービスの確認](#%e3%82%b5%e3%83%bc%e3%83%93%e3%82%b9%e3%81%ae%e7%a2%ba%e8%aa%8d)
    - [サービスの開始/終了](#%e3%82%b5%e3%83%bc%e3%83%93%e3%82%b9%e3%81%ae%e9%96%8b%e5%a7%8b%e7%b5%82%e4%ba%86)
    - [データベースの確認](#%e3%83%87%e3%83%bc%e3%82%bf%e3%83%99%e3%83%bc%e3%82%b9%e3%81%ae%e7%a2%ba%e8%aa%8d)
    - [データベースの接続/切断](#%e3%83%87%e3%83%bc%e3%82%bf%e3%83%99%e3%83%bc%e3%82%b9%e3%81%ae%e6%8e%a5%e7%b6%9a%e5%88%87%e6%96%ad)
    - [ロール(ユーザ)の作成](#%e3%83%ad%e3%83%bc%e3%83%ab%e3%83%a6%e3%83%bc%e3%82%b6%e3%81%ae%e4%bd%9c%e6%88%90)
    - [データベースの作成](#%e3%83%87%e3%83%bc%e3%82%bf%e3%83%99%e3%83%bc%e3%82%b9%e3%81%ae%e4%bd%9c%e6%88%90)
    - [データベースのマイグレーション](#%e3%83%87%e3%83%bc%e3%82%bf%e3%83%99%e3%83%bc%e3%82%b9%e3%81%ae%e3%83%9e%e3%82%a4%e3%82%b0%e3%83%ac%e3%83%bc%e3%82%b7%e3%83%a7%e3%83%b3)

## はじめに

サンプルアプリ(Feedback)を用いてご紹介します。

`Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。`

### 目的

この記事を最後まで読むと、次のことができるようになります。

| No.  | 概要                   | キーワード                 |
| :--- | :--------------------- | :------------------------- |
| 1    | Flask-SQLAlchemyの開発 | Flask-SQLAlchemy, psycopg2 |
| 2    | PostgreSQLの設定       | psql, Flask-Migrate        |

### 実行環境

| 環境             | Ver.    |
| :--------------- | :------ |
| macOS Catalina   | 10.15.2 |
| Python           | 3.7.3   |
| Flask-Migrate    | 2.5.2   |
| Flask-SQLAlchemy | 2.4.1   |
| Flask            | 1.1.1   |
| psycopg2         | 2.8.4   |
| requests         | 2.22.0  |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/python-flask-postgresql.git)

### 関連する記事

- [FlaskでRESTful Webサービスを作成する](https://qiita.com/nsuhara/items/449835bc94f0fb3bbcbd)

## 0. 開発環境の構成

```tree.sh
/
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── feedback
│   │   ├── __init__.py
│   │   ├── common/
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── feedback.py
│   │   ├── static/
│   │   ├── templates/
│   │   └── views/
│   ├── run.py
│   └── tests/
└── instance
     ├── postgresql.py
     ├── sqlite3.py
     └── config.py
```

## 1. Flask-SQLAlchemyの開発

### パッケージのインストール

1. パッケージをインストールする。

    ```procedure.sh
    ~$ pip install Flask-Migrate
    ~$ pip install Flask-SQLAlchemy
    ~$ pip install Flask
    ~$ pip install psycopg2
    ```

2. `psycopg2`のインストールでエラーが出る場合は、環境変数を指定してコマンドを実行する(macOS + venv環境)。

    ```procedure.sh
    ~$ xcode-select --install
    ~$ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
    ```

### SQLAlchemyの設定

1. 開発環境のコンフィグを設定する。

    ```config.py
    """instance/config.py
    """

    from instance.postgresql import SQLALCHEMY_DATABASE_URI as DATABASE_URI

    DEBUG = True
    # SECRET_KEY is generated by os.urandom(24).
    SECRET_KEY = '\xf7\xf4\x9bb\xd7\xa8\xdb\xee\x9f\xe3\x98SR\xda\xb0@\xb7\x12\xa4uB\xda\xa3\x1b'
    STRIPE_API_KEY = ''

    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    ```

2. PostgreSQLを設定する。

    ```postgresql.py
    """instance/postgresql.py
    """

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
        'user': 'nsuhara',
        'password': 'nsuhara',
        'host': '127.0.0.1',
        'name': 'db.postgresql'
    })
    ```

3. SQLite3を設定する(おまけ)。

    ```sqlite3.py
    """instance/sqlite3.py
    """

    import os

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{host}/{name}'.format(**{
        'host': os.path.dirname(os.path.abspath(__file__)),
        'name': 'db.sqlite3'
    })
    ```

### Modelの作成

1. SQLAlchemyのインスタンスを生成する。

    ```__init__.py
    """app/feedback/models/__init__.py
    """

    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()


    def init():
        """init
        """
        db.create_all()
    ```

2. SQLAlchemyのクラス(`db.Model`)を継承してModelを作成する。

    ```feedback.py
    """app/feedback/models/feedback.py
    """

    from datetime import datetime

    from feedback.models import db


    class Feedback(db.Model):
        """Feedback
        """
        __tablename__ = 'feedback'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        service = db.Column(db.String(255), nullable=False)
        title = db.Column(db.String(255), nullable=False)
        detail = db.Column(db.String(255), nullable=False)
        created_date = db.Column(
            db.DateTime, nullable=False, default=datetime.utcnow)

        def __init__(self, service, title, detail):
            self.service = service
            self.title = title
            self.detail = detail

        def to_dict(self):
            """to_dict
            """
            return {
                'id': self.id,
                'service': self.service,
                'title': self.title,
                'detail': self.detail,
                'created_date': self.created_date
            }
    ```

## 2. PostgreSQLの設定

`Homebrew`の実行例となります。

### サービスの確認

1. サービスを確認する。

    ```procedure.sh
    ~$ brew services list
    ```

    ```example.sh
    Name       Status  User    Plist
    postgresql started nsuhara /Users/nsuhara/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
    ```

### サービスの開始/終了

1. サービスを開始する。

    ```procedure.sh
    ~$ brew services start postgresql
    ```

2. サービスを終了する。

    ```procedure.sh
    ~$ brew services stop postgresql
    ```

### データベースの確認

1. データベースを確認する。

    `デフォルトで3つのデータベースが作成される。また、Macのユーザ名がOwnerとして設定される。`

    ```procedure.sh
    ~$ psql -l
    ```

    ```result.sh
                                List of databases
        Name      |  Owner  | Encoding | Collate | Ctype |  Access privileges
    --------------+---------+----------+---------+-------+---------------------
    postgres      | nsuhara | UTF8     | C       | C     |
    template0     | nsuhara | UTF8     | C       | C     | =c/nsuhara         +
                  |         |          |         |       | nsuhara=CTc/nsuhara
    template1     | nsuhara | UTF8     | C       | C     | =c/nsuhara         +
                  |         |          |         |       | nsuhara=CTc/nsuhara
    ```

### データベースの接続/切断

1. データベースに接続する。

    ```procedure.sh
    ~$ psql -h "<host_name>" -p <port_number> -U "<role_name>" -d "<database_name>"
    ```

    ```example.sh
    ~$ psql -h "127.0.0.1" -p 5432 -U "nsuhara" -d "postgres"
    ```

2. データベースの接続を切断する。

    ```procedure.sh
    postgresql=# \q
    ```

### ロール(ユーザ)の作成

1. データベースに接続する。

2. ロール(ユーザ)を確認する。

    ```procedure.sh
    postgresql=# \du
    ```

    ```result.sh
                                    List of roles
    Role name |                         Attributes                         | Member of
    ----------+------------------------------------------------------------+-----------
    nsuhara   | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
    ```

3. ロール(ユーザ)を作成する。

    ```procedure.sh
    postgresql=# CREATE ROLE "<role_name>" LOGIN PASSWORD "password";
    ```

    ```example.sh
    postgresql=# CREATE ROLE "nsuhara" LOGIN PASSWORD "nsuhara";
    ```

4. ロール(ユーザ)を削除する。

    ```procedure.sh
    postgresql=# DROP ROLE "<role_name>";
    ```

    ```example.sh
    postgresql=# DROP ROLE "nsuhara";
    ```

### データベースの作成

1. データベースに接続する。

2. データベースを確認する。

    ```procedure.sh
    postgresql=# \l
    ```

    ```result.sh
                            List of databases
        Name      |  Owner  | Encoding | Collate | Ctype |  Access privileges
    --------------+---------+----------+---------+-------+---------------------
    db.postgresql | nsuhara | UTF8     | C       | C     |
    postgres      | nsuhara | UTF8     | C       | C     |
    template0     | nsuhara | UTF8     | C       | C     | =c/nsuhara         +
                  |         |          |         |       | nsuhara=CTc/nsuhara
    template1     | nsuhara | UTF8     | C       | C     | =c/nsuhara         +
                  |         |          |         |       | nsuhara=CTc/nsuhara
    ```

3. データベースを作成する。

    ```procedure.sh
    postgresql=# CREATE DATABASE "<database_name>" OWNER "<role_ name>";
    ```

    ```example.sh
    postgresql=# CREATE DATABASE "db.postgresql" OWNER "nsuhara";
    ```

4. データベースを削除する。

    ```procedure.sh
    postgresql=# DROP DATABASE "<database_name>";
    ```

    ```example.sh
    postgresql=# DROP DATABASE "db.postgresql";
    ```

### データベースのマイグレーション

1. Flaskの環境変数を設定する。

2. データベースをマイグレートする。

    ```procedure.sh
    ~$ flask db init
    ~$ flask db migrate
    ~$ flask db upgrade
    ```
