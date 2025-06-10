# Digital RF Metadata Format under SDS

This document intends to bring the Digital-RF metadata specification into SDS and resolve ambiguities.

This is the reference documentation for writing metadata validators, deciding on database schemas, and similar tasks involving Digital-RF metadata.

> [!NOTE]
> The Digital-RF metadata format allows users to include optional metadata, but does not indicate nor enforce *how* they should add these custom metadata attributes.
> As a consequence, Digital-RF mixes its own namespace with the users', preventing the format from reliably evolving over time.
> We should be more strict about user-defined metadata before integrating it into SDS see [Namespaces](#namespaces).

+ [Digital RF Metadata Format under SDS](#digital-rf-metadata-format-under-sds)
    + [Format Specification](#format-specification)
        + [Required Attributes](#required-attributes)
        + [Optional Attributes](#optional-attributes)
        + [Extended Digital RF Capture Attributes under SDS](#extended-digital-rf-capture-attributes-under-sds)
    + [Data and Metadata](#data-and-metadata)
    + [Namespaces](#namespaces)
    + [HDF5 Layout](#hdf5-layout)
        + [RF File Layout](#rf-file-layout)
        + [File Cadence](#file-cadence)
        + [Directory Layout](#directory-layout)

## Format Specification

> The 3 right-most columns (`Type from docs / code`, `Name`, and `Description`) were extracted from their [v2 reference documentation](https://naic.nrao.edu/arecibo/phil/software/datataking/usrp/DigitalRF2.0.pdf) and/or source code.
> The source code version is favored when there are discrepancies.
> Keep this file up-to-date in case of changes to the original specification.

### Required Attributes

The 15 metadata attributes always returned are:

| Ideal Type (min bit rep) | Type from docs / code | Name                          | Description                                                                                                                                            |
| ------------------------ | --------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `int (u64b)`             | `int (u64b)`          | `H5Tget_class`                | result of `H5Tget_class(hdf5_data_object->hdf5_data_object)`                                                                                           |
| `int (u64b)`             | `int (u64b)`          | `H5Tget_size`                 | result of `H5Tget_size(hdf5_data_object->hdf5_data_object)`                                                                                            |
| `int (u64b)`             | `int (u64b)`          | `H5Tget_order`                | result of `H5Tget_order(hdf5_data_object->hdf5_data_object)`                                                                                           |
| `int (u64b)`             | `int (u64b)`          | `H5Tget_precision`            | result of `H5Tget_precision(hdf5_data_object->hdf5_data_object)`                                                                                       |
| `int (u64b)`             | `int (u64b)`          | `H5Tget_offset`               | result of `H5Tget_offset(hdf5_data_object->hdf5_data_object)`                                                                                          |
| `int (u64b)`             | `int (u64b)`          | `subdir_cadence_secs`         | Subdirectory cadence in seconds                                                                                                                        |
| `int (u64b)`             | `int (u64b)`          | `file_cadence_millisecs`      | File cadence in milliseconds                                                                                                                           |
| `int (u64b)`             | `int (u64b)`          | `sample_rate_numerator`       | Numerator to make the sample rate a rational number, in Hz                                                                                             |
| `int (u64b)`             | `int (u64b)`          | `sample_rate_denominator`     | Denominator to make the sample rate a rational number, in Hz                                                                                           |
| `bool`                   | `int`                 | `is_complex`                  | 1 if complex values, 0 if single valued.                                                                                                               |
| `int (u16b)`             | `int`                 | `num_subchannels`             | 1 or more subchannels in the file. The meaning of the different subchannels is not defined in the RF file, but may be in accompanying digital metadata |
| `bool`                   | `int`                 | `is_continuous`               | 1 if data is continuous, 0 if not                                                                                                                      |
| `int (u64b)`\*           | `string`              | `epoch`                       | start time of sample 0 (time since Unix epoch: 1970-01-01 UTC midnight)                                                                                |
| `string`                 | `string`              | `digital_rf_time_description` | a text description of how time is stored in this format                                                                                                |
| `string`                 | `string`              | `digital_rf_version`          | a version number of the Hdf5 RF format. Now 2.3.                                                                                                       |

### Optional Attributes

The 4 additional metadata attributes returned when sample is not `None` are:

| Ideal Type (min bit rep) | Type from docs / code | Name                 | Description                                                                        |
| ------------------------ | --------------------- | -------------------- | ---------------------------------------------------------------------------------- |
| `int (u64b)`             | `int (u64b)`          | `sequence_num`       | running number from start of acquisition. used to identify missing files           |
| `int (u64b)`\*           | `int (u64b)`\*        | `init_utc_timestamp` | changes at each restart of the recorder; needed if leap seconds correction applied |
| `int (u64b)`\*           | `int (u64b)`\*        | `computer_time`      | computer time at creation of individual RF file. As seconds, from Unix epoch.      |
| `UUIDv4 (128b)`\**       | `string`\**           | `uuid_str`           | set independently at each restart of the recorder                                  |

+ \* **Number of bits in timestamps:** 64 bits should be enough from nanoseconds to seconds: `2^64` nanoseconds ~ 584.9 years (year 2554).
+ \** **UUID version:** It is not specified in the documentation as it is "user-defined", but UUIDv4 is the version actually generated by the [Python SDK](https://github.com/MITHaystack/digital_rf/blob/22b8b5f4aeac5297ba03618485bb8985828583b0/python/digital_rf/digital_rf_hdf5.py#L370). We should probably clear the ambiguity and make this version the expected one for validation purposes until we have a good reason to change it.

### Extended Digital RF Capture Attributes under SDS

Extended attributes that are not part of the first Digital-RF specification, but that SDS supports and indexes.

This list is based on the [DRF properties indexed by SDS](https://github.com/spectrumx/sds-code/blob/stable/gateway/sds_gateway/api_methods/utils/metadata_schemas.py).

> Note some of these are computed properties.

| Attribute            | Python Type     | Description                                                                              | Required |
| -------------------- | --------------- | ---------------------------------------------------------------------------------------- | -------- |
| `antenna_direction`  | `float`         | The direction of the antenna, in degrees.                                                | Yes      |
| `antenna`            | `str`           | The antenna used in the capture.                                                         | Yes      |
| `bandwidth`          | `int`           | The resolution bandwidth of the capture, in Hz.                                          | Yes      |
| `center_frequencies` | `list[float]`\* | The center frequencies of each of the capture's subchannels, in Hz.                      | Yes      |
| `end_bound`          | `int`           | Index of the last sample, given in the number of samples since the epoch                 | Yes      |
| `gain`               | `float`         | The gain of the capture, in dB.                                                          | Yes      |
| `indoor_outdoor`     | `str`           | Whether the capture was taken indoors or outdoors.                                       | Yes      |
| `span`               | `int`           | The span of the capture, in seconds.                                                     | Yes      |
| `start_bound`        | `int`           | Index of the first sample, given in the number of samples since the epoch                | Yes      |
| `center_freq`        | `int`           | The center frequency of the capture, in Hz. Consider using `center_frequencies` instead. | No       |
| `custom_attrs`       | `dict`          | Custom attributes of the capture - fields that are not in the schema.                    | No       |

\* Type matches its `numpy.float64` counterpart from the Digital-RF library, and it's stored as an array of doubles in OpenSearch.

## Data and Metadata

| Term           | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| RF files       | Files containing RF data, not only metadata e.g. `rf@1394368244.000.h5`. |
| Metadata files | Files containing only metadata i.e. `drf_properties.h5`.                 |
| Channel        | A group of RF files e.g. `ch0`.                                          |
| Subchannel     | Different data streams within an RF file.                                |

Besides the required and optional attributes with their types above, below are some other requirements for Digital-RF compatibility that may be useful for validation. Maybe we can think of them as individual assertions for tests:

> Items marked with 🛑 are more strict or less ambiguous versions of what is in the specification document.

1. RF files must have exactly two HDF5 datasets under the root level: `rf_data` and `rf_data_index` 🛑.
2. Metadata files must have only HDF5 attributes under the root level (no groups or datasets) 🛑.
3. The first sample in each RF HDF5 file will always have an entry in `rf_data_index`.
4. There will be an additional entry in `rf_data_index` when a data gap occurs.
5. For continuous data, the `rf_data_index` will have a single entry.
6. Data in `rf_data` may be of any type supported by HDF5, which include e.g. complex, floating point (up to 128b), and int.
7. HDF5 RF files are grouped by their channel in subdirectories with the channel name.
8. Compression levels must be between 0 and 9, inclusive.
9. When the continuous flag is enabled, then gapped data must not be passed in.
10. All subchannels (within a file) must have the same gaps.
11. The 15 required metadata attributes within an RF file must match the higher-level metadata file.
12. RF data must follow either the $N_{sc} \times N_{sf} \times 2$ or $N_{sc} \times N_{sf} \times 1$ shapes described in [HDF5 Layout](#hdf5-layout).
13. Files must not start with the `tmp.` prefix in order to be processed by SDS.

## Namespaces

The Digital-RF metadata format allows users to include optional metadata, but does not indicate nor enforce *how* they should add these custom metadata attributes.

As a consequence, Digital-RF mixes its own namespace with the users', preventing the format from reliably evolving over time.

We should be more strict about user-defined metadata before integrating it into SDS using one of the following strategies:

1. **Reserved prefix:** enforce Digital-RF metadata to start with a prefix e.g. `__drf_`. A similar approach is used by ArangoDB, where attributes starting with an underscore are reserved for system use.
2. **Hierarchical namespaces:** enforce custom metadata to be stored in a separate HDF5 group e.g. `/user/`.

## HDF5 Layout

> Copied and adapted from the original documentation. Credits to the documentation authors.

### RF File Layout

Each RF file contains the following elements:

+ `/rf_data`: $N_{sc} \times N_{sf} \times 2$ (when complex) or $N_{sc} \times N_{sf} \times 1$ (when single-valued) vector of data, where $N_{sc}$ is the number of subchannels, $N_{sf}$ is the samples per file. Data type can be any valid HDF5
data type.
+ `/rf_data_index`: $N \times 2$ `uint64`, mapping between local (starts at 0) and global sample indices. The first row is always the global sample index and 0, indicating the first sample in the file.
+ `/rf_data` dataset has the 19 attributes described in the previous section, 15 that match the high level `metadata.h5` file, and 4 that may vary between files in a channel.

### File Cadence

The HDF5 files are written in the following way:

`2014-03-30T12-00-00/rf@1396379502.000.h5`

A new subdirectory is created at first write. Its name is in the format `YYYY-MM-SSTHH-MM-SS`, where the timestamp `ts` is the largest for which `ts = subdirectory_cadence_seconds x N <= first_sample // sample_rate` is true, where `N` is an integer.

A new subdirectory will be created when:

`(next_sample / sample_rate) >= (subdirectory_cadence_seconds x (N + 1))`

The file name `rf@1396379502.000.h5` includes seconds and milliseconds since Unix epoch. The millisecond timestamp of every file is determined by the largest millisecond timestamp where `file_ms = file_cadence_millseconds x N <= first_sample // (sample_rate / 1000.0)`
is `true`, where `N` is an integer.

All following samples will be written to the same file until `first_sample // (sample_rate / 1000.0) >= file_cadence_millseconds x (N + 1)`. The maximum number of samples a file can hold is:

`max_samples = file_cadence_millisecs * (sample_rate / 1000.0)`

To ensure file boundaries and subdirectory boundaries line up, the "write" API requires `subdir_cadence_secs` and `file_cadence_millisecs` to be related by:

`(subdir_cadence_secs * 1000) % file_cadence_millisecs == 0`

Note that files that are being actively written to have the four characters `tmp.` prepended to their name, such as `tmp.rf@1396379502.000.h5`. When a new Hdf5 file is opened, the API will automatically rename the file to remove the `tmp.` characters. This renaming will also occur for the last file written when the close method is called. The reason for this special name for files being actively updated is to allow mirroring or backup scripts to determine which files are complete and which might change.

### Directory Layout

In order to structure the data, we will use the following type of namespace layout:

`<top_level_directory>/<channel_name>/2014-03-30T12-00-00/rf@1396379502.000.h5`

Where the basename of the top_level_directory has the recommended form `experiment_name-{timestamp}`. Here a timestamp with curly brackets is optional. In some cases it is nice to have (e.g., campaign type of recording), where are, in other cases, not wanted behavior (e.g., a ring buffer that you expect to always reside in some place).

Digital metadata is defined in a separate document, but the Digital-RF "read" api contains a call to read digital metadata if it's written in the directory: `<top_level_directory>/<channel_name>/metadata/`.

While not yet implemented, a future release will make it to make it easy to identify data in Digital-RF format by placing a file `README.digital_rf` is placed under `<top_level_directory>` This file would act as an identifier, as well as a description of the data format. It is permissible to start acquisitions into the same `<top_level_directory>/<channel_name>` directory
