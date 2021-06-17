# locust-stress-testing
Send requests parsed from apache access log

## Prepare logs

The file that will be used as the source of the requests is a text file with one route per line. It can be parsed from apache `access.log` file using `awk` in the following way:

```
cat access.log | awk '{pring $9}' > request_source.txt
```
The actual stress testing will randomly choose a lines from the above file.
