sudo -u postgres dropdb motorway-test 2>/dev/null || true
sudo -u postgres createdb motorway-test

echo 'motorway-test db created'
echo "Please change the 'postgres' user password in 'src/config/test.json' if different from 'admin'"