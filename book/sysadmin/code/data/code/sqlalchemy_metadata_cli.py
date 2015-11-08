#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

import os
import optparse

#Part 3:  mapped class
class Filesystem(object):

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def __repr__(self):
        return "[Filesystem('%s','%s')]" % (self.path, self.file)

class Controller(object):
    """Handles Options"""

    def run(self):
        "Runs commands"
        p = optparse.OptionParser(description="python version of locate",
                                    prog="pylocate",
                                    version="0.1")
        p.add_option("--database", "-d",
                    help="path to databse")
        p.set_defaults(database="sqlite:///:memory:"
        options, arguments = p.parse_args()
        if len(arguments) == 1:
            path = arguments[0]

            #Part 1:  create engine
            engine = create_engine(options.database, echo=False)

            #Part 2:  metadata
            metadata = MetaData()

            filesystem_table = Table('filesystem', metadata,
            Column('id', Integer, primary_key=True),
                Column('path', String(500)),
                Column('file', String(255)),
            )

            metadata.create_all(engine)

            #Part 4:  mapper function
            mapper(Filesystem,filesystem_table)

            #Part 5:  create session
            Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
            session = Session()

            #Part 6:  crawl file system and populate database with results
            for dirpath, dirnames, filenames in os.walk(path):
                for file in filenames:
                    fullpath = os.path.join(dirpath, file)
                    record = Filesystem(fullpath, file)
                    session.save(record)

            #Part 7:  commit to the database
            session.commit()

            #Part 8:  query
            for record in session.query(Filesystem):
                print "Database Record Number: %s, Path: %s , File: %s " \
                % (record.id,record.path, record.file)
        else:
            p.print_help()
def main():
    controller = Controller()
    start = controller.run()


if __name__ == "__main__":
    main()
