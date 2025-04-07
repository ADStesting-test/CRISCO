# Generating Critical Test Scenarios for Autonomous Driving Systems via Influential Behavior Patterns

paper link: https://dl.acm.org/doi/pdf/10.1145/3551349.3560430

This project contains the implementation of CRISCO.

The generation approach requires the following dependencies to run:

	1. SORA-SVL simulator: https://github.com/YuqiHuai/SORA-SVL
	2. Apollo autonomous driving platform: https://github.com/ApolloAuto/apollo

# Prerequisites

* A 8-core processor and 16GB memory minimum
* Ubuntu 20.04 or later
* Python 3.8.10 or higher
* NVIDIA graphics card: NVIDIA proprietary driver (>=455.32) must be installed
* CUDA upgraded to version 11.1 to support Nvidia Ampere (30x0 series) GPUs
* Docker-CE version 19.03 and above
* NVIDIA Container Toolkit

# Requirements

Install LGSVL PythonAPI (pip3 install): https://github.com/lgsvl/PythonAPI

Version: SVL 2021.3

Other requirements: see in requirements.txt

# Apollo - A high performance, flexible architecture which accelerates the development, testing, and deployment of Autonomous Vehicles

Website of Apollo: https://apollo.auto/

Installation of Apollo 7.0: https://gitee.com/ApolloAuto/apollo/tree/v7.0.0

map: please put the "SanFrancisco-bin" in the map folder of Apollo (modules/map/data)

# Run
To generate critical test scenarios, start the simulator and Apollo, and then:

``
run generate_critical_scenarios.py in CRISCO, following the parameter: --r <the road type that you want to test the ADS on>
``

The road type can be: straight road, crossing, T-junction.

The safety-violation scenarios are recorded in the folder: safety_violation_scenarios.
To re-run a safety-violation scenario:

``
run reproduce_safety_violation.py in CRISCO, following the parameter: --r <your scenario description file name> --s <the safety-violation scenario name> --w <the re-run mechanism>
``

``
--w replay: reproduce the safety violations without connecting to Apollo; --w retest: re-execute the scenario to test the Apollo again
``


