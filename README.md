It is a simple python script which exposes data of a csv file as a JSON via simple http rest services.
•	Services –
1.	/emp - return all rows of the csv file as a JSON array.
2.	/emp/column/{csv column name} – It return all values of a csv column.
o	E.g. - /emp/column/City will return all Cities like “Seattle, Fairfax, ALDIE, Chantilly, Herndon”
3.	/emp/search/{search string} - It returns all rows of the csv file in a json array, where each row contains given string.
4.	/emp/search/{csv column name}/{searchString} – It works same like above service but the search is performed only in the given column name instead of on all columns.
