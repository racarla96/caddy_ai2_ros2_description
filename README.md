# caddy_ai2_ros2_description

**Versión:** 1.0.0
**Autor/es:** Ricardo  (rinese89), Rafael Carbonell Lázaro (racarla96)
**Fecha:** 2026
**Repositorio:** https://github.com/racarla96/caddy_ai2

---

## 📋 Descripción

Paquete ROS 2 para el robot agrícola Caddy AI2, un vehículo de 4 ruedas con geometría Ackermann (tracción trasera y dirección delantera). Diseñado para investigación en agricultura de precisión y navegación autónoma.

---

## 📦 Contenido del Paquete

```
caddy_ai2/
├── caddy_ai2_ros2_description/           # Modelo 3D y URDF
│   ├── urdf/                          # Archivos XACRO
│   ├── meshes/                         # STL del chasis y ruedas
│   ├── config/                          # Configuración RViz
│   └── launch/                           # Lanzadores específicos
│
├── caddy_ai2_common/                   # Librerías compartidas
│   ├── hardware_interfaces/               # Interfaces para hardware
│   ├── messages/                           # Mensajes ROS2 personalizados
│   └── utils/                               # Cinemática Ackermann
│
├── caddy_ai2_ros2_control_system_steering_driver/  # Control dirección
├── caddy_ai2_ros2_control_system_traction_driver/  # Control tracción
└── caddy_ai2_bringup/                               # Lanzamiento global
    ├── config/                                        # Parámetros globales
    ├── launch/                                          # Lanzadores principales
    └── urdf/                                              # Copia del URDF
```

---

## ⚙️ Requisitos del Sistema

### Hardware Recomendado
- CPU: Intel i5 / AMD Ryzen 5 o superior
- RAM: 8 GB mínimo (16 GB recomendado)
- GPU: Compatible con OpenGL 3.3+ (para RViz/Gazebo)
- Espacio: 5 GB libres

### Software
- Sistema Operativo: Ubuntu 22.04 LTS / 24.04 LTS
- ROS 2: Humble, Iron o Rolling
- Gazebo: Fortress o Garden (opcional)
- Python: 3.8+
- Compilador: g++ 9.4+

### Dependencias ROS 2
```bash
sudo apt install ros-${ROS_DISTRO}-xacro
sudo apt install ros-${ROS_DISTRO}-joint-state-publisher-gui
sudo apt install ros-${ROS_DISTRO}-robot-state-publisher
sudo apt install ros-${ROS_DISTRO}-rviz2
sudo apt install ros-${ROS_DISTRO}-gazebo-ros-pkgs    # Opcional
sudo apt install ros-${ROS_DISTRO}-ros2-control       # Opcional
```

---

## 🚀 Instalación

### 1. Crear espacio de trabajo (si no existe)
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### 2. Clonar el repositorio
```bash
cd src
git clone https://github.com/racarla96/caddy_ai2.git
```

### 3. Compilar
```bash
cd ~/ros2_ws
colcon build --packages-select caddy_ai2_ros2_description caddy_ai2_bringup
source install/setup.bash
```

### 4. Verificar instalación
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py --show-args
```

---

## 🎮 Guía Rápida de Uso

### Modo Visualización (por defecto)
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py
```

### Solo Robot State Publisher (headless)
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py enable_rviz:=false use_gui:=false
```

### Con Gazebo (simulación física)
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py enable_gazebo:=true
```

### Con ros2_control (modo simulación)
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py enable_ros2_control:=true
```

### Modo Hardware Real
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py is_simulation:=false enable_ros2_control:=true
```

### Simulación Completa
```bash
ros2 launch caddy_ai2_bringup vehicle_complete.launch.py \
    enable_gazebo:=true \
    enable_rviz:=true \
    enable_ros2_control:=true \
    world_name:=warehouse.world
```

---

## 📐 Especificaciones Técnicas

### Geometría del Vehículo

| Parámetro | Símbolo | Valor | Unidades |
|-----------|---------|-------|----------|
| Distancia entre ejes | L | 1.65 | m |
| Vía (ancho) | W | 1.0068 | m |
| Radio ruedas | r | 0.28 | m |
| Ancho ruedas | w | 0.212 | m |
| Altura chasis (centro) | h | 0.4 | m |
| Masa total | m | ~5.14 | kg |

### Posiciones Relativas (sistema de coordenadas)

| Elemento | X (m) | Y (m) | Z (m) |
|----------|-------|-------|-------|
| Centro de masas | 0 | 0 | 0 |
| Eje delantero | +0.825 | 0 | 0 |
| Eje trasero | -0.825 | 0 | 0 |
| Rueda delantera izquierda | +0.825 | +0.5034 | 0 |
| Rueda delantera derecha | +0.825 | -0.5034 | 0 |
| Rueda trasera izquierda | -0.825 | +0.5034 | 0 |
| Rueda trasera derecha | -0.825 | -0.5034 | 0 |
| Centro visual chasis | 0 | 0 | +0.4 |

### Límites de Dirección
- Ángulo máximo: ±0.61 rad (±35°)
- Velocidad máxima dirección: 1.0 rad/s
- Par máximo: 10 Nm

### Límites de Tracción
- Velocidad lineal máxima: 2.0 m/s
- Velocidad angular máxima: 1.5 rad/s

---

## 🎛️ Argumentos del Launch File

| Argumento | Default | Descripción |
|-----------|---------|-------------|
| is_simulation | true | Usar hardware simulado vs real |
| enable_rviz | true | Iniciar RViz para visualización |
| enable_gazebo | false | Iniciar Gazebo para simulación física |
| enable_ros2_control | false | Habilitar sistema ros2_control |
| use_gui | true | Mostrar sliders GUI para joints |
| world_name | empty | Mundo de Gazebo a cargar |
| rviz_config | display.rviz | Archivo de configuración de RViz |

### Nota sobre use_gui
- true: Lanza joint_state_publisher_gui - interfaz con sliders para mover joints manualmente
- false: Lanza joint_state_publisher sin interfaz - usa valores por defecto

---

## 🔬 Tópicos y Servicios

### Sin ros2_control
| Tópico | Tipo | Descripción |
|--------|------|-------------|
| /joint_states | sensor_msgs/JointState | Estado de todos los joints |
| /tf | tf2_msgs/TFMessage | Transforms del robot |
| /tf_static | tf2_msgs/TFMessage | Transforms estáticos |

### Con ros2_control habilitado
| Tópico | Tipo | Descripción |
|--------|------|-------------|
| /traction_controller/commands | std_msgs/Float64MultiArray | Velocidad ruedas traseras [rad/s] |
| /steering_controller/commands | std_msgs/Float64MultiArray | Ángulo dirección [rad] |
| /joint_states | sensor_msgs/JointState | Estado actualizado |

### Comandos de prueba
```bash
# Mover dirección a 0.3 rad
ros2 topic pub /left_front_steer_joint/command std_msgs/msg/Float64 "data: 0.3" -1

# Ver transforms
ros2 run tf2_tools view_frames

# Listar todos los tópicos
ros2 topic list
```

---

## 🛠️ Personalización

### Modificar geometría
Edita caddy_ai2_ros2_description/urdf/caddy_ai2.urdf.xacro:
```xml
<xacro:property name="wheelbase" value="1.65" />
<xacro:property name="track_width" value="1.0068" />
<xacro:property name="wheel_radius" value="0.28" />
<xacro:property name="chassis_z" value="0.4" />
```

### Ajustar límites
```xml
<joint name="left_front_steer_joint" type="revolute">
    <limit lower="-0.61" upper="0.61" effort="10" velocity="1.0"/>
</joint>
```

---

## 🧪 Testing y Depuración

### Verificar modelo URDF
```bash
cd ~/ros2_ws
xacro src/caddy_ai2/caddy_ai2_ros2_description/urdf/caddy_ai2.urdf.xacro > /tmp/caddy.urdf
check_urdf /tmp/caddy.urdf
```

### Visualizar árbol de joints
```bash
urdf_to_graphiz /tmp/caddy.urdf
evince /tmp/caddy.pdf
```

### Ver gráfico de computación
```bash
rqt_graph
```

### Depurar transforms
```bash
ros2 run tf2_ros tf2_echo base_footprint base_link
ros2 run tf2_ros tf2_echo base_link wheel_left_front_link
```

---

## ⚠️ Solución de Problemas

### Error: "package not found"
```bash
source ~/ros2_ws/install/setup.bash
# Añadir a ~/.bashrc: echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

### RViz no muestra el robot
1. Verificar que robot_state_publisher está corriendo: ros2 node list
2. Comprobar fixed frame en RViz: debe ser base_footprint
3. Publicar un joint state manual para probar

### Gazebo no inicia
```bash
gazebo --version
gazebo /opt/ros/${ROS_DISTRO}/share/gazebo_ros/worlds/empty.world
```

### ros2_control no responde
```bash
ros2 control list_controllers
ros2 param dump /controller_manager
```

---

## 📄 Licencia

**Copyright (c) 2026, racarla96 - Rafael Carbonell Lázaro**

Esta obra está bajo una **Licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0)**.

### Usted es libre de:
- Compartir — copiar y redistribuir el material en cualquier medio o formato
- Adaptar — remezclar, transformar y construir a partir del material para cualquier propósito, incluso comercialmente

### Bajo los siguientes términos:
- Atribución — Debe dar crédito adecuado, proporcionar un enlace a la licencia e indicar si se realizaron cambios.
- No restricciones adicionales — No puede aplicar términos legales ni medidas tecnológicas que restrinjan legalmente a otros.

### Avisos:
- No se otorgan garantías. La licencia puede no otorgarle todos los permisos necesarios.

**Texto completo de la licencia:**
https://creativecommons.org/licenses/by/4.0/legalcode

---

## 👤 Autor

**Rafael Carbonell Lázaro** (racarla96)

- Email: rafael.carbonell@ejemplo.com
- GitHub: https://github.com/racarla96
- LinkedIn: https://linkedin.com/in/rafaelcarbonell

---

## 📅 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2026-02-18 | Versión inicial estable |
| 0.9.0 | 2026-01-15 | Beta - pruebas de campo |
| 0.5.0 | 2025-12-01 | Alpha - modelo básico |

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (git checkout -b feature/NuevaCaracteristica)
3. Commit cambios (git commit -m 'Añadir nueva característica')
4. Push (git push origin feature/NuevaCaracteristica)
5. Abre un Pull Request
```