# Resource Monotonicity of DRF

DRF does not satisfy the property of resource monotonicity. Resource monotonicity means that if more resources are added to the system, none of the allocations of the existing users should decrease. In other words, adding more resources to the system should not negatively impact the allocation of any user​.

## Setup

```bash
pip3 install -r requirements.txt
```

## Scenario 1

```bash
python3 main.py --num_cpus 9 --num_mems 18
```

Result

```
Resource allocation:
User A: 3.0 CPUs and 12.0 GB of memory
User B: 6.0 CPUs and 2.0 GB of memory
```

## Scenario 2 (2x Memory)

```bash
python3 main.py --num_cpus 9 --num_mems 36
```

Result

```
Resource allocation:
User A: 3.0 CPUs and 12.0 GB of memory
User B: 3.0 CPUs and 1.0 GB of memory
```

B's resource allocation decreased even after an increase of memory.