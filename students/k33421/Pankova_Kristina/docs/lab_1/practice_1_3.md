# Практики 1-3 для лабораторной работы 1

# Практика 1

API-эндпойнты для профессий:

```python
@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)

    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}
```

# Практика 2

API и модели для умений воинов и их ассоциативной сущности:

```python
class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(
    default=None, foreign_key="skill.id", primary_key=True
    )
    warrior_id: Optional[int] = Field(
    default=None, foreign_key="warrior.id", primary_key=True
    )
    level: Optional[int] = None

class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink)


class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)


class SkillResponse(SQLModel):
    id: int
    name: str
    description: str

class WarriorResponse(SQLModel):
    id: int
    name: str
    level: int
    skills: List[SkillResponse]
```

API для умений война:

```python
@app.post("/skill")
def skills_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}

@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skills_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.exec(select(Skill).where(Skill.id == skill_id)).first()


@app.post("/skill_warrior_link")
def skill_warrior_link_create(link: SkillWarriorLink, session=Depends(get_session)):
    link = SkillWarriorLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": link}

@app.get("/skill_warrior_links")
def skill_warrior_links_list(session=Depends(get_session)) -> List[SkillWarriorLink]:
    return session.exec(select(SkillWarriorLink)).all()

@app.get("/skill_warrior_link/{skill_id}/{warrior_id}")
def skill_warrior_link_get(skill_id: int, warrior_id: int, session=Depends(get_session)) -> SkillWarriorLink:
    return session.exec(select(SkillWarriorLink).where((SkillWarriorLink.skill_id == skill_id) & (SkillWarriorLink.warrior_id == warrior_id))).first()
```

API для отображения война (войнов) вместе с их умениями:

```python
@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    warriors = session.exec(select(Warrior).options(joinedload(Warrior.skills))).unique().all()

    response_data = [
        WarriorResponse(
            id=warrior.id,
            name=warrior.name,
            level=warrior.level,
            skills=[
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    description=skill.description
                )
                for skill in warrior.skills
            ]
        )
        for warrior in warriors
    ]
    return JSONResponse(content=[item.dict() for item in response_data])



@app.get("/warriors/{warrior_id}", response_model=WarriorResponse)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> WarriorResponse:
    warrior = session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()
    skills = session.exec(select(Skill).join(SkillWarriorLink).where(SkillWarriorLink.warrior_id == warrior.id)).all()

    response_data = WarriorResponse(
        id=warrior.id,
        name=warrior.name,
        level=warrior.level,
        skills=[
            SkillResponse(
                id=skill.id,
                name=skill.name,
                description=skill.description
            )
            for skill in skills
        ]
    )

    return JSONResponse(content=response_data.dict())
```

# Практика 3

alembic.ini

```python
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to migrations/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:migrations/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = postgresql://postgres:1234@localhost:5432/finance_db


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```


env.py
```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys

from sqlmodel import SQLModel

sys.path.append("..")

from models import *

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

Сгенерированный файл миграции:
```python
"""skill added

Revision ID: 0911f66586a9
Revises: 
Create Date: 2024-03-26 15:19:52.202008

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0911f66586a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('skillwarriorlink', sa.Column('level', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('skillwarriorlink', 'level')
    # ### end Alembic commands ###
```

.env
```python
DB_ADMIN = postgresql://postgres:1234@localhost:5432/warriors_db
```

alembic.ini new url
```python
...
import os
sqlalchemy.url = os.environ.get('DB_ADMIN')
...
```

