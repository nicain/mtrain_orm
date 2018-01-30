from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Training = declarative_base()

transitions_association_table = Table(
    'transitions_association',
    Training.metadata,
    Column('left_id', Integer, ForeignKey('regimens.id')),
    Column('right_id', Integer, ForeignKey('transitions.id'))
)

training_stages_association_table = Table(
    'training_stages_association',
    Training.metadata,
    Column('left_id', Integer, ForeignKey('regimens.id')),
    Column('right_id', Integer, ForeignKey('training_stages.id'))
)


class Transition(Training):

    __tablename__ = "transitions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    regimens = relationship(
        "Regimen",
        secondary=transitions_association_table,
        back_populates="transitions"
    )


class TrainingStage(Training):

    __tablename__ = "training_stages"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    regimens = relationship(
        "Regimen",
        secondary=training_stages_association_table,
        back_populates="training_stages"
    )


class Regimen(Training):

    __tablename__ = "regimens"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    training_stages = relationship(
        "TrainingStage",
        secondary=training_stages_association_table,
        back_populates="regimens"
    )
    transitions = relationship(
        "Transition",
        secondary=transitions_association_table,
        back_populates="regimens"
    )


class BehaviorTraining(Training):

    __tablename__ = "behavior_training"

    id = Column(Integer, autoincrement=True, primary_key=True)
    mouse_id = Column(Integer, nullable=False)
    regimen_id = Column(Integer, ForeignKey("regimens.id"))
    regimen = relationship("Regimen", uselist=False)


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    Training.metadata.create_all(engine)

    _SessionmakerFactory = sessionmaker(bind=engine)

    regimen = Regimen(
        name="my_first_regimen",
        training_stages=[
            TrainingStage(name="training_stage_0"),
            TrainingStage(name="training_stage_1"),
            TrainingStage(name="training_stage_2"),
            TrainingStage(name="training_stage_3")
        ],
        transitions=[
            Transition(name="transition_0"),
        ]
    )

    session = _SessionmakerFactory()

    session.add(regimen)
    session.commit()

    a_regimen = session.query(Regimen).one()

    print("regimen_name: ", a_regimen.name)
    print("transitions: ", [transition.name for transition in a_regimen.transitions])
    print("training_stages: ", [training_stage.name for training_stage in a_regimen.training_stages])

    regimen_id = session.query(Regimen).filter(Regimen.name=="my_first_regimen").one().id

    training = BehaviorTraining(mouse_id=999999, regimen_id=regimen_id)

    session.add(training)
    session.commit()

    a_training_thing = session.query(BehaviorTraining).one()

    print("my training thing:", a_training_thing)
    print("my training thing mouse_id: ", a_training_thing.mouse_id)
    print("my training thing regimen name: ", a_training_thing.regimen.name)
    print("my training thing transitions: ", [transition.name for transition in a_training_thing.regimen.transitions])
    print("my training thing training_stages: ", [training_stage.name for training_stage in a_training_thing.regimen.training_stages])
