import storm.locals
import storm_model
import os

db = storm.locals.create_database('sqlite:///%s' % os.path.join(os.getcwd(), 'inventory.db'))

store = storm.locals.Store(db)

for o in store.find(storm_model.OperatingSystem, storm_model.OperatingSystem.name.like(u'Lin%')):
    print o.id, o.name, o.description
