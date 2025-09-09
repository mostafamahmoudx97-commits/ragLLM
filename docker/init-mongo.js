// init-mongo.js

db = db.getSiblingDB('admin');

db.createUser({
  user: 'admin',
  pwd: 'admin123',
  roles: [{ role: 'root', db: 'admin' }],
});