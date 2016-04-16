<?php
    if(isset($_GET['fn']))
    {
        $filename = $_GET['fn'];
        $path = './upfile/' . $filename;

        Header("Content-type: application/octet-stream");
        Header("Content-Length: " . filesize($path));
        Header("Content-Disposition: attachment; filename=$filename");
        Header("Cache-Control: no-cache");

        if(is_file($path))
        {
            $fp = fopen($path, "r");
            if(!fpassthru($fp))
            fclose($fp);
        }
    }
?>
