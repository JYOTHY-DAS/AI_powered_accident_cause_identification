import pyopencl as cl
import numpy as np

# Create OpenCL context
platform = cl.get_platforms()[0]  # Select first platform (AMD)
device = platform.get_devices()[0]  # Select first GPU device
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Define a simple OpenCL kernel (adds two arrays)
program_src = """
__kernel void add_arrays(__global const float* a, __global const float* b, __global float* result) {
    int gid = get_global_id(0);
    result[gid] = a[gid] + b[gid];
}
"""
program = cl.Program(context, program_src).build()

# Create input data
size = 10
a = np.random.rand(size).astype(np.float32)
b = np.random.rand(size).astype(np.float32)
result = np.empty_like(a)

# Allocate device memory
mf = cl.mem_flags
a_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
result_buf = cl.Buffer(context, mf.WRITE_ONLY, result.nbytes)

# Execute the OpenCL kernel
program.add_arrays(queue, a.shape, None, a_buf, b_buf, result_buf)

# Copy result back to host
cl.enqueue_copy(queue, result, result_buf)

print("Array A:", a)
print("Array B:", b)
print("Result:", result)
