<!-- markdownlint-disable -->

<a href="../../th2_data_services_utils/aggregate.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `aggregate`





---

<a href="../../th2_data_services_utils/aggregate.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `aggregate_by_fields`

```python
aggregate_by_fields(
    data: Union[Iterable[dict], DataFrame],
    *fields: str,
    total_row: bool = False,
    pivot: Union[Iterable[str], str] = None
) → Union[DataFrame, DataFrameGroupBy]
```

Aggregates by fields using the lazy method. The method need you if require to count fields or fields group. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`fields`</b>:  Fields for aggregate. 
 - <b>`total_row`</b>:  Adding a total row. 
 - <b>`pivot`</b>:  Which columns must is pivoted. 



**Returns:**
 Statistics. 



**Raises:**
 ValueError. 


---

<a href="../../th2_data_services_utils/aggregate.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `aggregate_several_group`

```python
aggregate_several_group(
    data: Iterable[dict],
    display_html_df: bool = True,
    receive_df: bool = False
) → Union[DataFrame, NoneType]
```

Aggregates several groups in dataframe. The method divided each field on separated groups. 



**Note:**

> The method can use DataFrame type for output and Html type for output. If you use 'Jupyter Notebook' then use display_html_df = True else False. 
>

**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`display_html_df`</b>:  Whether display to html. 
 - <b>`receive_df`</b>:  Whether to create dataframe. 



**Returns:**
 DataFrame with data divided into groups. 



**Raises:**
 ValueError. 


---

<a href="../../th2_data_services_utils/aggregate.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `aggregate_by_intervals_lazy`

```python
aggregate_by_intervals_lazy(
    data: Iterable[dict],
    time_field: str,
    agg: str = 'count',
    resolution: str = 'D',
    every: int = 1
) → DataFrame
```

Aggregates by time using lazy method. The method only to count quantity records in intervals. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`time_field`</b>:  Time field. 
 - <b>`agg`</b>:  Aggregate function name. 
 - <b>`resolution`</b>:  Datetime suffix for intervals. 
 - <b>`every`</b>:  Frequently of intervals. 



**Returns:**
 Show all groups in dataframe. 



**Raises:**
 ValueError. 


---

<a href="../../th2_data_services_utils/aggregate.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `aggregate_by_intervals`

```python
aggregate_by_intervals(
    data: Iterable[dict],
    time_field: str,
    *fields: str,
    intervals: str = 'Q',
    total_row: bool = False,
    pivot: Union[Iterable[str], str] = None
) → DataFrame
```

Aggregates by fields with time intervals. The method count records and records groups in intervals. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`time_field`</b>:  Time field. 
 - <b>`fields`</b>:  Fields for aggregate. 
 - <b>`intervals`</b>:  Intervals. 
 - <b>`total_row`</b>:  Adding a total row. 
 - <b>`pivot`</b>:  Which columns must is pivoted. 



**Returns:**
 Statistics. 



**Raises:**
 ValueError. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
