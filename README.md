# caddy_ai2_ros2_description

**Autores:** Ricardo (rinese89), Rafael Carbonell Lázaro (racarla96), Claude Sonnet (Anthropic)  
**Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

Paquete de descripción del robot agrícola Caddy AI2: vehículo de 4 ruedas con geometría Ackermann (dirección delantera, tracción trasera). Fuente única de verdad para la geometría, parámetros físicos y modelo URDF del robot.

---

## Estructura

```
caddy_ai2_ros2_description/
├── bringup/
│   ├── config/
│   │   └── robot_params.yaml       # Parámetros físicos del robot
│   ├── launch/
│   │   └── display.launch.py       # Visualización en RViz
│   └── rviz/
│       └── display.rviz            # Configuración de RViz
└── description/
    └── model/
        ├── meshes/stl/             # Malla STL del chasis
        └── urdf/
            └── caddy_ai2_model.urdf.j2   # Template URDF base (Jinja2)
```

---

## Arquitectura

El paquete usa **Jinja2** como motor de plantillas. Los parámetros físicos se definen una sola vez en `robot_params.yaml` y se inyectan en los templates en tiempo de launch, sin necesidad de recompilar.

| Fichero | Paquete | Formato | Usado por |
|---|---|---|---|
| `caddy_ai2_model.urdf.j2` | `caddy_ai2_ros2_description` | URDF + Jinja2 | Display (RViz) + Robot real |
| `caddy_ai2_model_sim.urdf.j2` | `caddy_ai2_ros2_gazebo_simulation` | URDF + Jinja2 | Solo simulación Gazebo |

`caddy_ai2_model_sim.urdf.j2` extiende el template base mediante herencia Jinja2 (`{%- extends %}`), añadiendo el bloque `ros2_control` con el plugin `gz_ros2_control/GazeboSimSystem` y el plugin de Gazebo `gz_ros2_control::GazeboSimROS2ControlPlugin`.

---

## Parámetros físicos (`robot_params.yaml`)

### Cinemática

| Parámetro | Valor | Unidad | Descripción |
|---|---|---|---|
| `wheelbase` | 1.65 | m | Distancia entre ejes delantero y trasero |
| `track_width` | 0.91 | m | Distancia entre centros de rueda izquierda/derecha |
| `wheel_radius` | 0.235 | m | Radio de la rueda |
| `max_steer_angle` | 0.4 | rad | Límite de dirección (software) |

### Físicos / Colisión

| Parámetro | Valor | Unidad | Descripción |
|---|---|---|---|
| `mass` | 590 | kg | Masa total del vehículo |
| `height` | 0.25 | m | Altura del cuerpo (usada para inercia) |
| `wheel_width` | 0.22 | m | Anchura de rueda |
| `wheel_mass` | 8.7 | kg | Masa de cada rueda |
| `vehicle_collision_length` | 2.660 | m | Longitud del box de colisión |
| `vehicle_collision_width` | 1.230 | m | Anchura del box de colisión |
| `vehicle_collision_height` | 1.7 | m | Altura del box de colisión |
| `vehicle_collision_offset_x` | -0.25 | m | Offset X del box de colisión respecto a `base_link` |
| `inertial_origin_offset_x` | -0.275 | m | Offset X del origen inercial respecto a `base_link` |

### Sensores

Los sensores habilitados y sus poses de montaje se definen en la sección `sensors` del mismo fichero. Cada entrada puede habilitarse/deshabilitarse con `enabled: true/false` sin eliminar la configuración.

| Sensor | Tipo | Estado | `frame_id` | Nota |
|---|---|---|---|---|
| `imu_sbg_ig500n` | IMU | habilitado | `imu_link` | — |
| `sick_lms_291` | 2D LiDAR | habilitado | `lidar_sick_lms_291_link` | pose PROVISIONAL |
| `ydlidar_x4` | 2D LiDAR | habilitado | `ydlidar_x4_link` | pose PROVISIONAL, apunta hacia atrás (yaw=π) |
| `navsat_generic` | GPS | deshabilitado | `navsat_link` | — |

---

## Árbol TF (jerarquía de links)

```
base_footprint                  ← link raíz (plano del suelo)
└── base_link                   ← chasis (offset z = wheel_radius)
    ├── steering_link            ← eje de dirección (x = +wheelbase/2)
    │   ├── front_right_wheel   ← rueda delantera derecha
    │   └── front_left_wheel    ← rueda delantera izquierda
    └── traction_link           ← eje de tracción continuo (x = -wheelbase/2)
        ├── rear_right_wheel    ← rueda trasera derecha
        └── rear_left_wheel     ← rueda trasera izquierda

base_footprint (también padre de los sensores habilitados):
    ├── imu_link
    ├── lidar_sick_lms_291_link
    └── ydlidar_x4_link
```

Los joints de los sensores son `fixed`, anclados a `base_footprint`.  
`steering_joint` es `revolute` (rango ±`max_steer_angle`). `system_traction_joint` es `continuous`.

---

## Launch: display.launch.py

Lanza `robot_state_publisher` + `joint_state_publisher` + RViz para visualizar el robot ensamblado.

```bash
# Visualización standalone
ros2 launch caddy_ai2_ros2_description display.launch.py

# Con simulación Gazebo corriendo (no lanza joint_state_publisher)
ros2 launch caddy_ai2_ros2_description display.launch.py simulation:=true

# Con robot real corriendo (no lanza joint_state_publisher)
ros2 launch caddy_ai2_ros2_description display.launch.py real_robot:=true

# Con namespace y prefix (multi-robot)
ros2 launch caddy_ai2_ros2_description display.launch.py namespace:=robot1 prefix:=robot1_
```

### Argumentos

| Argumento | Default | Descripción |
|---|---|---|
| `namespace` | `''` | Namespace ROS del robot |
| `prefix` | `''` | Prefijo para nombres de links y joints |
| `simulation` | `false` | Los joint states vienen de Gazebo |
| `real_robot` | `false` | Los joint states vienen del hardware real |

`joint_state_publisher` solo arranca cuando tanto `simulation` como `real_robot` son `false`.

### Inclusión desde otro launch

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('caddy_ai2_ros2_description'),
            'bringup', 'launch', 'display.launch.py'
        )
    ),
    launch_arguments={
        'namespace': 'robot1',
        'real_robot': 'true',
    }.items()
)
```

---

## Dependencias

```bash
sudo apt install ros-${ROS_DISTRO}-robot-state-publisher
sudo apt install ros-${ROS_DISTRO}-joint-state-publisher
sudo apt install ros-${ROS_DISTRO}-rviz2
pip install jinja2
```

---

## Desarrollo

La configuración de VS Code recomendada (extensiones y asociaciones de ficheros `.j2`) está documentada en [`caddy_ai2_ros2_conventions/vscode.md`](../caddy_ai2_ros2_conventions/vscode.md).

---

## Tópicos publicados

| Tópico | Tipo | Descripción |
|---|---|---|
| `/robot_description` | `std_msgs/String` | URDF renderizado |
| `/joint_states` | `sensor_msgs/JointState` | Estado de joints (solo en modo display) |
| `/tf` | `tf2_msgs/TFMessage` | Árbol de transforms |
| `/tf_static` | `tf2_msgs/TFMessage` | Transforms de joints fijos |
