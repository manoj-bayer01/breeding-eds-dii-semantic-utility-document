# Data Architecture Overview

*Last updated: 2025-09-18 15:39:34*


## Data Model Diagram

```mermaid
graph TB
    capacity_request["Capacity Request"]
    capacity_request --> |contains| capacity_request_data{Data}
    capacity_request2["Capacity Request3"]
    capacity_request2 --> |contains| capacity_request2_data{Data}
    capacity_request -.-> |one_to_many| experiment_sets_entries
    capacity_request -.-> |one_to_many| experiment_sets_entries2
    capacity_request["Capacity Request"]
    capacity_request --> |contains| capacity_request_data{Data}
    capacity_request2["Capacity Request3"]
    capacity_request2 --> |contains| capacity_request2_data{Data}
    capacity_request -.-> |one_to_many| experiment_sets_entries
    capacity_request -.-> |one_to_many| experiment_sets_entries2
    capacity_request["Capacity Request"]
    capacity_request --> |contains| capacity_request_data{Data}
    capacity_request2["Capacity Request3"]
    capacity_request2 --> |contains| capacity_request2_data{Data}
    capacity_request -.-> |one_to_many| experiment_sets_entries
    capacity_request -.-> |one_to_many| experiment_sets_entries2
    capacity_request["Capacity Request"]
    capacity_request --> |contains| capacity_request_data{Data}
    capacity_request2["Capacity Request3"]
    capacity_request2 --> |contains| capacity_request2_data{Data}
    capacity_request -.-> |one_to_many| experiment_sets_entries
    capacity_request -.-> |one_to_many| experiment_sets_entries2
```

## Components by File

### Semantic Design Template Semantic

**Data Cubes:**
- `capacity_request`: Capacity Request
- `capacity_request2`: Capacity Request3

**Relationships:**
- `experiment_sets_entries` (one_to_many)
- `experiment_sets_entries2` (one_to_many)

**Dimensions:** 1 defined

**Measures:** 1 defined

### Semantic Output

**Data Cubes:**
- `capacity_request`: Capacity Request
- `capacity_request2`: Capacity Request3

**Relationships:**
- `experiment_sets_entries` (one_to_many)
- `experiment_sets_entries2` (one_to_many)

**Dimensions:** 1 defined

**Measures:** 1 defined

### Semantic Updated

**Data Cubes:**
- `capacity_request`: Capacity Request
- `capacity_request2`: Capacity Request3

**Relationships:**
- `experiment_sets_entries` (one_to_many)
- `experiment_sets_entries2` (one_to_many)

**Dimensions:** 1 defined

**Measures:** 1 defined

### Test Output

**Data Cubes:**
- `capacity_request`: Capacity Request
- `capacity_request2`: Capacity Request3

**Relationships:**
- `experiment_sets_entries` (one_to_many)
- `experiment_sets_entries2` (one_to_many)

**Dimensions:** 1 defined

**Measures:** 1 defined
