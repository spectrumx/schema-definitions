# RadioHound Metadata Format under SDS

The RadioHound metadata format is a JSON format created at the Wireless Institute at the University of Notre Dame to address the storage of [periodograms](https://en.wikipedia.org/wiki/Periodogram) and related metadata.

## Human-readable specification

For a machine-readable schema, see the [v0 schema](./v0/schema.json).

### Top-level attributes

#### Required top-level attributes

| Attribute     | Required? | Ideal Type (min bit or length representation)          | Type in `.rh.json` for storage | Description                                                                                          |
| ------------- | --------- | ------------------------------------------------------ | ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `data`        | True      | base64 string (unbound)                                | str                            | The periodogram data as a base64-encoded numpy array                                                 |
| `gain`        | True      | float (32b)                                            | number                         | The gain in dB                                                                                       |
| `latitude`    | True      | float (32b)                                            | number                         | The latitude where the data was captured, in decimal degrees                                         |
| `longitude`   | True      | float (32b)                                            | number                         | The longitude where the data was captured, in decimal degrees                                        |
| `mac_address` | True      | str (12 chars)                                         | str                            | The MAC address of the device, without separators                                                    |
| `metadata`    | True      | dict (unbound)                                         | object                         | The metadata of the data ([see attributes](#attributes-in-metadata))                                 |
| `sample_rate` | True      | int (64b)                                              | number                         | The sample rate of the capture, in Hz                                                                |
| `short_name`  | True      | str (<=255 chars)                                      | str                            | The short name of the device                                                                         |
| `timestamp`   | True      | ISO 8601 with timezone (unbound, generally <=35 chars) | str                            | Timestamp of the capture start, as ISO 8601 with timezone information                                |
| `type`        | True      | str (<=255 chars)                                      | str                            | The [numpy-compatible dtype](https://numpy.org/doc/stable/user/basics.types.html) of `data` elements |
| `version`     | True      | str (<=255 chars)                                      | str                            | Version of the RadioHound data format, defaults to v0 when missing                                   |

#### Optional top-level attributes

| Attribute           | Required? | Ideal Type (min bit or length representation) | Type in `.rh.json` for storage | Description                                                                                  |
| ------------------- | --------- | --------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| `altitude`          | False     | float (32b)                                   | number                         | The altitude where the data was captured, in meters                                          |
| `batch`             | False     | int (64b)                                     | number                         | Can be used to group scans together                                                          |
| `center_frequency`  | False     | float (32b)                                   | number                         | The center frequency of the capture, calculated as the mean of the start and end frequencies |
| `custom_fields`     | False     | dict (unbound)                                | object                         | Custom fields that are not part of the standard schema                                       |
| `hardware_board_id` | False     | str (<=255 chars)                             | str                            | The hardware board ID of the device capturing the data                                       |
| `hardware_version`  | False     | str (<=255 chars)                             | str                            | The hardware version of the device capturing the data                                        |
| `software_version`  | False     | str (<=255 chars)                             | str                            | The software version of the device capturing the data                                        |

### Attributes in `metadata`

| Attribute            | Required? | Ideal Type (min bit or length representation) | Type in `.rh.json` for storage | Description                                                        |
| -------------------- | --------- | --------------------------------------------- | ------------------------------ | ------------------------------------------------------------------ |
| `metadata.data_type` | True      | str (<=255 chars)                             | str                            | The category of this capture: Only `periodogram` is valid in `v0`. |
| `metadata.fmax`      | True      | int (64b)                                     | number                         | The maximum frequency in the sample                                |
| `metadata.fmin`      | True      | int (64b)                                     | number                         | The minimum frequency in the sample                                |
| `metadata.gps_lock`  | True      | bool (1b)                                     | bool                           | Whether a GPS satellite lock is successfully obtained              |
| `metadata.nfft`      | True      | int (64b)                                     | number                         | Number of FFT bins, recommended to be a power of 2                 |
| `metadata.scan_time` | True      | float (32b)                                   | number                         | The time taken to scan this sample, in seconds                     |

### Deprecated attributes

The following attributes may appear in files before this spec and are deprecated in `v0`. Their data will be dropped from new `v0` files:

| Deprecated in version | Attribute         | Ideal Type (min bit or length representation) | Type in `.rh.json` for storage |
| --------------------- | ----------------- | --------------------------------------------- | ------------------------------ |
| `v0`                  | `metadata.xcount` | int (64b)                                     | number                         |
| `v0`                  | `metadata.xstart` | int (64b)                                     | number                         |
| `v0`                  | `metadata.xstop`  | int (64b)                                     | number                         |
| `v0`                  | `suggested_gain`  | float (32b)                                   | number                         |
| `v0`                  | `uncertainty`     | int (32b)                                     | number                         |

### Moved attributes

The following attributes may appear in files before this spec and are moved in `v0`. Their data will be renamed when serializing new `v0` files:

| Moved in version | Previous Name            | New Name                          | Ideal Type (min bit or length representation) | Type in `.rh.json` for storage | Description                                              |
| ---------------- | ------------------------ | --------------------------------- | --------------------------------------------- | ------------------------------ | -------------------------------------------------------- |
| `v0`             | `requested.fmin`         | `custom_fields.requested.fmin`    | int (64b)                                     | number                         | The minimum frequency requested for the sample, in Hz    |
| `v0`             | `requested.fmax`         | `custom_fields.requested.fmax`    | int (64b)                                     | number                         | The maximum frequency requested for the sample, in Hz    |
| `v0`             | `requested.span`         | `custom_fields.requested.span`    | int (64b)                                     | number                         | The frequency span requested for the sample, in Hz       |
| `v0`             | `requested.rbw`          | `custom_fields.requested.rbw`     | int (64b)                                     | number                         | The resolution bandwidth requested for the sample, in Hz |
| `v0`             | `requested.samples`      | `custom_fields.requested.samples` | int (64b)                                     | number                         | The number of samples requested for the sample           |
| `v0`             | `requested.gain`         | `custom_fields.requested.gain`    | float (32b)                                   | number                         | The gain requested for the sample, in dB                 |
| `v0`             | `metadata.archiveResult` | `metadata.archive_result`         | bool (1b)                                     | bool                           | Whether the data was archived                            |

## Specification changelog

### `v0`

[Generated schema](./v0/schema.json).

1. Formalized data attributes, their types, and requiredness.
2. Enforcing timezone information in the `timestamp` field writes. Missing timezones will be assumed to be UTC on read.
3. Added `version` to top-level to have some backwards compatibility, starting as `v0` and incrementing as `v1`, ..., `vn`.
4. Established deprecated and moved attributes.
    When writing new files, deprecated ones will be dropped and moved attributes will be renamed.

## Adding VS Code support

Add the following user settings to `settings.json`:

```jsonc
"": {
    // ...
    "*.rh": "json",
    // ...
}
// ...
"json.schemas": [
    // ...
    {
        "fileMatch": [
            "*.rh",
            "*.rh.json"
        ],
        "url": "https://json.schemastore.org/radiohound-v0.json"
    },
    // ...
]
```
