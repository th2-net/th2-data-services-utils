<!-- markdownlint-disable -->

<a href="../../th2_data_services_utils/graph.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `graph`





---

<a href="../../th2_data_services_utils/graph.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_tick_diagram`

```python
create_tick_diagram(
    data: DataFrame,
    legend_to_table: bool = False
) → Union[DataFrame, NoneType]
```

Create ticks diagram. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`legend_to_table`</b>:  Whether to create legend in Dataframe. 


---

<a href="../../th2_data_services_utils/graph.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_line_plot_image`

```python
create_line_plot_image(
    x: List[int],
    y: List[int],
    file_name: str = 'file',
    x_label: str = None,
    y_label: str = None,
    xticks_label: List[str] = None,
    title: str = 'plot',
    width: int = None,
    height: int = None
) → None
```

Creates Line plot as file. 



**Args:**
 
 - <b>`x`</b>:  Values of X-axis. 
 - <b>`y`</b>:  Values of Y-axis. 
 - <b>`file_name`</b>:  Output file name. 
 - <b>`x_label`</b>:  Label of X-axis. 
 - <b>`y_label`</b>:  Label of Y-axis. 
 - <b>`title`</b>:  Title of plot. 
 - <b>`xticks_label`</b>:  Values for X axis. 
 - <b>`width`</b>:  Width 
 - <b>`height`</b>:  Height 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
