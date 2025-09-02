#!/bin/bash

# 1 Job (2G)
echo ">>> Starting 1 Job (2G)..."
fio --name=smallfile_1_job \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=2G \
    --direct=1 \
    --numjobs=1 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_1_job.json \
    --output-format=json
echo "<<< Finished 1 Job (2G)"

# 2 Jobs (2G)
echo ">>> Starting 2 Jobs (2G)..."
fio --name=smallfile_2_jobs \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=2G \
    --direct=1 \
    --numjobs=2 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_2_jobs.json \
    --output-format=json
echo "<<< Finished 2 Jobs (2G)"

# 3 Jobs (2G)
echo ">>> Starting 3 Jobs (2G)..."
fio --name=smallfile_3_jobs \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=2G \
    --direct=1 \
    --numjobs=3 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_3_jobs.json \
    --output-format=json
echo "<<< Finished 3 Jobs (2G)"

# 4 Jobs (2G)
echo ">>> Starting 4 Jobs (2G)..."
fio --name=smallfile_4_jobs \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=2G \
    --direct=1 \
    --numjobs=4 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_4_jobs.json \
    --output-format=json
echo "<<< Finished 4 Jobs (2G)"

# 1 Job (5G)
echo ">>> Starting 1 Job (5G)..."
fio --name=smallfile_1_job_5g \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=5G \
    --direct=1 \
    --numjobs=1 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_1_job_5g.json \
    --output-format=json
echo "<<< Finished 1 Job (5G)"

# 2 Jobs (5G)
echo ">>> Starting 2 Jobs (5G)..."
fio --name=smallfile_2_jobs_5g \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=5G \
    --direct=1 \
    --numjobs=2 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_2_jobs_5g.json \
    --output-format=json
echo "<<< Finished 2 Jobs (5G)"

# 3 Jobs (5G)
echo ">>> Starting 3 Jobs (5G)..."
fio --name=smallfile_3_jobs_5g \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=5G \
    --direct=1 \
    --numjobs=3 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_3_jobs_5g.json \
    --output-format=json
echo "<<< Finished 3 Jobs (5G)"

# 4 Jobs (5G)
echo ">>> Starting 4 Jobs (5G)..."
fio --name=smallfile_4_jobs_5g \
    --filename=/home/nvidia/nvme/test_file \
    --ioengine=libaio \
    --rw=write \
    --bsrange=128k-10m \
    --size=5G \
    --direct=1 \
    --numjobs=4 \
    --iodepth=32 \
    --time_based --runtime=60 \
    --group_reporting \
    --output=smallfile_4_jobs_5g.json \
    --output-format=json
echo "<<< Finished 4 Jobs (5G)"

echo "=== All tests completed ==="

