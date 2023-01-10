# Usage Examples

## csv-to-database

<br>

Make sure to have `MYSQL` installed on your laptop. Create a user with 
`host='localhost', user='root'` and your password. Don't forgot to store your password in a `.env` file which needs to be inside the project directory. Define the password variable in the file as follows:

>>> ``` MYSQL_PASS=YOUR_PASSWORD ```

<br>

___

<br>

### Version 1

1. First create a database:

            ``` python -m src/tools/upload_data.py -db True ```

2. Create as many tables as you like within the database, and insert data from CSV files. Run the following command to create each table with their respective data. As an example, let's create `sales` table in our database and upload data from a csv file into it:

            ``` python src/tools/upload_data.py -d "data/sales.csv" -t "sales" ```

<br>

___

> Flags to pass to command line:
>
> - -db : Whether to create database or not (bool)
>    
> - -d : input data path (str)
>    
> - -t : table name to create (str)

___

<br>

### Version 2

1. First create a database:

            ``` python -m src/tools/database_V2.py -db True -db_name 'groceries' ```

2. Create as many tables as you like within the database and insert data from each CSV files into their respective tables by running a single python command.

    As an example, let's say we create a database `groceries` by running the above command. We then define tasks in the `config.yaml` file. Task in this case are simply a list to tables we would like to create in our database and path to CSV files for each table. Look at the `config_template.yaml` for more details on how to structure each tasks. 

    Finally, we can run the following line by providing a database and task name as an argument. 

            ``` python src/tools/database_V2.py -db_name 'groceries' -t "csv-to-database" ```

___

> Flags to pass to command line:
>
> - -db : Whether to create database or not (bool)
>    
> - -db_name : database name (str)
>
> - -t : task name (str)


<br>

___

## Illustration

<br>

![illustration](https://user-images.githubusercontent.com/120341649/209677377-170b27ab-ae45-4b36-b614-56aec51c6062.png)
