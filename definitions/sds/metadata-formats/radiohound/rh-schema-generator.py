# This is PEP-723-compatible script: https://peps.python.org/pep-0723/
# You can run it with uv without manually installing its dependencies:
#   uv run rh-schema-generator.py
# Which will run a self-test and create the `<VERSION>/schema.json` file.

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "numpy>=2.1.0",
#     "pydantic>=2.0.0",
#     "rich",
#     "ruff",
# ]
# ///
import ast
import base64
import datetime
import json
import logging
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Any

import numpy as np
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
)
from rich import print  # pylint: disable=redefined-builtin

FORMAT_VERSION = "v0"
MAX_INT_SIZE = int(2**63 - 1)


def log_warning(msg: str) -> None:
    """Log a warning message."""
    logging.warning("%s", msg)


def serialize_data(v: bytes) -> str:
    """Serialize data to a base64 string."""
    return base64.b64encode(v).decode()


def serialize_type(v: "NumpyDType") -> str:  # type: ignore
    return v.value


def validate_mac_address(v: str) -> str:
    pattern = r"^[0-9A-Fa-f]+$"
    if not re.match(pattern=pattern, string=v):
        msg = "MAC address must be a hexadecimal string with no separators"
        raise ValueError(msg)
    return v


def validate_timestamp(v: datetime.datetime) -> datetime.datetime:
    # make sure it has timezone info, defaulting to UTC when missing
    if not v.tzinfo:
        msg = "Timestamp must have timezone information. Assuming UTC."
        log_warning(msg)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        v = v.replace(tzinfo=now_utc.tzinfo)
    return v


def validate_version_after(v: str) -> str:
    # make sure that, if present, it's a valid version string
    pattern = r"^v[0-9]+$"
    if not re.match(pattern=pattern, string=v):
        raise ValueError("Version must match pattern 'v[0-9]+'")
    return v


def validate_data(v: str) -> bytes:
    """Make sure data is a valid base64 encoding."""
    if not v:
        raise ValueError("Data must not be empty")
    try:
        buffer = base64.b64decode(v)
    except Exception as err:
        raise ValueError("Data must be base64 encoded") from err
    return buffer


class DataType(Enum):
    """Data types supported by RadioHound."""

    PERIODOGRAM = "periodogram"


def validate_data_type(v: str) -> DataType:
    try:
        return DataType(v)
    except ValueError as err:
        raise ValueError("Invalid data type") from err


class _RHMetadataV0(BaseModel):
    """Metadata for a RadioHound capture."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    data_type: Annotated[
        DataType,
        AfterValidator(validate_data_type),
        Field(desc="The category of this capture"),
    ]
    fmax: Annotated[
        int,
        Field(desc="The maximum frequency in the sample", gt=0, lt=MAX_INT_SIZE),
    ]
    fmin: Annotated[
        int,
        Field(desc="The minimum frequency in the sample", gt=0, lt=MAX_INT_SIZE),
    ]
    gps_lock: Annotated[
        bool,
        Field(
            description="Whether device coordinates were set and locked (e.g. when satellites are not reachable)",
        ),
    ]
    nfft: Annotated[
        int,
        Field(description="Number of FFT bins, recommended to be a power of 2", gt=0),
    ]
    scan_time: Annotated[
        float,
        Field(desc="The time taken to scan this sample, in seconds", gt=0),
    ]
    xcount: Annotated[
        int,
        Field(desc="The number of points in the periodogram", gt=0, lt=MAX_INT_SIZE),
    ]
    xstart: Annotated[
        int,
        Field(desc="The start frequency of the periodogram", gt=0, lt=MAX_INT_SIZE),
    ]
    xstop: Annotated[
        int,
        Field(desc="The stop frequency of the periodogram", gt=0, lt=MAX_INT_SIZE),
    ]


def all_dtypes() -> set[str]:
    """Return all numpy-compatible data types."""
    return set(dtype.__name__ for dtype in np.sctypeDict.values())


NumpyDType = Enum("NumpyDTypes", {dtype: dtype for dtype in all_dtypes()})


def validate_type(v: str) -> "NumpyDType":  # type: ignore
    if v not in NumpyDType.__members__:
        raise ValueError(f"Invalid data type: {v}")
    return NumpyDType[v]


def nd_array_before_validator(x: str | list) -> np.ndarray:
    # custom before validation logic
    if isinstance(x, str):
        x_list = ast.literal_eval(x)
        x = np.array(x_list)
    if isinstance(x, list):
        x = np.array(x)
    return x


def nd_array_serializer(x) -> list:
    return x.tolist()


class _RadioHoundDataV0(BaseModel):
    """Describes a RadioHound capture."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    data: Annotated[
        bytes, AfterValidator(validate_data), PlainSerializer(serialize_data)
    ]
    data_as_numpy: Annotated[
        np.ndarray,
        Field(default=None, exclude=True),
        BeforeValidator(nd_array_before_validator),
        PlainSerializer(nd_array_serializer, return_type=list),
    ]
    gain: float
    mac_address: Annotated[
        str,
        AfterValidator(validate_mac_address),
        Field(
            description="MAC address of the RadioHound device",
            min_length=12,
            max_length=12,
        ),
    ]
    metadata: Annotated[_RHMetadataV0, Field(description="Metadata for this capture")]
    sample_rate: Annotated[
        int,
        Field(description="Sample rate of the capture in Hz", gt=0, lt=MAX_INT_SIZE),
    ]
    short_name: Annotated[
        str, Field(description="Short name for the capture", max_length=255)
    ]
    timestamp: Annotated[
        datetime.datetime,
        AfterValidator(validate_timestamp),
        Field(
            description="Timestamp of the capture start as ISO 8601 with timezone information."
        ),
    ]

    type: Annotated[
        str,
        AfterValidator(validate_type),
        PlainSerializer(serialize_type),
        Field(description="Numpy data type"),
    ]
    version: Annotated[
        str,
        AfterValidator(validate_version_after),
        Field(
            description="Version of the RadioHound data format",
            max_length=255,
            default="v0",
        ),
    ]
    custom_fields: Annotated[
        dict[str, Any],
        Field(
            description="Custom fields that are not part of the standard schema",
            default_factory=dict,
        ),
    ]

    def model_post_init(self, __context: Any) -> None:  # noqa: F821
        self.data_as_numpy = np.frombuffer(self.data, dtype=self.type.value)
        # return super().model_post_init(__context)

    def to_file(self, file_path: Path | str | bytes) -> None:
        """Write the RadioHound data to a file."""
        obj = self.model_dump(mode="json")
        file_path_real: Path
        if file_path is None:
            raise ValueError("File path must not be None")
        if isinstance(file_path, bytes):
            file_path_real = Path(file_path.decode())
        if isinstance(file_path, str):
            file_path_real = Path(file_path)
        if isinstance(file_path, Path):
            file_path_real = file_path
        # if file_path_real has no extension, use .rh
        if not file_path_real.suffix:
            file_path_real = file_path_real.with_suffix(".rh")
        with file_path_real.open(mode="w", encoding="utf-8") as fp:
            json.dump(obj, fp=fp, indent=4)


def load_rh_file_v0(file_path: Path | str | bytes) -> _RadioHoundDataV0:
    """Loads a valid RadioHound file into memory.

    Args:
        file_path:  Path to a valid RadioHound file to load.
    Returns:
        The loaded RadioHound data.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValidationError: If the file is not a valid RadioHound file.
    """
    file_path_real: Path
    if file_path is None:
        raise ValueError("File path must not be None")
    if isinstance(file_path, bytes):
        file_path_real = Path(file_path.decode())
    if isinstance(file_path, str):
        file_path_real = Path(file_path)
    if isinstance(file_path, Path):
        file_path_real = file_path
    if not file_path_real.exists():
        raise FileNotFoundError(f"File not found: {file_path_real}")
    with open(file_path_real, mode="rb") as fp:
        return _RadioHoundDataV0.model_validate_json(json_data=fp.read())


def _self_test(verbose: bool = False) -> None:
    """Run self-tests."""
    sample_dir = Path(FORMAT_VERSION) / "samples"
    sample_files = [
        sample_dir / "obsolete-reference.rh",
    ]
    if verbose:
        print("\n\nRUNNING SELF-TESTS")
    for sample_file in sample_files:
        if verbose:
            print(f"\tLoading sample file: {sample_file}")
        loaded_model = load_rh_file_v0(sample_file)
        if verbose:
            print("\n\nDUMPED SAMPLE:")
            print(loaded_model.model_dump_json(indent=4))
            print("\n\nNUMPY DATA:")
            print(
                f"Shape: {loaded_model.data_as_numpy.shape}, dtype: {loaded_model.data_as_numpy.dtype}"
            )
        # dump it to a file to create a reference format for this version
        reference_file = sample_file.parent / f"reference-{FORMAT_VERSION}"
        print(f"Writing reference file: {reference_file}")
        loaded_model.to_file(file_path=reference_file)


def _dump_schema(
    model: BaseModel,
    file_path: Path,
    verbose: bool = False,
) -> None:
    """Dump the JSON schema for a model."""
    json_schema = model.model_json_schema(mode="serialization")
    if verbose:
        print("\n\nSCHEMA:")
        print(json_schema)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open(mode="w", encoding="utf-8") as fp:
        json.dump(json_schema, fp=fp, indent=4)


def main() -> None:
    """Entry point to generate the JSON schema."""
    print(f"Python interpreter path: {sys.executable}")
    _self_test(verbose=True)
    schema_path = Path(FORMAT_VERSION) / "schema.json"
    _dump_schema(model=_RadioHoundDataV0, file_path=schema_path, verbose=True)


if __name__ == "__main__":
    main()

RadioHoundData = _RadioHoundDataV0
load_rh_file = load_rh_file_v0

__all__ = ["RadioHoundData", "load_rh_file_v0", "main"]
