from easy_markers.generator import MarkerGenerator, get_point, get_quat
from visualization_msgs.msg import InteractiveMarker
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from visualization_msgs.msg import InteractiveMarkerControl
from math import sqrt

TYPEDATA = {
    'rotate_x': [1, 1, 0, 0, InteractiveMarkerControl.ROTATE_AXIS],
    'rotate_y': [1, 0, 0, 1, InteractiveMarkerControl.ROTATE_AXIS],
    'rotate_z': [1, 0, 1, 0, InteractiveMarkerControl.ROTATE_AXIS],
    'move_x': [1, 1, 0, 0, InteractiveMarkerControl.MOVE_AXIS],
    'move_y': [1, 0, 0, 1, InteractiveMarkerControl.MOVE_AXIS],
    'move_z': [1, 0, 1, 0, InteractiveMarkerControl.MOVE_AXIS],
}
SQRT2 = sqrt(2)


def default_callback(feedback):
    print(feedback)


class InteractiveGenerator:
    def __init__(self, node, name='interactive_markers'):
        self.server = InteractiveMarkerServer(node, name)
        self.mg = MarkerGenerator(node)
        self.mg.type = 1
        self.mg.scale = [.25] * 3
        self.c = 0
        self.markers = {}

    def makeMarker(self, callback=None, marker=None, position=None, controls=[],
                   fixed=False, name=None, frame='map', description='', imode=0, rot=None):

        if marker is None:
            marker = self.mg.marker()

        if callback is None:
            callback = default_callback

        if name is None:
            name = f'control{self.c}'
            self.c += 1

        int_marker = InteractiveMarker()
        int_marker.header.frame_id = frame
        int_marker.pose.position = get_point(position)
        int_marker.pose.orientation = get_quat(rot)
        int_marker.scale = 1.0
        int_marker.name = name
        int_marker.description = description

        control = InteractiveMarkerControl()
        control.always_visible = True
        control.interaction_mode = imode
        control.markers.append(marker)
        int_marker.controls.append(control)

        for control_name in controls:
            data = TYPEDATA[control_name]
            control = InteractiveMarkerControl()
            control.orientation.w = data[0] / SQRT2
            control.orientation.x = data[1] / SQRT2
            control.orientation.y = data[2] / SQRT2
            control.orientation.z = data[3] / SQRT2
            control.name = control_name
            control.interaction_mode = data[4]
            if fixed:
                control.orientation_mode = InteractiveMarkerControl.FIXED
            int_marker.controls.append(control)

        self.server.insert(int_marker, feedback_callback=callback)
        self.markers[name] = int_marker
        self.server.applyChanges()
        return int_marker
