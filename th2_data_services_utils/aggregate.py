from functools import reduce
from itertools import chain, cycle
from typing import Union, Iterable, Optional

import vaex
from IPython.core.display import display_html
from pandas import DataFrame, concat, Series, Grouper
from pandas.core.groupby import DataFrameGroupBy


def aggregate_by_fields(
        data: Union[Iterable[dict], DataFrame],
        *fields: str,
        total_row: bool = False,
        pivot: Union[Iterable[str], str] = None,
) -> Union[DataFrame, DataFrameGroupBy]:
    """Aggregates by fields using the lazy method.

    Args:
        data: Data.
        fields: Fields for aggregate.
        total_row: Adding a total row.
        pivot: Which columns must is pivoted.

    Returns:
        Statistics.

    Examples:
    --------
    >> raw_data = [
        {'attachedMessageIds': False, 'eventName': 'test run 1', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 1, 1), 'type': 'Test Run'},
        {'attachedMessageIds': True, 'eventName': 'heartbeat', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 10, 2), 'type': 'Heartbeat'},
        {'attachedMessageIds': False, 'eventName': 'test run 2', 'successful': False,
          'time': datetime.datetime(2021, 1, 1, 1, 2, 12), 'type': 'Test Run'},
          . . . . . ]
    >> data = aggregate_by_fields(raw_data, "type", "successful")
                                    count
    type            successful
    Heartbeat       False           2
                    True            1
    Receive message False           2
                    True            3
    Send message    False           1
                    True            4
    Test Case       False           1
                    True            4
    Test Run        False           2
                    True            1
    Verification    False           1
                    True            2

    >> data_total = aggregate_by_fields(raw_data, "type", "successful", total_row=True)
                                    count
    type            successful
    Heartbeat       False           2.0
                    True            1.0
    Receive message False           2.0
                    True            3.0
    Send message    False           1.0
                    True            4.0
    Test Case       False           1.0
                    True            4.0
    Test Run        False           2.0
                    True            1.0
    Verification    False           1.0
                    True            2.0
    Total           Total           24.0

    >> data_pivot = aggregate_by_fields(raw_data, "type", "successful", pivot="successful")

    successful       False  True
    type
    Heartbeat            2      1
    Receive message      2      3
    Send message         1      4
    Test Case            1      4
    Test Run             2      1
    Verification         1      2

    --------
    """
    df = DataFrame(data)
    if df.empty:
        raise ValueError("Input data is empty.")
    if not fields:
        raise ValueError("Fields is empty.")

    df: DataFrame = (
        vaex.from_pandas(df)
            .groupby(by=fields, agg="count", sort=True)
            .to_pandas_df()
            .set_index([*fields])
    )

    if pivot:
        if isinstance(pivot, str):
            pivot = (pivot,)
        index = (field for field in fields if field not in pivot)
        df = df.reset_index().pivot(index=index, columns=pivot, values="count")
    if total_row:
        index_length = len(df.index.names)
        name = ("Total",) * index_length if index_length > 1 else "Total"
        df.loc[name, :] = [
            column.sum() if str(column.dtype) != "object" else "Total"
            for _, column in df.items()
        ]
    return df


def aggregate_several_group(
        data: Iterable[dict], display_html_df: bool = True, receive_df: bool = False
) -> Optional[DataFrame]:
    """Aggregates several groups in dataframe.

    Args:
        data: Data.
        display_html_df: Whether display to html.
        receive_df: Whether to create dataframe.

    Returns:
        DataFrame with data divided into groups.

    Examples:
    --------
    >> raw_data = [
        {'attachedMessageIds': False, 'eventName': 'test run 1', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 1, 1), 'type': 'Test Run'},
        {'attachedMessageIds': True, 'eventName': 'heartbeat', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 10, 2), 'type': 'Heartbeat'},
        {'attachedMessageIds': False, 'eventName': 'test run 2', 'successful': False,
          'time': datetime.datetime(2021, 1, 1, 1, 2, 12), 'type': 'Test Run'},
          . . . . . ]
    >> output = aggregate_several_group(raw_data, display_html_df=False, receive_df=True).fillna("-")

                       time count             type  ... count attachedMessageIds count
    0   2021-01-01 01:01:01   1.0        Heartbeat  ...     9              False    10
    1   2021-01-01 01:01:59   1.0  Receive message  ...    15               True    14
    2   2021-01-01 01:02:12   1.0     Send message  ...    24              Total    24
    3   2021-01-01 01:03:54   1.0        Test Case  ...     -                  -     -
    4   2021-01-01 01:04:30   1.0         Test Run  ...     -                  -     -
    5   2021-01-01 01:10:02   1.0     Verification  ...     -                  -     -
    6   2021-01-01 01:11:11   1.0            Total  ...     -                  -     -
    7   2021-01-01 01:13:40   1.0                -  ...     -                  -     -
    8   2021-01-01 01:23:23   1.0                -  ...     -                  -     -
    9   2021-01-01 01:32:42   1.0                -  ...     -                  -     -
    10  2021-01-01 01:33:12   1.0                -  ...     -                  -     -
    11  2021-01-01 01:33:33   1.0                -  ...     -                  -     -
    12  2021-01-01 01:40:10   1.0                -  ...     -                  -     -
    13  2021-01-01 01:41:19   1.0                -  ...     -                  -     -
    14  2021-01-01 01:43:43   1.0                -  ...     -                  -     -
    15  2021-01-01 01:44:44   1.0                -  ...     -                  -     -
    16  2021-01-01 01:45:22   1.0                -  ...     -                  -     -
    17  2021-01-01 01:54:52   1.0                -  ...     -                  -     -
    18  2021-01-01 01:55:55   1.0                -  ...     -                  -     -
    19  2021-01-01 01:56:32   1.0                -  ...     -                  -     -
    20  2021-01-01 02:10:01   1.0                -  ...     -                  -     -
    21  2021-01-01 02:12:11   1.0                -  ...     -                  -     -
    22  2021-01-01 02:12:32   1.0                -  ...     -                  -     -
    23  2021-01-01 02:33:01   1.0                -  ...     -                  -     -
    24                Total  24.0                -  ...     -                  -     -

    --------
    """

    if not data:
        raise ValueError("Input data is empty.")

    df = DataFrame(data)

    results = []
    for column in df.columns:
        results.append(aggregate_by_fields(df, column, total_row=True).reset_index())

    if display_html_df:
        html_str = ""
        for output, title in zip(results, chain(cycle([""]), cycle(["</br>"]))):
            html_str += '<th style="text-align: center"><td style="vertical-align:top">'
            html_str += f"<h2>{title}<h2>"
            html_str += output.to_html().replace(
                "table", 'table style="display:inline"'
            )
            html_str += "</td><th>"
        display_html(html_str, raw=True)

    if receive_df:
        result = reduce(
            lambda main_df, another_df: concat([main_df, another_df], axis=1)
            if len(main_df.index) > len(another_df.index)
            else concat([another_df, main_df], axis=1),
            results,
        )
        return result


def aggregate_by_intervals_lazy(
        data: Iterable[dict],
        time_field: str,
        agg: str = "count",
        resolution: str = "D",
        every: int = 1,
) -> DataFrame:
    """Aggregates by time using lazy method.

    Args:
        data: Data.
        time_field: Time field.
        agg: Aggregate function name.
        resolution: Datetime suffix for intervals.
        every: Frequently of intervals.

    Returns:
        Show all groups in dataframe.

    Examples:
    --------
    >> raw_data = [
        {'attachedMessageIds': False, 'eventName': 'test run 1', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 1, 1), 'type': 'Test Run'},
        {'attachedMessageIds': True, 'eventName': 'heartbeat', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 10, 2), 'type': 'Heartbeat'},
        {'attachedMessageIds': False, 'eventName': 'test run 2', 'successful': False,
          'time': datetime.datetime(2021, 1, 1, 1, 2, 12), 'type': 'Test Run'},
          . . . . . ]
    >> output = aggregate_by_intervals_lazy(data_for_analyzing, "time", resolution="m", every=30)

    time  count
    0 2021-01-01 01:02:00      7
    1 2021-01-01 01:32:00     11
    2 2021-01-01 02:02:00      3
    3 2021-01-01 02:32:00      1

    --------
    """
    if not data:
        raise ValueError("Input data is empty.")

    dfv = vaex.from_pandas(DataFrame(data))
    compute = dfv.groupby(
        by=vaex.BinnerTime(
            expression=time_field, df=dfv, resolution=resolution, every=every
        ),
        agg=agg,
    ).to_pandas_df()

    return compute


def aggregate_by_intervals(
        data: Iterable[dict],
        time_field: str,
        *fields: str,
        intervals: str = "Q",
        total_row: bool = False,
        pivot: Union[Iterable[str], str] = None,
) -> DataFrame:
    """Aggregates by fields with time intervals.

    Args:
        data: Data.
        time_field: Time field.
        fields: Fields for aggregate.
        intervals: Intervals.
        total_row: Adding a total row.
        pivot: Which columns must is pivoted.

    Returns:
        Statistics.

    Examples:
    --------
    >> raw_data = [
        {'attachedMessageIds': False, 'eventName': 'test run 1', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 1, 1), 'type': 'Test Run'},
        {'attachedMessageIds': True, 'eventName': 'heartbeat', 'successful': True,
            'time': datetime.datetime(2021, 1, 1, 1, 10, 2), 'type': 'Heartbeat'},
        {'attachedMessageIds': False, 'eventName': 'test run 2', 'successful': False,
          'time': datetime.datetime(2021, 1, 1, 1, 2, 12), 'type': 'Test Run'},
          . . . . . ]
    >> data = aggregate_by_intervals(data_for_analyzing, "time", "eventName", "type", intervals="min")
                                                            count
    time                eventName      type
    2021-01-01 01:01:00 test case 3    Test Case            1
                        test run 1     Test Run             1
    2021-01-01 01:02:00 test run 2     Test Run             1
    2021-01-01 01:03:00 message        Send message         1
    2021-01-01 01:04:00 test case 1    Test Case            1
    2021-01-01 01:10:00 heartbeat      Heartbeat            1
    2021-01-01 01:11:00 message 444    Receive message      1
    2021-01-01 01:13:00 message123     Receive message      1
    2021-01-01 01:23:00 message 333    Receive message      1
    2021-01-01 01:32:00 test run 3     Test Case            1
    2021-01-01 01:33:00 heartbeat      Heartbeat            1
                        test run 4     Test Run             1
    2021-01-01 01:40:00 test case 4    Test Case            1
    2021-01-01 01:41:00 message122     Receive message      1
    2021-01-01 01:43:00 message 444    Send message         1
    2021-01-01 01:44:00 message122     Send message         1
    2021-01-01 01:45:00 verification32 Verification         1
    2021-01-01 01:54:00 verification33 Verification         1
    2021-01-01 01:55:00 message 333    Send message         1
    2021-01-01 01:56:00 message 444    Receive message      1
    2021-01-01 02:10:00 test case 2    Test Case            1
    2021-01-01 02:12:00 heartbeat      Heartbeat            1
                        message123     Send message         1
    2021-01-01 02:33:00 verification   Verification         1

    >> data = aggregate_by_intervals(data_for_analyzing, "time", "eventName", "type", intervals="min", total_row=True)
                                                            count
    time                eventName      type
    2021-01-01 01:01:00 test case 3    Test Case            1
                        test run 1     Test Run             1
    2021-01-01 01:02:00 test run 2     Test Run             1
    2021-01-01 01:03:00 message        Send message         1
    2021-01-01 01:04:00 test case 1    Test Case            1
    2021-01-01 01:10:00 heartbeat      Heartbeat            1
    2021-01-01 01:11:00 message 444    Receive message      1
    2021-01-01 01:13:00 message123     Receive message      1
    2021-01-01 01:23:00 message 333    Receive message      1
    2021-01-01 01:32:00 test run 3     Test Case            1
    2021-01-01 01:33:00 heartbeat      Heartbeat            1
                        test run 4     Test Run             1
    2021-01-01 01:40:00 test case 4    Test Case            1
    2021-01-01 01:41:00 message122     Receive message      1
    2021-01-01 01:43:00 message 444    Send message         1
    2021-01-01 01:44:00 message122     Send message         1
    2021-01-01 01:45:00 verification32 Verification         1
    2021-01-01 01:54:00 verification33 Verification         1
    2021-01-01 01:55:00 message 333    Send message         1
    2021-01-01 01:56:00 message 444    Receive message      1
    2021-01-01 02:10:00 test case 2    Test Case            1
    2021-01-01 02:12:00 heartbeat      Heartbeat            1
                        message123     Send message         1
    2021-01-01 02:33:00 verification   Verification         1
    Total               Total          Total             24.0

    >> data = aggregate_by_intervals(data_for_analyzing, "time", "eventName", "type", intervals="min", pivot="type")

    type                                Heartbeat  ...  Verification
    time                eventName                  ...
    2021-01-01 01:01:00 test case 3           NaN  ...           NaN
                        test run 1            NaN  ...           NaN
    2021-01-01 01:02:00 test run 2            NaN  ...           NaN
    2021-01-01 01:03:00 message               NaN  ...           NaN
    2021-01-01 01:04:00 test case 1           NaN  ...           NaN
    2021-01-01 01:10:00 heartbeat             1.0  ...           NaN
    2021-01-01 01:11:00 message 444           NaN  ...           NaN
    2021-01-01 01:13:00 message123            NaN  ...           NaN
    2021-01-01 01:23:00 message 333           NaN  ...           NaN
    2021-01-01 01:32:00 test run 3            NaN  ...           NaN
    2021-01-01 01:33:00 heartbeat             1.0  ...           NaN
                        test run 4            NaN  ...           NaN
    2021-01-01 01:40:00 test case 4           NaN  ...           NaN
    2021-01-01 01:41:00 message122            NaN  ...           NaN
    2021-01-01 01:43:00 message 444           NaN  ...           NaN
    2021-01-01 01:44:00 message122            NaN  ...           NaN
    2021-01-01 01:45:00 verification32        NaN  ...           1.0
    2021-01-01 01:54:00 verification33        NaN  ...           1.0
    2021-01-01 01:55:00 message 333           NaN  ...           NaN
    2021-01-01 01:56:00 message 444           NaN  ...           NaN
    2021-01-01 02:10:00 test case 2           NaN  ...           NaN
    2021-01-01 02:12:00 heartbeat             1.0  ...           NaN
                        message123            NaN  ...           NaN
    2021-01-01 02:33:00 verification          NaN  ...           1.0

    --------
    """
    if not data:
        raise ValueError("Input data is empty.")
    if not fields:
        raise ValueError("Fields is empty")

    df = DataFrame(data=data)

    time: Series = df.get(time_field)
    if time.empty:
        raise ValueError(f"{time_field} is empty.")
    elif time.dtype != "datetime64[ns]":
        raise ValueError(f"{time_field} isn't of type datetime64[ns]")

    df = (
        df.filter(items=[time_field, *fields])
            .set_index(time_field)
            .groupby([Grouper(freq=intervals), *fields], sort=True)
            .size()
            .reset_index(name="count")
            .set_index([time_field, *fields])
    )

    if pivot:
        if isinstance(pivot, str):
            pivot = (pivot,)
        index = [time_field] + [field for field in fields if field not in pivot]
        df = df.reset_index().pivot(index=index, columns=pivot, values="count")
    if total_row:
        index_length = len(df.index.names)
        name = ("Total",) * index_length if index_length > 1 else "Total"
        df.loc[name, :] = [
            column.sum() if str(column.dtype) != "object" else "Total"
            for _, column in df.items()
        ]
    return df
