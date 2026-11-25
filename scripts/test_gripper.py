from pathlib import Path
import time

import mujoco
import mujoco.viewer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "assets" / "workcell.xml"


def get_id(model, object_type, name):
    object_id = mujoco.mj_name2id(model, object_type, name)
    if object_id < 0:
        raise ValueError(f"Object not found: {name}")
    return object_id


def main():
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    # get home keyframe id (home keyframe = some default position for robot e.g. for humanoid standing position actuator commands)
    home_id = get_id(model, mujoco.mjtObj.mjOBJ_KEY, "home")
    mujoco.mj_resetDataKeyframe(model, data, home_id)
    mujoco.mj_forward(model, data)

    left_id = get_id(
        model, mujoco.mjtObj.mjOBJ_ACTUATOR, "left_finger_actuator"
    )
    right_id = get_id(
        model, mujoco.mjtObj.mjOBJ_ACTUATOR, "right_finger_actuator"
    )

    print("Gripper test starting.")
    print("Controls: open -> close -> open")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        with viewer.lock():
            viewer.cam.azimuth = 179.41
            viewer.cam.elevation = -23.65
            viewer.cam.distance = 1.36
            viewer.cam.lookat[:] = [0.3941, 0.0242, 0.6667] # Adjust [x, y, z] to center on your table/robot

        for label, command in [
            ("OPEN", 0.0),
            ("CLOSE", 0.015),
            ("OPEN", 0.0),
        ]:
            print(f"\nGripper: {label}")

            data.ctrl[left_id] = command
            data.ctrl[right_id] = command

            for _ in range(1000):
                mujoco.mj_step(model, data)
                viewer.sync()
                time.sleep(model.opt.timestep)

            print(
                "Finger positions:",
                data.qpos[
                    model.jnt_qposadr[
                        get_id(model, mujoco.mjtObj.mjOBJ_JOINT,
                               "left_finger_joint")
                    ]
                ],
                data.qpos[
                    model.jnt_qposadr[
                        get_id(model, mujoco.mjtObj.mjOBJ_JOINT,
                               "right_finger_joint")
                    ]
                ],
            )

        print("\nGripper test complete. Close the viewer to exit.")
        while viewer.is_running():
            viewer.sync()
            time.sleep(0.02)


if __name__ == "__main__":
    main()