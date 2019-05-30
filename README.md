A query of, and basic analysis of, the LA city parking citation database. 

Calculations show that the city collected over $140M in parking citations over the course of 2018. To conduct your own analysis you
can update the python code within the main section of the program. The data is stored within a generator object, which can only be
iterated through once, so a new generator must be created for each calculation. This can be done quickly using the open_file_generator
function. Also, the start and end date can be edited to your desired timeframe, however please note that the database begins in 2016.

WARNING: The database contains over 9.5M entries as of May 2019. Loading the full file to your machine will take several minutes the same
time. The python script is written such that it only accesses rows within the timeframe.
