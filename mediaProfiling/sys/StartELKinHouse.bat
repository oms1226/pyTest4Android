@ECHO OFF
echo STARTTIME:%date:~0,4%%date:~5,2%%date:~8,2%.%time:~0,2%%time:~3,2%%time:~6,2%
start "elasticsearch" cmd /C "D:\_workspace\Elasticsearch\elasticsearch-6.1.3\elasticsearch-6.1.3\bin\elasticsearch.bat"
echo "start:elasticsearch"
ping 127.0.0.1 -n 30 > nul
start "kibana" cmd /C "D:\_workspace\Elasticsearch\kibana-6.1.3-windows-x86_64\kibana-6.1.3-windows-x86_64\bin\kibana.bat"
echo "start:kibana"
ping 127.0.0.1 -n 5 > nul
start "logstash" cmd /C "D:\_workspace\Elasticsearch\logstash-6.1.3\logstash-6.1.3\bin\logstash.bat --config.reload.automatic -f %CD%\logstash.config"
echo "start:logstash"
ping 127.0.0.1 -n 30 > nul
rem cmd /K "D:\_workspace\Elasticsearch\filebeat-6.1.3-windows-x86_64\filebeat-6.1.3-windows-x86_64\filebeat -e -c %CD%\filebeat.yml"
start "filebeat" cmd /K "D:\_workspace\Elasticsearch\filebeat-6.1.3-windows-x86_64\filebeat-6.1.3-windows-x86_64\filebeat -e -c %CD%\filebeat.yml"
echo "start:filebeat"
echo END__TIME:%date:~0,4%%date:~5,2%%date:~8,2%.%time:~0,2%%time:~3,2%%time:~6,2%
