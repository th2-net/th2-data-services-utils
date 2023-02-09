<!-- markdownlint-disable -->

<a href="../../th2_data_services_utils/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils`





---

<a href="../../th2_data_services_utils/utils.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `search_fields`

```python
search_fields(
    data: Union[List[dict], dict],
    *fields: str
) → DefaultDict[str, List[Any]]
```

Search for fields. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`fields`</b>:  Fields for search 



**Returns:**
 Dictionary with a list of found tags. 


---

<a href="../../th2_data_services_utils/utils.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `append_total_rows`

```python
append_total_rows(
    data: DataFrameGroupBy,
    fields_options: Dict[str, str]
) → Union[DataFrame, DataFrameGroupBy]
```

Append total rows in data. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`fields_options`</b>:  Aggregate function for total rows. 



**Returns:**
 DataFrame with total rows. 


---

<a href="../../th2_data_services_utils/utils.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `delete_string_by_pattern`

```python
delete_string_by_pattern(string: str, pattern: str) → str
```

Deletes string by pattern. 



**Args:**
 
 - <b>`string`</b>:  String for delete. 
 - <b>`pattern`</b>:  Pattern. 



**Returns:**
 String with deleted pieces. 


---

<a href="../../th2_data_services_utils/utils.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_tag_in_string`

```python
find_tag_in_string(data: str, search_tag: str) → str
```

Find tag value in record as string. 



**Args:**
 
 - <b>`data`</b>:  Record as string. 
 - <b>`search_tag`</b>:  Tag for search. 



**Returns:**
 Tag value. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
