# PowerShell script to create DB and user
$env:PGPASSWORD = "password"

$db_name = "products"
$db_user = "admin"
$password = "products"
$pg_host = "127.0.0.1"
$pg_port = "5432"

$psql = "C:\Program Files\PostgreSQL\17\bin\psql.exe"

& $psql -U postgres -h $pg_host -p $pg_port -c "CREATE DATABASE $db_name;"
& $psql -U postgres -h $pg_host -p $pg_port -c "CREATE USER $db_user WITH PASSWORD '$password';"
& $psql -U postgres -h $pg_host -p $pg_port -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"
& $psql -U postgres -h $pg_host -p $pg_port -d $db_name -c "GRANT USAGE, CREATE ON SCHEMA public TO $db_user;"
& $psql -U postgres -h $pg_host -p $pg_port -d $db_name -c "ALTER SCHEMA public OWNER TO $db_user;"

Write-Host " Database $db_name created with user $db_user and password $password"
