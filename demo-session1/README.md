## Usage Examples

### csv-to-database
___
> Flags to pass to command line:
>
>>-db : Whether to create database or not (bool)
>>    
>> -d : input data path (str)
>>    
>> -t : table name to create (str)
___
First create a database:

```python -m src/tools/upload_data.py -db True```

Then you can create as many tables as you like within the database and insert data from CSV files. As an example, insert sales data to database:

```python src/tools/upload_data.py -d "data/sales.csv" -t "sales" ```