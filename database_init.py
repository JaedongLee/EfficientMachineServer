from sqlalchemy import MetaData, create_engine

from definitions import ROOT_DIR

engine = create_engine(f'sqlite:///{ROOT_DIR}/resource/database/EfficientMachine.db',
                       connect_args={'check_same_thread': False})
meta = MetaData(bind=engine)
MetaData.reflect(meta)
