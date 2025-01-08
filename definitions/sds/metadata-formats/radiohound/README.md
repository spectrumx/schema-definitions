# RadioHound Metadata Format under SDS

The RadioHound metadata format was created at the Wireless Institute at the University of Notre Dame to address the storage of [periodograms](https://en.wikipedia.org/wiki/Periodogram) and related metadata. The format is based on SigMF and is used in the RadioHound software.

## Format description

### Top-level attributes

| Attribute       | Required? | Ideal Type (min bit or length representation)          | Type in `.rh` (JSON) - for storage | Description                                                                                          |
| --------------- | --------- | ------------------------------------------------------ | ---------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `data`          | True      | base64 string (unbound)                                | str                                | The periodogram data as a base64-encoded numpy array                                                 |
| `gain`          | True      | float (32b)                                            | number                             | The gain in dB                                                                                       |
| `mac_address`   | True      | str (12 chars)                                         | str                                | The MAC address of the device without separators                                                     |
| `sample_rate`   | True      | int (64b)                                              | number                             | The sample rate of the data                                                                          |
| `short_name`    | True      | str (<=255 chars)                                      | str                                | The short name of the device                                                                         |
| `timestamp`     | True      | ISO 8601 with timezone (unbound, generally <=35 chars) | str                                | The timestamp of the data                                                                            |
| `type`          | True      | str (<=255 chars)                                      | str                                | The [numpy-compatible dtype](https://numpy.org/doc/stable/user/basics.types.html) of `data` elements |
| `version`       | True      | str (<=255 chars)                                      | str                                | The version of the metadata format                                                                   |
| `custom_fields` | False     | dict (unbound)                                         | object                             | Custom fields set by the writer                                                                      |

### Attributes in `metadata`

| Attribute            | Ideal Type (min bit or length representation) | Type in `.rh` (JSON) for storage | Description                                                                            |
| -------------------- | --------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------- |
| `metadata`           | dict (unbound)                                | object                           | The metadata of the data                                                               |
| `metadata.data_type` | str (<=255 chars)                             | str                              | The category of this capture: Only `periodogram` is valid in `v0`.                     |
| `metadata.fmax`      | int (64b)                                     | number                           | The maximum frequency in the sample                                                    |
| `metadata.fmin`      | int (64b)                                     | number                           | The minimum frequency in the sample                                                    |
| `metadata.gps_lock`  | bool (1b)                                     | bool                             | Whether device coordinates are set and locked (e.g. when satellites are not reachable) |
| `metadata.nfft`      | int (64b)                                     | number                           | The number of points in the FFT                                                        |
| `metadata.scan_time` | float (32b)                                   | number                           | The time taken to scan this sample, in seconds                                         |
| `metadata.xcount`    | int (64b)                                     | number                           | The number of points in the periodogram                                                |
| `metadata.xstart`    | int (64b)                                     | number                           | The start frequency of the periodogram                                                 |
| `metadata.xstop`     | int (64b)                                     | number                           | The stop frequency of the periodogram                                                  |

## Specification changelog

### `v0`

1. Formalized data attributes, their types, and requiredness.
2. Enforcing timezone information in the `timestamp` field writes. Missing timezones will be assumed to be UTC on read.
3. Added `version` to top-level to have some backwards compatibility, starting as "v0" and incrementing as "v1", ..., "vn".

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
            "*.rh"
        ],
        "url": "https://raw.githubusercontent.com/spectrumx/schema-definitions/refs/heads/master/definitions/sds/metadata-formats/radiohound/v0/schema.json"
    },
    // ...
]
```
