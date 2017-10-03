# Kawasaki experimental

Experimental packages for Kawasaki manipulators within [ROS-Industrial][].
See the [ROS wiki][] page for more information.


## Contents

This repository contains packages that will (eventually) be migrated to a [kawasaki][] repository after they have received sufficient testing.
The contents of these packages are subject to change, without prior notice.
Any available APIs are to be considered unstable and are not guaranteed to be complete and / or functional.


## Compatibility

These packages have been created on Ubuntu Trusty and ROS Indigo, but are expected to work under Xenial and Kinetic as well.
Some dependencies may have to be build from sources on newer OS/ROS combinations though.


## Workspace setup

To setup a workspace and start using the packages, follow the below steps (make sure to have installed basic ROS and [catkin_tools][]):

```bash
$ source /opt/ros/$distro/setup.bash
$ mkdir -p $HOME/kawasaki_ws/src
$ cd $HOME/kawasaki_ws/src
$ git clone https://github.com/gavanderhoorn/kawasaki_experimental.git
$ cd $HOME/kawasaki_ws
$ rosdep update
$ rosdep install --from-paths src --ignore-src
# follow instructions and let it install dependencies
$ catkin build
```

After a successful build, activate the workspace with `source devel/setup.bash`.



[ROS-Industrial]: http://wiki.ros.org/Industrial
[ROS wiki]: http://wiki.ros.org/kawasaki_experimental
[kawasaki]: https://github.com/ros-industrial/kawasaki
[catkin_tools]: https://catkin-tools.readthedocs.io/en/latest/installing.html
