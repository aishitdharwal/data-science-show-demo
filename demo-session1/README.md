## Usage Examples

### ***csv-to-database***

___

Make sure to have ***MYSQL*** installed on your laptop. Create a user with 
`host='localhost', user='root'` and your password. Don't forgot to store your password in a `.env` file which needs to be inside the project directory. Fill in the file as follows:

>>> ```MYSQL_PASS=YOUR_PASSWORD```

___

First create a database:

```python -m src/tools/upload_data.py -db True```

Then you can create as many tables as you like within the database. Insert data from CSV files. As an example, insert **sales** data to database:

```python src/tools/upload_data.py -d "data/sales.csv" -t "sales" ```

___

> Flags to pass to command line:
>
> - -db : Whether to create database or not (bool)
>    
> - -d : input data path (str)
>    
> - -t : table name to create (str)

## Illustration
![illustration](https://user-images.githubusercontent.com/120341649/209677377-170b27ab-ae45-4b36-b614-56aec51c6062.png)