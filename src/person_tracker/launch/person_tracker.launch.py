from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    LaunchDescription()

    tracker = Node(
        package="person_tracker",
        executable="detect_person",
        
        
    
    )
    follow = Node(
        package="person_tracker",
        executable="follow_person",
        
    )

    compressed = Node(
            package='image_transport',
            executable='republish',
            name='image_republisher',
            arguments=['compressed', 'raw'],
            remappings=[
                ('in/compressed', '/camera/color/image_raw/compressed'),
                ('out', '/camera/image_raw/uncompressed')
            ]
        )


  

    return LaunchDescription([tracker,
                              follow,
                              compressed])  