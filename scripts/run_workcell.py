from pathlib import Path

import mujoco
import mujoco.viewer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "assets" / "workcell.xml"


def get_id(model, object_type, name):
    object_id = mujoco.mj_name2id(model, object_type, name)

    if object_id < 0:
        raise ValueError(f"Could not find model object: {name}")

    return object_id


def main():
    print(f"Loading workcell: {MODEL_PATH}")

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    # Start from the original UR5e home keyframe.
    home_id = get_id(
        model,
        mujoco.mjtObj.mjOBJ_KEY,
        "home",
    )
    mujoco.mj_resetDataKeyframe(model, data, home_id)
    mujoco.mj_forward(model, data)

    print("\n========== WORKCELL SUMMARY ==========")
    print("MuJoCo version:", mujoco.__version__)
    print("Bodies:", model.nbody)
    print("Joints:", model.njnt)
    print("Actuators:", model.nu)
    print("Geometries:", model.ngeom)
    print("Cameras:", model.ncam)
    print("Simulation timestep:", model.opt.timestep)

    print("\n========== REQUIRED OBJECTS ==========")

    required_objects = {
        "red_cube": (mujoco.mjtObj.mjOBJ_BODY, "red_cube"),
        "worktable": (mujoco.mjtObj.mjOBJ_BODY, "worktable"),
        "placement_tray": (
            mujoco.mjtObj.mjOBJ_BODY,
            "placement_tray",
        ),
        "camera": (
            mujoco.mjtObj.mjOBJ_CAMERA,
            "workcell_camera",
        ),
    }

    for label, (object_type, name) in required_objects.items():
        object_id = get_id(model, object_type, name)
        print(f"{label}: ID {object_id}")

    cube_id = get_id(
        model, mujoco.mjtObj.mjOBJ_BODY, "red_cube"
    )

    print("\n========== CUBE INITIAL POSITION ==========")
    print("Position:", data.xpos[cube_id].copy())

    print("\n========== ROBOT HOME STATE ==========")
    print("Joint positions:", data.qpos[:6])

    print("\nLaunching workcell viewer...")
    print("Close the viewer window to exit.")

    mujoco.viewer.launch(model, data)


if __name__ == "__main__":
    main()