import yaml
import logging
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


'''
Additional table: regimens TODO replace regiments with regimen

records are name, transitions, training_stages


'''


logger = logging.getLogger(__name__)

BehavioralStageGraph = declarative_base()

class Transition(BehavioralStageGraph):

    """Regimens Table. Stores all regimen-related information.

    Attributes
    ----------
    id : column, string, non-null, unique, primary key
        index of the entry
    name : column, string, non-null, unique
        name of the regimen
    transitions_path : column, string, non-null
        absolute path to the transitions file
    training_stages_path : column, string, non-null
        absolute path to the training stages file
    """

    __tablename__ = "transitions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    trigger = Column(String, nullable=False, unique=False)
    source = Column(Integer, ForeignKey("training_stages.id"), nullable=False, unique=False)
    dest = Column(Integer, ForeignKey("training_stages.id"), nullable=False, unique=False)
    conditions = Column(JSON, nullable=False)  # i would use varchar but i have no idea what our paths will eventually look like...


class TrainingStage(BehavioralStageGraph):

    """Stages Table. Stores the possible stages:

    Attributes
    ----------
    id : column, string, non-null, unique, primary key
        index of the entry
    name : column, string
        stage of the mouse
    """

    __tablename__ = "training_stages"

    id = Column(Integer, autoincrement=True, primary_key=True)
    training_stage = Column(String, nullable=False, unique=True)
    regimen = Column(String, nullable=False)
    script = Column(JSON, nullable=False)
    parameters = Column(JSON, nullable=False)

class BehavorialTraining(BehavioralStageGraph):
    
    """Stages Table. Stores the possible stages:

    Attributes
    ----------
    id : column, string, non-null, unique, primary key
        index of the entry
    name : column, string
        stage of the mouse
    """

    __tablename__ = "behavioral_training"

    id = Column(Integer, autoincrement=True, primary_key=True)
    mouse_id = Column(Integer, nullable=False, unique=False)
    training_stage = Column(Integer, ForeignKey("training_stages.id"), nullable=False)
    regimen = Column(String, nullable=False, unique=False)
    input_date = Column(DateTime, nullable=False, unique=False)

