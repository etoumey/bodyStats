<?php
    $username = ""; 
    $password = "";   
    $host = "localhost";
    $database="userData.db";

    $server = mysql_connect($host, $user, $password);
    $connection = mysql_select_db($database, $server);

    $myquery = "
    SELECT * FROM userData
    ";

    $query = mysql_query($myquery);

    if ( ! $query ) {
        echo mysql_error();
        die;
    }

    $data = array();

    for ($x = 0; $x < mysql_num_rows($query); $x++) {
        $data[] = mysql_fetch_assoc($query);
    }

    echo json_encode($data);     

    mysql_close($server);
?>