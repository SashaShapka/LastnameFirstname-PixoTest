# drop_db.ps1

$db_name = "products"
$db_user = "admin"
$password = "products"

$env:PGPASSWORD = "password"

$psql = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
$pg_host = "127.0.0.1"
$pg_port = "5432"

& $psql -U postgres -h $pg_host -p $pg_port -c "DROP DATABASE IF EXISTS $db_name;"
& $psql -U postgres -h $pg_host -p $pg_port -c "REASSIGN OWNED BY $db_user TO postgres;"
& $psql -U postgres -h $pg_host -p $pg_port -c "DROP OWNED BY $db_user;"
& $psql -U postgres -h $pg_host -p $pg_port -c "DROP ROLE IF EXISTS $db_user;"

Write-Host " Database '$db_name' and user '$db_user' dropped"
