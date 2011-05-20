#!/usr/bin/env python

######################################################################
# Software License Agreement (BSD License)
#
#  Copyright (c) 2010, Rice University
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the Rice University nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
######################################################################

# Author: Mark Moll

from math import sin, cos
try:
    from ompl import base as ob
    from ompl import control as oc
    from ompl import geometric as og
except:
    # if the ompl module is not in the PYTHONPATH assume it is installed in a
    # subdirectory of the parent directory called "py-bindings."
    from os.path import basename, abspath, dirname, join
    import sys
    sys.path.insert(0, join(dirname(dirname(abspath(__file__))),'py-bindings'))
    from ompl import base as ob
    from ompl import control as oc
    from ompl import geometric as og

def isStateValid(spaceInformation, state):
    # perform collision checking or check if other constraints are
    # satisfied
    return spaceInformation.satisfiesBounds(state)

def propagate(cspace, start, control, duration, state):
    state.setX( start.getX() + control[0] * duration * cos(start.getYaw()) )
    state.setY( start.getY() + control[0] * duration * sin(start.getYaw()) )
    state.setYaw(start.getYaw() + control[1] * duration)

def plan():
    # construct the state space we are planning in
    space = ob.SE2StateSpace()

    # set the bounds for the R^2 part of SE(2)
    bounds = ob.RealVectorBounds(2)
    bounds.setLow(-1)
    bounds.setHigh(1)
    space.setBounds(bounds)

    # create a control space
    cspace = oc.RealVectorControlSpace(space, 2)

    # set the bounds for the control space
    cbounds = ob.RealVectorBounds(2)
    cbounds.setLow(-.3)
    cbounds.setHigh(.3)
    cspace.setBounds(cbounds)

    # set the state propagation routine
    cspace.setPropagationFunction(propagate)

    # define a simple setup class
    ss = oc.SimpleSetup(cspace)
    ss.setStateValidityChecker(isStateValid)

    # create a start state
    start = ob.State(space)
    start().setX(-0.5);
    start().setY(0.0);
    start().setYaw(0.0);

    # create a goal state
    goal = ob.State(space);
    goal().setX(0.0);
    goal().setY(0.5);
    goal().setYaw(0.0);

    # set the start and goal states
    ss.setStartAndGoalStates(start, goal, 0.05)

    # attempt to solve the problem
    solved = ss.solve(20.0)

    if solved:
        # print the path to screen
        print "Found solution:", ss.getSolutionPath().asGeometric()

if __name__ == "__main__":
    plan()
