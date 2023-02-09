import pytest

from typing import List

from pandas import Timestamp

from th2_data_services_utils.aggregate import (
    aggregate_by_fields,
    aggregate_by_intervals,
    aggregate_several_group,
    # search_fields,
    # append_total_rows,
    # delete_string_by_pattern,
    # find_tag_in_string,
    aggregate_by_intervals_lazy,
)


def test_aggregate_by_fields_empty_data():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_fields([], "test")
    assert exc_info.value


def test_aggregate_by_fields_empty_fields(data_for_analyzing: List[dict]):
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_fields(data_for_analyzing, [])
    assert exc_info.value


def test_aggregate_by_fields_basic_computing(data_for_analyzing: List[dict]):
    output = aggregate_by_fields(data_for_analyzing, "type", "successful")

    assert output.to_dict() == {
        "count": {
            ("Heartbeat", False): 2,
            ("Heartbeat", True): 1,
            ("Receive message", False): 2,
            ("Receive message", True): 3,
            ("Send message", False): 1,
            ("Send message", True): 4,
            ("Test Case", False): 1,
            ("Test Case", True): 4,
            ("Test Run", False): 2,
            ("Test Run", True): 1,
            ("Verification", False): 1,
            ("Verification", True): 2,
        }
    }


def test_aggregate_by_fields_computing_with_total_row(data_for_analyzing: List[dict]):
    output = aggregate_by_fields(
        data_for_analyzing, "type", "successful", total_row=True
    )
    assert output.to_dict() == {
        "count": {
            ("Heartbeat", False): 2,
            ("Heartbeat", True): 1,
            ("Receive message", False): 2,
            ("Receive message", True): 3,
            ("Send message", False): 1,
            ("Send message", True): 4,
            ("Test Case", False): 1,
            ("Test Case", True): 4,
            ("Test Run", False): 2,
            ("Test Run", True): 1,
            ("Verification", False): 1,
            ("Verification", True): 2,
            ("Total", "Total"): 24,
        }
    }


def test_aggregate_by_fields_computing_with_pivot(data_for_analyzing: List[dict]):
    output = aggregate_by_fields(
        data_for_analyzing, "type", "successful", pivot="successful"
    )

    assert output.to_dict() == {
        False: {
            "Heartbeat": 2,
            "Receive message": 2,
            "Send message": 1,
            "Test Case": 1,
            "Test Run": 2,
            "Verification": 1,
        },
        True: {
            "Heartbeat": 1,
            "Receive message": 3,
            "Send message": 4,
            "Test Case": 4,
            "Test Run": 1,
            "Verification": 2,
        },
    }


def test_aggregate_by_fields_computing_with_pivot_and_total_row(
        data_for_analyzing: List[dict],
):
    output = aggregate_by_fields(
        data_for_analyzing, "type", "successful", pivot="successful", total_row=True
    )

    assert output.to_dict() == {
        False: {
            "Heartbeat": 2,
            "Receive message": 2,
            "Send message": 1,
            "Test Case": 1,
            "Test Run": 2,
            "Verification": 1,
            "Total": 9,
        },
        True: {
            "Heartbeat": 1,
            "Receive message": 3,
            "Send message": 4,
            "Test Case": 4,
            "Test Run": 1,
            "Verification": 2,
            "Total": 15,
        },
    }


def test_aggregate_by_intervals_data_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals([], "time")
    assert exc_info.value


def test_aggregate_by_intervals_data_basic(data_for_analyzing: List[dict]):
    output = aggregate_by_intervals(
        data_for_analyzing, "time", "eventName", "type", intervals="min"
    )

    assert output.to_dict() == {
        "count": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3", "Test Case"): 1,
            (Timestamp("2021-01-01 01:01:00"), "test run 1", "Test Run"): 1,
            (Timestamp("2021-01-01 01:02:00"), "test run 2", "Test Run"): 1,
            (Timestamp("2021-01-01 01:03:00"), "message", "Send message"): 1,
            (Timestamp("2021-01-01 01:04:00"), "test case 1", "Test Case"): 1,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 01:11:00"), "message 444", "Receive message"): 1,
            (Timestamp("2021-01-01 01:13:00"), "message123", "Receive message"): 1,
            (Timestamp("2021-01-01 01:23:00"), "message 333", "Receive message"): 1,
            (Timestamp("2021-01-01 01:32:00"), "test run 3", "Test Case"): 1,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 01:33:00"), "test run 4", "Test Run"): 1,
            (Timestamp("2021-01-01 01:40:00"), "test case 4", "Test Case"): 1,
            (Timestamp("2021-01-01 01:41:00"), "message122", "Receive message"): 1,
            (Timestamp("2021-01-01 01:43:00"), "message 444", "Send message"): 1,
            (Timestamp("2021-01-01 01:44:00"), "message122", "Send message"): 1,
            (Timestamp("2021-01-01 01:45:00"), "verification32", "Verification"): 1,
            (Timestamp("2021-01-01 01:54:00"), "verification33", "Verification"): 1,
            (Timestamp("2021-01-01 01:55:00"), "message 333", "Send message"): 1,
            (Timestamp("2021-01-01 01:56:00"), "message 444", "Receive message"): 1,
            (Timestamp("2021-01-01 02:10:00"), "test case 2", "Test Case"): 1,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 02:12:00"), "message123", "Send message"): 1,
            (Timestamp("2021-01-01 02:33:00"), "verification", "Verification"): 1,
        }
    }


def test_aggregate_by_intervals_data_with_total_row(data_for_analyzing: List[dict]):
    output = aggregate_by_intervals(
        data_for_analyzing, "time", "eventName", "type", intervals="min", total_row=True
    )

    assert output.to_dict() == {
        "count": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3", "Test Case"): 1,
            (Timestamp("2021-01-01 01:01:00"), "test run 1", "Test Run"): 1,
            (Timestamp("2021-01-01 01:02:00"), "test run 2", "Test Run"): 1,
            (Timestamp("2021-01-01 01:03:00"), "message", "Send message"): 1,
            (Timestamp("2021-01-01 01:04:00"), "test case 1", "Test Case"): 1,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 01:11:00"), "message 444", "Receive message"): 1,
            (Timestamp("2021-01-01 01:13:00"), "message123", "Receive message"): 1,
            (Timestamp("2021-01-01 01:23:00"), "message 333", "Receive message"): 1,
            (Timestamp("2021-01-01 01:32:00"), "test run 3", "Test Case"): 1,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 01:33:00"), "test run 4", "Test Run"): 1,
            (Timestamp("2021-01-01 01:40:00"), "test case 4", "Test Case"): 1,
            (Timestamp("2021-01-01 01:41:00"), "message122", "Receive message"): 1,
            (Timestamp("2021-01-01 01:43:00"), "message 444", "Send message"): 1,
            (Timestamp("2021-01-01 01:44:00"), "message122", "Send message"): 1,
            (Timestamp("2021-01-01 01:45:00"), "verification32", "Verification"): 1,
            (Timestamp("2021-01-01 01:54:00"), "verification33", "Verification"): 1,
            (Timestamp("2021-01-01 01:55:00"), "message 333", "Send message"): 1,
            (Timestamp("2021-01-01 01:56:00"), "message 444", "Receive message"): 1,
            (Timestamp("2021-01-01 02:10:00"), "test case 2", "Test Case"): 1,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat", "Heartbeat"): 1,
            (Timestamp("2021-01-01 02:12:00"), "message123", "Send message"): 1,
            (Timestamp("2021-01-01 02:33:00"), "verification", "Verification"): 1,
            ("Total", "Total", "Total"): 24.0,
        }
    }


def test_aggregate_by_intervals_data_with_pivot(data_for_analyzing: List[dict]):
    output = aggregate_by_intervals(
        data_for_analyzing, "time", "eventName", "type", intervals="min", pivot="type"
    ).fillna(0)

    assert output.to_dict() == {
        "Heartbeat": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 0,
        },
        "Receive message": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 1.0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 1.0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 1.0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 0,
        },
        "Send message": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 1.0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 1.0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 1.0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 1.0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 0,
        },
        "Test Case": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 1.0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 1.0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 1.0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 1.0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 1.0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 0,
        },
        "Test Run": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 1.0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 1.0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 1.0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 0,
        },
        "Verification": {
            (Timestamp("2021-01-01 01:01:00"), "test case 3"): 0,
            (Timestamp("2021-01-01 01:01:00"), "test run 1"): 0,
            (Timestamp("2021-01-01 01:02:00"), "test run 2"): 0,
            (Timestamp("2021-01-01 01:03:00"), "message"): 0,
            (Timestamp("2021-01-01 01:04:00"), "test case 1"): 0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:11:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:13:00"), "message123"): 0,
            (Timestamp("2021-01-01 01:23:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:32:00"), "test run 3"): 0,
            (Timestamp("2021-01-01 01:33:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 01:33:00"), "test run 4"): 0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 0,
            (Timestamp("2021-01-01 01:41:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:43:00"), "message 444"): 0,
            (Timestamp("2021-01-01 01:44:00"), "message122"): 0,
            (Timestamp("2021-01-01 01:45:00"), "verification32"): 1.0,
            (Timestamp("2021-01-01 01:54:00"), "verification33"): 1.0,
            (Timestamp("2021-01-01 01:55:00"), "message 333"): 0,
            (Timestamp("2021-01-01 01:56:00"), "message 444"): 0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 0,
            (Timestamp("2021-01-01 02:12:00"), "heartbeat"): 0,
            (Timestamp("2021-01-01 02:12:00"), "message123"): 0,
            (Timestamp("2021-01-01 02:33:00"), "verification"): 1.0,
        },
    }


def test_aggregate_by_intervals_lazy_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals_lazy([], "time")
    assert exc_info.value


def test_aggregate_by_intervals_lazy_data_basic(data_for_analyzing: List[dict]):
    output = aggregate_by_intervals_lazy(
        data_for_analyzing, "time", resolution="m", every=30
    )

    assert output.to_dict() == {
        "time": {
            0: Timestamp("2021-01-01 01:02:00"),
            1: Timestamp("2021-01-01 01:32:00"),
            2: Timestamp("2021-01-01 02:02:00"),
            3: Timestamp("2021-01-01 02:32:00"),
        },
        "count": {0: 7, 1: 11, 2: 3, 3: 1},
    }


def test_aggregate_several_group_data_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_several_group([])
    assert exc_info


def test_aggregate_several_group(data_for_analyzing: List[dict]):
    output = aggregate_several_group(
        data_for_analyzing, display_html_df=False, receive_df=True
    ).fillna("-")

    assert output.to_dict() == {
        "time": {
            0: Timestamp("2021-01-01 01:01:01"),
            1: Timestamp("2021-01-01 01:01:59"),
            2: Timestamp("2021-01-01 01:02:12"),
            3: Timestamp("2021-01-01 01:03:54"),
            4: Timestamp("2021-01-01 01:04:30"),
            5: Timestamp("2021-01-01 01:10:02"),
            6: Timestamp("2021-01-01 01:11:11"),
            7: Timestamp("2021-01-01 01:13:40"),
            8: Timestamp("2021-01-01 01:23:23"),
            9: Timestamp("2021-01-01 01:32:42"),
            10: Timestamp("2021-01-01 01:33:12"),
            11: Timestamp("2021-01-01 01:33:33"),
            12: Timestamp("2021-01-01 01:40:10"),
            13: Timestamp("2021-01-01 01:41:19"),
            14: Timestamp("2021-01-01 01:43:43"),
            15: Timestamp("2021-01-01 01:44:44"),
            16: Timestamp("2021-01-01 01:45:22"),
            17: Timestamp("2021-01-01 01:54:52"),
            18: Timestamp("2021-01-01 01:55:55"),
            19: Timestamp("2021-01-01 01:56:32"),
            20: Timestamp("2021-01-01 02:10:01"),
            21: Timestamp("2021-01-01 02:12:11"),
            22: Timestamp("2021-01-01 02:12:32"),
            23: Timestamp("2021-01-01 02:33:01"),
            24: "Total",
        },
        "count": {
            0: 10.0,
            1: 14.0,
            2: 24.0,
            3: "-",
            4: "-",
            5: "-",
            6: "-",
            7: "-",
            8: "-",
            9: "-",
            10: "-",
            11: "-",
            12: "-",
            13: "-",
            14: "-",
            15: "-",
            16: "-",
            17: "-",
            18: "-",
            19: "-",
            20: "-",
            21: "-",
            22: "-",
            23: "-",
            24: "-",
        },
        "type": {
            0: "Heartbeat",
            1: "Receive message",
            2: "Send message",
            3: "Test Case",
            4: "Test Run",
            5: "Verification",
            6: "Total",
            7: "-",
            8: "-",
            9: "-",
            10: "-",
            11: "-",
            12: "-",
            13: "-",
            14: "-",
            15: "-",
            16: "-",
            17: "-",
            18: "-",
            19: "-",
            20: "-",
            21: "-",
            22: "-",
            23: "-",
            24: "-",
        },
        "eventName": {
            0: "heartbeat",
            1: "message",
            2: "message 333",
            3: "message 444",
            4: "message122",
            5: "message123",
            6: "test case 1",
            7: "test case 2",
            8: "test case 3",
            9: "test case 4",
            10: "test run 1",
            11: "test run 2",
            12: "test run 3",
            13: "test run 4",
            14: "verification",
            15: "verification32",
            16: "verification33",
            17: "Total",
            18: "-",
            19: "-",
            20: "-",
            21: "-",
            22: "-",
            23: "-",
            24: "-",
        },
        "successful": {
            0: False,
            1: True,
            2: "Total",
            3: "-",
            4: "-",
            5: "-",
            6: "-",
            7: "-",
            8: "-",
            9: "-",
            10: "-",
            11: "-",
            12: "-",
            13: "-",
            14: "-",
            15: "-",
            16: "-",
            17: "-",
            18: "-",
            19: "-",
            20: "-",
            21: "-",
            22: "-",
            23: "-",
            24: "-",
        },
        "attachedMessageIds": {
            0: False,
            1: True,
            2: "Total",
            3: "-",
            4: "-",
            5: "-",
            6: "-",
            7: "-",
            8: "-",
            9: "-",
            10: "-",
            11: "-",
            12: "-",
            13: "-",
            14: "-",
            15: "-",
            16: "-",
            17: "-",
            18: "-",
            19: "-",
            20: "-",
            21: "-",
            22: "-",
            23: "-",
            24: "-",
        },
    }


def test_aggregate_group_by_intervals_data_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals([], "time", "field")
    assert exc_info.value


def test_aggregate_group_by_intervals_fields_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals([{"time": ["test"]}], "time", [])
    assert exc_info.value


def test_aggregate_group_by_intervals_time_series_empty():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals([{"time": []}], "time", "field")
    assert exc_info.value


def test_aggregate_group_by_intervals_time_has_not_time_type():
    with pytest.raises(ValueError) as exc_info:
        aggregate_by_intervals(
            [{"time": ["test1", "test2", "test3"]}], "time", "field"
        )
    assert exc_info.value


def test_aggregate_groups_by_intervals(data_for_analyzing: List[dict]):
    output = aggregate_by_intervals(
        data_for_analyzing,
        "time",
        "eventName",
        "successful",
        intervals="10min",
        total_row=True,
        pivot="successful",
    ).fillna("-")

    assert output.to_dict() == {
        False: {
            (Timestamp("2021-01-01 01:00:00"), "message"): 1.0,
            (Timestamp("2021-01-01 01:00:00"), "test case 1"): "-",
            (Timestamp("2021-01-01 01:00:00"), "test case 3"): 1.0,
            (Timestamp("2021-01-01 01:00:00"), "test run 1"): "-",
            (Timestamp("2021-01-01 01:00:00"), "test run 2"): 1.0,
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): "-",
            (Timestamp("2021-01-01 01:10:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 01:10:00"), "message123"): "-",
            (Timestamp("2021-01-01 01:20:00"), "message 333"): 1.0,
            (Timestamp("2021-01-01 01:30:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 01:30:00"), "test run 3"): "-",
            (Timestamp("2021-01-01 01:30:00"), "test run 4"): 1.0,
            (Timestamp("2021-01-01 01:40:00"), "message 444"): "-",
            (Timestamp("2021-01-01 01:40:00"), "message122"): "-",
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): "-",
            (Timestamp("2021-01-01 01:40:00"), "verification32"): "-",
            (Timestamp("2021-01-01 01:50:00"), "message 333"): "-",
            (Timestamp("2021-01-01 01:50:00"), "message 444"): "-",
            (Timestamp("2021-01-01 01:50:00"), "verification33"): 1.0,
            (Timestamp("2021-01-01 02:10:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 02:10:00"), "message123"): "-",
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): "-",
            (Timestamp("2021-01-01 02:30:00"), "verification"): "-",
            ("Total", "Total"): 9.0,
        },
        True: {
            (Timestamp("2021-01-01 01:00:00"), "message"): "-",
            (Timestamp("2021-01-01 01:00:00"), "test case 1"): 1.0,
            (Timestamp("2021-01-01 01:00:00"), "test case 3"): "-",
            (Timestamp("2021-01-01 01:00:00"), "test run 1"): 1.0,
            (Timestamp("2021-01-01 01:00:00"), "test run 2"): "-",
            (Timestamp("2021-01-01 01:10:00"), "heartbeat"): 1.0,
            (Timestamp("2021-01-01 01:10:00"), "message 444"): "-",
            (Timestamp("2021-01-01 01:10:00"), "message123"): 1.0,
            (Timestamp("2021-01-01 01:20:00"), "message 333"): "-",
            (Timestamp("2021-01-01 01:30:00"), "heartbeat"): "-",
            (Timestamp("2021-01-01 01:30:00"), "test run 3"): 1.0,
            (Timestamp("2021-01-01 01:30:00"), "test run 4"): "-",
            (Timestamp("2021-01-01 01:40:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 01:40:00"), "message122"): 2.0,
            (Timestamp("2021-01-01 01:40:00"), "test case 4"): 1.0,
            (Timestamp("2021-01-01 01:40:00"), "verification32"): 1.0,
            (Timestamp("2021-01-01 01:50:00"), "message 333"): 1.0,
            (Timestamp("2021-01-01 01:50:00"), "message 444"): 1.0,
            (Timestamp("2021-01-01 01:50:00"), "verification33"): "-",
            (Timestamp("2021-01-01 02:10:00"), "heartbeat"): "-",
            (Timestamp("2021-01-01 02:10:00"), "message123"): 1.0,
            (Timestamp("2021-01-01 02:10:00"), "test case 2"): 1.0,
            (Timestamp("2021-01-01 02:30:00"), "verification"): 1.0,
            ("Total", "Total"): 15.0,
        },
    }
