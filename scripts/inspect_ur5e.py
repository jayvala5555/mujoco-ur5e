import numpy as np
import argparse
from pathlib import Path

import mujoco


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_MODEL = (
    PROJECT_ROOT
    / "third_party/mujoco_menagerie/universal_robots_ur5e/scene.xml"
)


def inspect_model(xml_path: Path):
    print(f"\nLoading model: {xml_path}")

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    mujoco.mj_forward(model, data)

    print("\n========== MODEL SUMMARY ==========")
    print(f"MuJoCo version : {mujoco.__version__}")
    print(f"Bodies         : {model.nbody}")
    print(f"Joints         : {model.njnt}")
    print(f"Actuators      : {model.nu}")
    print(f"Position vars  : {model.nq}")
    print(f"Velocity vars  : {model.nv}")
    print(f"Simulation dt  : {model.opt.timestep}")

    print("\n========== JOINTS ==========")

    for joint_id in range(model.njnt):
        name = mujoco.mj_id2name(
            model, mujoco.mjtObj.mjOBJ_JOINT, joint_id
        )
        joint_type = model.jnt_type[joint_id]
        qpos_address = model.jnt_qposadr[joint_id]
        dof_address = model.jnt_dofadr[joint_id]

        print(
            f"{joint_id}: {name} | "
            f"type={joint_type} | "
            f"qpos={qpos_address} | "
            f"dof={dof_address}"
        )

    print("\n========== ACTUATORS ==========")

    for actuator_id in range(model.nu):
        name = mujoco.mj_id2name(
            model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_id
        )
        print(
            f"{actuator_id}: {name} | "
            f"control range={np.rad2deg(model.actuator_ctrlrange[actuator_id])}"
        )

    print("\n========== INITIAL STATE ==========")
    print("qpos:", data.qpos)
    print("qvel:", data.qvel)

    return model, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xml",
        type=Path,
        default=DEFAULT_MODEL,
        help="Path to the MuJoCo XML model",
    )
    parser.add_argument(
        "--viewer",
        action="store_true",
        help="Open the interactive MuJoCo viewer",
    )

    args = parser.parse_args()

    model, data = inspect_model(args.xml)

    if args.viewer:
        print("\nLaunching MuJoCo viewer. Close the window to exit.")
        import mujoco.viewer

        mujoco.viewer.launch(model, data)


if __name__ == "__main__":
    main()
