-- variable changes in the wikipedia .sql file
SET GLOBAL time_zone='+00:00';
SET GLOBAL unique_checks=0;
SET GLOBAL foreign_key_checks=0;
SET GLOBAL sql_notes=0;
SET GLOBAL autocommit=0;
SET GLOBAL sql_mode='NO_AUTO_VALUE_ON_ZERO';
SET GLOBAL sql_log_bin=0;

-- sizes
SET @3gb=3221225472;
SET @2gb=2147483648;
SET @1gb=1073741824;
SET @512mb=536870912;
SET @256mb=268435356;
SET @128mb=268435356;

-- MyISAM settings
SET GLOBAL bulk_insert_buffer_size=@2gb;
SET GLOBAL key_buffer_size=@2gb;
SET GLOBAL sort_buffer_size=@2gb;
SET GLOBAL myisam_sort_buffer_size=@2gb;
SET GLOBAL max_allowed_packet=@512mb;
SET GLOBAL read_buffer_size=@512mb;
SET GLOBAL read_rnd_buffer_size=@512mb;
