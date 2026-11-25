# AI-Enabled Robotic Pick-and-Place

MuJoCo VLA-UR6e

Project goal: Build an AI-enabled robotic pick-and-place system in which a Vision-Language-Action (VLA) model understands a natural-language instruction, observes the robot's environment, and generates actions to control a simulated UR5e robot.

Core task: Given the instruction "Pick up the red cube and place it in the tray", the robot should perceive, pick, transport, and place the cube autonomously.

## Overall Workflow

1. Simulation environment \
MuJoCo + UR5e + workcell + camera

2. Robot control \
Kinematics + trajectory planning + gripper + safety

3. Demonstration generation \
Expert controller + observations + actions + language

4. VLA development \
SmolVLA pretrained model + UR5e embodiment adaptation + fine-tuning

5. Autonomous execution \
Language + image + robot state → predicted action chunks → UR5e

6. Evaluation \
Success rate + execution time + robustness + failure analysis

## Technical Stack

| Component | Technology |
|---|---|
Physics simulation | MuJoCo 3.2.2
Robot | Universal Robots UR5e
Robot model | Google DeepMind MuJoCo Menagerie
Programming | Python, C++ where useful
Vision | RGB camera, OpenCV
Robot control | MuJoCo actuators, kinematics, trajectory planning
Demonstration dataset | LeRobot dataset format
VLA | Hugging Face SmolVLA
Deep learning | PyTorch
Training | Google Colab free GPU, if available
Version control | Git and GitHub

## Checklist

- [X] Workspace setup.
- [X] Add UR5e Arm model.
- [X] Workcell (Environment) setup.
- [ ] Robot manipulation. 

