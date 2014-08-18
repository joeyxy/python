<?php
    # set this to your client machine or proxy,
    # comment it out if you don't want protection
    $proxy_host = '';
    $proxy_port = 0;
    if(array_key_exists('req',$_POST)) {
            $req = $_POST['req'];
    } else {
        #print("unknown request");
        exit;
    }

	$nlnl = strpos($req, "\r\n\r\n");
	if (!$nlnl) $nlnl = strpos($req, "\n\n");
	if (!$nlnl) { exit; }
	$headers = substr($req, 0, $nlnl);
	$headers = preg_replace('/^Keep-Alive:.*?(\n|$)/ims', '', $headers, 1);
	$headers = preg_replace('/^(Proxy-)?Connection:.*?(\n|$)/ims', '', $headers, 1);
	$headers .= "\r\n". (!empty($proxy_host) ? 'Proxy-' : '') .'Connection: close';
	$req = $headers . substr($req, $nlnl);

    if (empty($proxy_host)) {
        $nl = strpos($req, "\n");
        $headl = substr($req, 0, $nl);
        if(!preg_match('/(\w+)\s+(\S+)(.*)/', $headl, $matches)) {
            exit;
        }
        $url = parse_url($matches[2]);
        $host = $url["host"];
        $port = $url["port"] ? $url["port"] : 80;
        $req = $matches[1] ." ".
               ($url["path"] ? $url["path"] : '/') .
               ($url["query"] ? "?". $url["query"] : '') .
               $matches[3] . substr($req, $nl);
    } else {
        $host = $proxy_host;
        $port = $proxy_port;
    }

    $fp = fsockopen ($host, $port, $errno, $errstr, 30);
    if (!$fp) {
        print("fsockopen failed: $errstr ($errno)");
        print "HTTP/1.0 500 $errstr ($errno)\r\n";
        print "Content-Type: text/html\r\n\r\n";
        print "<html><body><b>error</b></body></html>\n";
        exit;
    }

    #socket_set_blocking($fp, 0);
    #socket_set_timeout($fp, 5, 0);

    fwrite($fp, $req);
    $headers_processed = 0;
    $reponse = '';
    while (!feof($fp)) {
        $r = fread($fp, 2048);
        if ($strip_header && !$headers_processed) {
            $response .= $r;
            $nlnl = strpos($response, "\r\n\r\n"); $add = 4;
            if (!$nlnl) { $nlnl = strpos($response, "\n\n"); $add = 2; }
            if (!$nlnl) continue;
            if ($set_content_type) {
                $headers = substr($response, 0, $nlnl);
                if (preg_match_all('/^(Content-.*?)(\r?\n|$)/ims', $headers, $matches)) {
                    for ($i = 0; $i < count($matches[0]); ++$i) {
                        $ct = $matches[1][$i];
                        debug("content-*: $ct");
                        header($ct);
                    }
                }
            }
            print substr($response, $nlnl + $add);
            $headers_processed = 1;
        } else
            print $r;
    }
    fclose ($fp);

?>
