-- variable changes in the wikipedia .sql file
SET GLOBAL time_zone='+00:00';
SET GLOBAL unique_checks=0;
SET GLOBAL foreign_key_checks=0;
SET GLOBAL sql_notes=0;
SET GLOBAL sql_mode='NO_AUTO_VALUE_ON_ZERO';
SET GLOBAL sql_log_bin=0;

-- import speedup variables
SET @big_size=2147483648; -- 2 GB
SET @small_size=536870912; -- 0.5 GB
SET GLOBAL bulk_insert_buffer_size=@small_size;
SET GLOBAL key_buffer_size=@small_size;
SET GLOBAL sort_buffer_size=@small_size;
SET GLOBAL myisam_sort_buffer_size=@small_size;
SET GLOBAL max_allowed_packet=@small_size;
SET GLOBAL read_buffer_size=@small_size;
SET GLOBAL read_rnd_buffer_size=@small_size;
