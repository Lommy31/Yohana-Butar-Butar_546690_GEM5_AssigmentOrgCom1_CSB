# should be aligned with ../run_ubuntu.py
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import (
    SimpleProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource, Resource,
DiskImageResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
from gem5.coherence_protocol import CoherenceProtocol
import m5
# This runs a check to ensure the gem5 binary is compiled to X86 and to
the
# MESI Two Level coherence protocol.
requires(
    isa_required=ISA.X86,
    kvm_required=True,
)

from gem5.components.memory import SingleChannelDDR4_2400
memory = SingleChannelDDR4_2400(size="3GB")

# Here we setup the processor.
from gem5.components.processors.simple_switchable_processor import
SimpleSwitchableProcessor
processor = SimpleProcessor(
    cpu_type = CPUTypes.KVM,
    num_cores = 1,
    isa = ISA.X86
)
from gem5.components.cachehierarchies.classic.no_cache import NoCache
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=NoCache(),
)

command = "cd ~/experiment/testops;" + \
"echo '12345' | sudo -E -S ./01-annotate-this;"
board.set_kernel_disk_workload(
     kernel=Resource("x86-linux-kernel-5.4.0-105-generic",),

disk_image=DiskImageResource(local_path="imagebuild/disk-image-ubuntu-24
-041/x86-ubuntu-24-04-gapbs"),
    readfile_contents=command,
    kernel_args=[
        "earlyprintk=ttyS0",
        "console=ttyS0",
        "lpj=7999923",
        "root=/dev/sda2",
        "no_systemd=true",
      ],
)
num_run = 0
def workbegin_handler():
    print("Work begin")
    m5.checkpoint("cpt01")
    return True
def workend_handler():
    print("Done with the workload")
    return False
def exit_event_handler():
    print('first exit event: Kernel booted')
    yield False
    print('second exit event: In after boot')
    yield False
    yield False
simulator = Simulator(
    board=board,
    on_exit_event= {
       ExitEvent.WORKBEGIN: workbegin_handler,
       ExitEvent.EXIT: exit_event_handler(),
       ExitEvent.WORKEND: workend_handler
    },
#
)
simulator.run()                             
