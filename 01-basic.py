from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

# Here we setup the board. The prebuilt X86DemoBoard allows for
Full-System X86
# simulation.
board = X86DemoBoard()

workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
board.set_workload(workload)

def exit_event_handler():
  print("First exit: kernel booted")
  yield False # gem5 is now executing systemd startup
  print("Second exit: Started `after_boot.sh` script")
  # The after_boot.sh script is executed after the kernel and systemd
have
  # booted.
  yield False # gem5 is now executing the `after_boot.sh` script
  print("Third exit: Finished `after_boot.sh` script")
  # The after_boot.sh script will run a script if it is passed via
  # m5 readfile. This is the last exit event before the simulation
exits.
  yield True


simulator = Simulator(
  board=board,
  on_exit_event={
     # Here we want override the default behavior for the first m5
exit
     # exit event.
     ExitEvent.EXIT: exit_event_handler()
  },
)
simulator.rum()
