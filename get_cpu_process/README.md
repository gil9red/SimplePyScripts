# Get CPU Process

Functional utility and CLI tool that returns some basic process-related info to the user, using psutil.  


```sh
$ ./cpu --help

Simple CPU related script written by Zac the Wise utilising psutil

Basic usage: cpu "<process-name>"

Example: cpu "amethyst"
Returns 'running' or 'not running'


Advanced usage: cpu <option> <arguement>

     --get-pid "<process-name>"         returns the process id

     --run-time "<process-name>">       returns the process running-time
``` 
