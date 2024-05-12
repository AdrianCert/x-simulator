# Welcome to MkDocs

This is the documentation for X-Simulator, a simulator of a computing system.

## The main components

* `the processor`
* `the memory`
* `the peripheral devices`

# Main Components Explanation
We will now proceed to give a brief presentation of the essential modules in this project.

### 1. The Procesor 

The role of a processor is to simulate the operations of a real-world processor. The processor is responsible for interpreting and executing program code, managing registers, accessing memory, and other tasks specific to data processing and instruction execution.

The ProcessorRegisters class in the code is responsible for managing the processor's registers within the simulator. Specifically, this class has the following functionalities and responsibilities:

* Initializes a memory area for the processor's registers.
* Creates and stores ProcessorRegister objects for each register of the processor.
* Associates each register with a memory area within the processor's memory.
* Provides methods for accessing and modifying values in the registers.
* Handles unallocated memory in case the memory space is insufficient for all registers.
In essence, the ProcessorRegisters class acts as a manager for all of the processor's registers, providing a level of abstraction that facilitates read and write operations to the individual registers of the processor.

In our simulator, several instructions are defined and each of them performs some specific operation.
The operations are: 'ADD' (addition), 'SUB' (substraction), 'MUL' (multiplication), 'DIV' (division) and 'MOV' that performs data transfer between registers or between a constant and a register.
### 2. The Memory

The Memory component in the project defines two main classes, Memory and MemoryView, which are fundamental for managing and simulating memory within a computer system simulator. Here's a more detailed description of the functionalities and roles of these classes:

* The "read" and "write" methods of the "Memory" class allow data to be read and written to certain addresses in memory. These methods validate the specified addresses and handle the appropriate endianess.

* The view method of the Memory class allows the creation of MemoryView objects, which represent subsets of the main memory. These subviews can be used to access and manipulate specific portions of system memory.

```python
        def view(self, address: int, size: int = 1) -> "Memory":
            self.validate_address(address, size)
            memory_view = MemoryView(self, address, size)
            self.sub_views[address : address + size] = memory_view
            return memory_view
```

* The validate_address method of the Memory class has the role of checking whether a specified address is valid within the memory space of the Memory object. This method receives two arguments: address (the address on which the validation is done) and optionally size (the size of the data to be accessed at that address).

```python
    def validate_address(self, address: int, size: int = 1):
        if address < 0 or address >= self.size:
            raise ValueError(f"Invalid address: {address}")
        if address + size > self.size:
            raise ValueError(f"Invalid address range: {address} - {address + size}")
```

   



