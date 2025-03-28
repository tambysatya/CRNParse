
from DiffExpr import *
import libsbml
import numpy as np
import torch

def run(filename, targetname, ts, t0=0, dt0=0.1):
    mdl = libsbml.readSBML(filename).getModel()
    system = DiffEqSystem(mdl)
    y0, params = system.getY0()
    traj = system.getTrajectory(y0,params,ts, t0=t0, dt0=dt0)
    print (traj)
    traj = torch.tensor(np.array(traj))
    torch.save(traj, targetname)
    return traj


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="the sbml file to be processed.", required=True)
    parser.add_argument("-ts", "--times", help="time points", nargs="+",type=float, required=True)
    parser.add_argument("-o", "--output_file", help="where to store the differential equations system.", required=True)
    parser.add_argument("-t0", "--initial_time", help="initial time point",type=float, default=0)
    parser.add_argument("-dt0", "--initial_time_step", help="initial time step",type=float, default=0.1)

    args = parser.parse_args()
    print(args)
    run(args.input_file, args.output_file, args.times, t0=args.initial_time, dt0=args.initial_time_step)


